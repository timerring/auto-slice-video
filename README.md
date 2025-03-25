# auto-slice-video

Auto slice the shorts based on the density of danmaku.

## Features

- Detect the dense period of danmaku based on the sliding window algorithm.
- Slice the video based on the density of danmaku.
- Support GPU accelerated calculation.(Automatically choose whether to use GPU acceleration)
- Support custom quantity slicing videos.
- Support custom slice duration.

## Prerequisites

To use this tool, you need to install ffmpeg first.

- Windows: `choco install ffmpeg` (via [Chocolatey](https://chocolatey.org/)) or other methods.
- macOS: `brew install ffmpeg` (via [Homebrew](https://brew.sh/)).
- Linux: `sudo apt install ffmpeg` (Debian/Ubuntu). 

More OS please refer to the [official website](https://ffmpeg.org/download.html).

## Usage

### cli usage

```bash
python -m autoslice.autosv
```

### api usage

```python
from autoslice.autosv import slice_video_by_danmaku

slice_video_by_danmaku(ass_path, video_path, duration=300, top_n=3, max_overlap=60, step=1)
```
