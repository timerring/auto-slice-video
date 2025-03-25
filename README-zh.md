<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/headerDark.svg" />
    <img src="assets/headerLight.svg" alt="auto-slice-video" />
  </picture>

基于弹幕密度的自动高能片段切片机

[English](./README.md) | 简体中文

</div>

## 功能

- 基于滑动窗口算法检测弹幕密集的时间段
- 根据弹幕密度自动切片视频
- 支持 Nvidia GPU 加速计算（[自动选择是否使用GPU加速](#为什么我不能使用gpu加速)）
- 支持自定义数量的视频切片
- 支持自定义切片时长
- 添加详细的日志信息
- 支持命令行使用和API使用

## 效果展示

![](https://cdn.jsdelivr.net/gh/timerring/scratchpad2023/2024/2025-03-25-18-27-58.gif)

## 安装

使用此工具前，您需要先安装ffmpeg:

- Windows: `choco install ffmpeg`（通过[Chocolatey](https://chocolatey.org/)）或其他方法
- macOS: `brew install ffmpeg`（通过[Homebrew](https://brew.sh/)）
- Linux: `sudo apt install ffmpeg`（Debian/Ubuntu）

更多操作系统安装 ffmpeg 请参考[官方网站](https://ffmpeg.org/download.html)。

安装 autosv:

```bash
pip install autosv
```

## 使用方法

### 命令行使用

```bash
# eg. 默认参数见 autosv -h
autosv -a sample.ass -v sample.mp4
autosv -a sample.ass -v sample.mp4 -d 300 -n 3 --overlap 60 --step 1
autosv -h
# optional arguments:
#   -h, --help            show this help message and exit
#   -V, --version         Print version information
#   -a ASS, --ass ASS     The input ass file of the danmaku
#   -v VIDEO, --video VIDEO
#                         The input video file
#   -d DURATION, --duration DURATION
#                         The duration(seconds) of the sliced highlight video, default is 60
#   -n TOP_N, --top_n TOP_N
#                         The number of the top dense periods to return, default is 1
#   --overlap OVERLAP     The overlapped(seconds) between the sliced highlight videos, default is 30
#   --step STEP           The step(seconds) of the sliding window, default is 1
```

### API使用

```python
from autosv import slice_video_by_danmaku
# 基本参数同上
slice_video_by_danmaku(ass_path, video_path, duration=300, top_n=3, max_overlap=60, step=1)
```

## 常见问题

### 为什么我不能使用gpu加速？

`autosv` 会通过 `nvcc -V` 检测机器上是否可用cuda，如果您的机器有NVIDIA GPU，请确保您的驱动已安装且cuda可用。同时，确保您已安装正确版本的`numba`和`numpy`。