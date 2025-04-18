from scripts.yt_video import *
import sys
import argparse



if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='YouTube Video Uploader')
    parser.add_argument('--channel_name', required=True,
                        help='Name of youtube channel to upload video')
    args = parser.parse_args()
    channels = config.get("youtube_channel_token_paths")
    if args.channel_name not in channels:
        print(f"Error: Channel {args.channel_name} not found in {channels}")
        sys.exit(1)
    youtube_authenticate(channels.get(args.channel_name, None))
