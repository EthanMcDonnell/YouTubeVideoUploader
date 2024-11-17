from yt_video import *
from utils import *

def main():
    num_of_videos = get_number_of_videos("input")
    last_video = ""
    for _ in range(num_of_videos):
        video_path, video_name = find_single_video("input")
        if (last_video == video_name):
            print("duplicate video found")
            return
        if (video_insert(video_name, video_path)):
            last_video = video_name
            os.remove(video_path)
            print(f"{video_path} has been removed")

if __name__ == "__main__":
    main()