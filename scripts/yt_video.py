
from config.config import *
import os
import random
import time
from scripts.utils import *
from googleapiclient.errors import HttpError
from http.client import HTTPException

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
MAX_RETRIES = 10

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import google.auth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from googleapiclient.http import MediaFileUpload


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
config: Config = Config()
SECRET_FILE = config.get("credentials", "secret_file")
TOKEN_FILE = config.get("credentials", "token_file")

def _youtube_authenticate():
    # Check if token.json exists (stores user's access and refresh tokens)
    if TOKEN_FILE == None or SECRET_FILE == None:
        raise FileExistsError()
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials are available, go through the authorization flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    print("Creds validated")
    print("Building")
    return build("youtube", "v3", credentials=creds)
# This method implements an exponential backoff strategy to resume a failed upload.


def _resumable_upload(request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print('Uploading file...')
            status, response = request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print(
                        f'Video id "{response["id"]}" was successfully uploaded.')
                    return True
                else:
                    exit(
                        f'The upload failed with an unexpected response: {response}')
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = f'A retriable HTTP error {e.resp.status} occurred:\n{e.content}'
            else:
                raise
        except (HTTPException, IOError) as e:  # Replace RETRIABLE_EXCEPTIONS with specific exceptions
            error = f'A retriable error occurred: {e}'

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit('No longer attempting to retry.')

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print(f'Sleeping {sleep_seconds:.2f} seconds and then retrying...')
            time.sleep(sleep_seconds)

def video_insert_short(video_name, video_path):
    if ( not is_video_less_than_a_minute(video_path)):
        return
    video_insert(video_name, video_path)

def video_insert(video_name, video_path):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    youtube = _youtube_authenticate()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": "#shorts #ytshorts #funny #interesting #memes #trending #bangers #music",
                "title": video_name
            },
            "status": {
                "privacyStatus": "public"
            }
        },

        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )

    return _resumable_upload(request)
