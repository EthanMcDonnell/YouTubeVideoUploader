from scripts.yt_video import *
from scripts.utils import *
from config.config import Config
import argparse
import sys

config = Config()


def main(token_path, vid_description, vid_title_additions, yt_category_id:int):
    print("Youtube Video Uploader Commenced")
    
    if (token_path is None):
        print("token path shouldnt be None")
        sys.exit(1)
    print(f"Using token path: {token_path}")
    input_vid_dir = config.get("credentials", "input_vid_dir")
    num_of_videos = get_number_of_videos(input_vid_dir)
    last_video = ""
    if num_of_videos > 1:
        print(f"Number of videos found: {num_of_videos}")
        raise Exception("Multiple videos found in input_vid_dir")
    try:
        for _ in range(num_of_videos):
            video_path, video_name = find_single_video(input_vid_dir)
            if (last_video == video_name):
                print("duplicate video found")
                return
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
            video_name += vid_title_additions
            youtube = youtube_authenticate(token_path)
            if (video_insert(youtube, video_name, video_path, vid_description, yt_category_id)):
                last_video = video_name
                os.remove(video_path)
                print(f"{video_path} has been removed")
                
    except Exception as e:
        print("Error occurred during video upload")
        print("Moving video to error folder")
        print(e)
        video = os.path.basename(video_path)
        move_file(video_path, "error/" + video)

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='YouTube Video Uploader')
    parser.add_argument('--channel_name', required=True,
                        help='Name of youtube channel to upload video')
    args = parser.parse_args()
    channels = config.get("youtube_channel_token_paths")
    description = config.get("youtube_channel_descriptions")
    title_additions = config.get("youtube_channel_title_additions")
    category_id = config.get("youtube_channel_category_id")
    if args.channel_name not in channels:
        print(f"Error: Channel {args.channel_name} not found in {channels}")
        sys.exit(1)
    
    main(channels.get(args.channel_name, None), description.get(args.channel_name, "Thanks, sub for more :)"), title_additions.get(args.channel_name, ""), category_id.get(args.channel_name, 24))
