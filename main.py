from scripts.yt_video import *
from scripts.utils import *
from config.config import Config
def main():
    input_vid_dir = Config().get("credentials", "input_vid_dir")
    num_of_videos = get_number_of_videos(input_vid_dir)
    last_video = ""
    for _ in range(num_of_videos):
        video_path, video_name = find_single_video(input_vid_dir)
        if (last_video == video_name):
            print("duplicate video found")
            return
        if (video_insert(video_name, video_path)):
            last_video = video_name
            os.remove(video_path)
            print(f"{video_path} has been removed")

if __name__ == "__main__":
    main()