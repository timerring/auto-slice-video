# Copyright (c) 2024 bilive.
# Copyright (c) 2025 auto-slice-video

import subprocess


def format_time(seconds):
    """Format seconds to hh:mm:ss."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"


def slice_video(video_path, output_path, start_time, duration):
    """Slice the video using ffmpeg."""
    duration = format_time(duration)
    command = [
        "ffmpeg",
        "-y",
        "-ss",
        format_time(start_time),
        "-i",
        video_path,
        "-t",
        duration,
        "-map_metadata",
        "-1",
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        output_path,
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
