# Copyright (c) 2025 auto-slice-video

import os
from .calculate.selection import find_dense_periods
from .slice.slice_video import slice_video
from .log.logger import Log


def parse_time(time_str):
    """Convert ASS time format to seconds with milliseconds."""
    h, m, s = time_str.split(":")
    s, ms = s.split(".")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def extract_timestamps(file_path):
    """Extract dialogue start times from the ASS file."""
    timestamps = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("Dialogue:"):
                parts = line.split(",")
                start_time = parse_time(parts[1].strip())
                timestamps.append(start_time)
    return timestamps


def slice_video_by_danmaku(
    ass_path, video_path, duration=60, top_n=1, max_overlap=30, step=1
):
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
    autosv_log = Log("autosv")
    autosv_log.info("autosv v0.0.3")
    autosv_log.info("https://github.com/timerring/auto-slice-video")
    output_folder = os.path.abspath(os.path.dirname(video_path))
    video_name = os.path.basename(video_path)
    timestamps = extract_timestamps(ass_path)
    dense_periods = find_dense_periods(
        autosv_log, timestamps, duration, top_n, max_overlap, step
    )
    autosv_log.info("The dense periods and their count are:")
    slices_path = []
    for period in dense_periods:
        autosv_log.info(
            f"Start from {period[0]} to {period[0] + duration} seconds with the count is {period[1]}"
        )
        slice_video(
            video_path,
            f"{output_folder}/{period[0]}s_{video_name}",
            period[0],
            duration,
        )
        autosv_log.info(f"Slice the {output_folder}/{period[0]}s_{video_name} done.")
        slices_path.append(f"{output_folder}/{period[0]}s_{video_name}")
    return slices_path


if __name__ == "__main__":
    slice_video_by_danmaku("./test/sample.ass", "./test/sample.mp4", 300, 3, 60, 1)
