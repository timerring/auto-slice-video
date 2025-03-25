# Copyright (c) 2025 auto-slice-video

import os
from .calculate.selection import find_dense_periods
from .slice.slice_video import slice_video

def parse_time(time_str):
    """Convert ASS time format to seconds with milliseconds."""
    h, m, s = time_str.split(':')
    s, ms = s.split('.')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

def extract_timestamps(file_path):
    """Extract dialogue start times from the ASS file."""
    timestamps = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('Dialogue:'):
                parts = line.split(',')
                start_time = parse_time(parts[1].strip())
                timestamps.append(start_time)
    return timestamps

def slice_video_by_danmaku(ass_path, video_path, duration=300, top_n=3, max_overlap=60, step=1):
    """
    Slice the video by the dense periods of danmaku.

    Args:
        ass_path: The path to the ASS file.
        video_path: The path to the video file.
        duration: The duration of the slice.
        top_n: The number of top dense periods to return.
        max_overlap: The maximum allowed overlap between periods (in seconds).
        step: The step size for sliding window (in seconds).
    """
    output_folder = os.path.dirname(video_path)
    video_name = os.path.basename(video_path)
    timestamps = extract_timestamps(ass_path)
    dense_periods = find_dense_periods(timestamps, duration, top_n, max_overlap, step)
    print("The dense periods and their count are:")
    i = 1
    for period in dense_periods:
        print(f"Start from {period[0]} seconds with the count is {period[1]}")
        slice_video(video_path, f'{output_folder}{i}_{video_name}', period[0], duration)
        i += 1

if __name__ == "__main__":
    slice_video_by_danmaku('./sample.ass', './sample.mp4', 300, 3, 60, 1)