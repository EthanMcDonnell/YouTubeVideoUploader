from yt_video import *
from utils import *

def main():
    video_path, video_name = find_single_video("input")
    video_insert(video_name, video_path)

if __name__ == "__main__":
    main()