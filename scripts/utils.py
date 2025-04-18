import shutil
import os
import json
from moviepy.editor import VideoFileClip


def is_video_less_than_a_minute(file_path):
    
    clip = VideoFileClip(file_path)
    duration = clip.duration  # Duration in seconds
    clip.close()
    print(f"video '{file_path}' is less than a minute {duration < 60}")
    return duration < 60


def move_file(source_path, destination_path):
    """
    Move a file from the source path to the destination path.

    Args:
        source_path (str): The path of the file to move.
        destination_path (str): The path to move the file to.

    Returns:
        None

    Raises:
        FileNotFoundError: If the source file does not exist.
        PermissionError: If there are insufficient permissions to move the file.
        Exception: For other unexpected errors.
    """
    try:
        if not os.path.exists(source_path):
            raise FileNotFoundError(
                f"Source file '{source_path}' does not exist.")

        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # Move the file
        shutil.move(source_path, destination_path)
        print(f"File moved from '{source_path}' to '{destination_path}'")
    except Exception as e:
        print(f"Error moving file: {e}")


def get_field_from_json(file_path, *field_path):
    """
    Retrieve a nested field from a JSON file given a list of field names representing the path.
    
    Args:
        file_path (str): Path to the JSON file.
        field_path (str): Variable-length argument list representing the path to the field.
    
    Returns:
        The value at the specified path in the JSON structure, or None if not found.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        # Traverse through the field path
        for field in field_path:
            data = data.get(field)
            if data is None:
                return None  # Return None if any part of the path is invalid

        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file: {e}")
        return None

"""
Returns:
    video path, video name (without extension)
"""
def find_single_video(folder_path):
    # Define common video file extensions
    video_extensions = {'.mp4', '.mkv', '.avi',
                        '.mov', '.flv', '.wmv', '.webm'}

    # List all files in the folder with video extensions
    video_files = [file for file in os.listdir(folder_path)
                   if os.path.splitext(file)[1].lower() in video_extensions]

    # Check for multiple or no video files
    if len(video_files) == 0:
        raise FileNotFoundError("No video files found in the folder.")

    # Return the single video file name
    return os.path.join(folder_path, video_files[0]), os.path.splitext(os.path.basename(video_files[0]))[0]


def get_number_of_videos(folder_path):

    video_extensions = {'.mp4', '.mkv', '.avi',
                        '.mov', '.flv', '.wmv', '.webm'}

    # List all files in the folder with video extensions
    video_files = [file for file in os.listdir(folder_path)
                   if os.path.splitext(file)[1].lower() in video_extensions]
    return len(video_files)
