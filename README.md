# YouTubeVideoUploader
Upload video to youtube using python

## Prerequisites
 - Google's Data v3 API. 
    - Google Account and Google Cloud Project (GCP)
    - Setup OAuth 2.0 in the Google Cloud Terminal
    - Undergo an [audit](https://support.google.com/youtube/contact/yt_api_form) in order to get public video upload privileges. See top of [Data v3 Insert Endpoint](https://developers.google.com/youtube/v3/docs/videos/insert) for more information.
 - Create config.toml in config folder that matches the following format:
 ```
[credentials]
secret_file="<location>"
input_vid_dir="<location>"
[youtube_channel_token_paths]
CHANNEL_NAME = "<path to token.json for this channel>"
[youtube_channel_descriptions]
CHANNEL_NAME = "<video description>"
[youtube_channel_title_additions]
CHANNEL_NAME = "<end of title hashtags/ extra additions>"
[youtube_channel_category_id]
CHANNEL_NAME = <Youtube category Ids. e.g. 23>
 ```
 Note: CHANNEL_NAME can be anything and the config file supports multiple channels
 - Ensure the directories specified in the config already exist. Specifically the token paths and secret_file.
 - Download secrets file from GCP in location specified in config.
 - Download token by running `python3 update_token.py --channel_name CHANNEL_NAME`
 
 ## Function
 - Using your GCP under development works fine you will just need to recreate a token every week by running the previously mentioned update_token.py
 - The name of the video will be the name of the video uploaded.
 - Place the video(s) wanting to be uploaded into input folder.
 - Run `python3 main.py --channel_name CHANNEL_NAME`