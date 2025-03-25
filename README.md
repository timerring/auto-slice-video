<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/headerDark.svg" />
    <img src="assets/headerLight.svg" alt="auto-slice-video" />
  </picture>

**Auto slice the highlight shorts** based on the density of danmaku.

English | [简体中文](./README-zh.md)

</div>

## Features

- Detect the dense period of danmaku based on the sliding window algorithm.
- Slice the video based on the density of danmaku.
- Support GPU accelerated calculation.([Automatically choose whether to use GPU acceleration](#why-i-cannot-use-the-gpu-acceleration))
- Support custom quantity slicing videos.
- Support custom slice duration.

## Installation

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
from autosv import slice_video_by_danmaku

slice_video_by_danmaku(ass_path, video_path, duration=300, top_n=3, max_overlap=60, step=1)
```

## common issues

### Why I cannot use the gpu acceleration?

The autosv will detect whether the cuda is available on the machine via `nvcc -V`, if your machine has nvidia gpu, please make sure your driver is installed and the cuda is available.