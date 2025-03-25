# Copyright (c) 2025 auto-slice-video

import argparse
import sys
import os
from autosv import slice_video_by_danmaku


def cli():
    parser = argparse.ArgumentParser(
        description="Auto slice the highlight shorts based on the density of danmaku."
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="autosv 0.0.1",
        help="Print version information",
    )
    parser.add_argument(
        "-a",
        "--ass",
        required=True,
        type=str,
        help="The input ass file of the danmaku",
    )
    parser.add_argument(
        "-v",
        "--video",
        required=True,
        type=str,
        help="The input video file",
    )
    parser.add_argument(
        "-d",
        "--duration",
        default=60,
        type=int,
        help="The duration(seconds) of the sliced highlight video, default is 60",
    )
    parser.add_argument(
        "-n",
        "--top_n",
        default=1,
        type=int,
        help="The number of the top dense periods to return, default is 1",
    )
    parser.add_argument(
        "--overlap",
        default=30,
        type=int,
        help="The overlapped(seconds) between the sliced highlight videos, default is 30",
    )
    parser.add_argument(
        "--step",
        default=1,
        type=int,
        help="The step(seconds) of the sliding window, default is 1",
    )

    args = parser.parse_args()
    if os.path.splitext(args.ass)[1] == ".ass":
        slice_video_by_danmaku(
            args.ass, args.video, args.duration, args.top_n, args.overlap, args.step
        )
    else:
        print("Please assign the correct input the file in ass format!", flush=True)


if __name__ == "__main__":
    cli()
