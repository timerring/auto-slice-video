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

## 安装

使用此工具前，您需要先安装ffmpeg。

- Windows: `choco install ffmpeg`（通过[Chocolatey](https://chocolatey.org/)）或其他方法
- macOS: `brew install ffmpeg`（通过[Homebrew](https://brew.sh/)）
- Linux: `sudo apt install ffmpeg`（Debian/Ubuntu）

更多操作系统安装 ffmpeg 请参考[官方网站](https://ffmpeg.org/download.html)。

## 使用方法

### 命令行使用

```bash
python -m autosv.cli
```

### API使用

```python
from autosv import slice_video_by_danmaku

slice_video_by_danmaku(ass_path, video_path, duration=300, top_n=3, max_overlap=60, step=1)
```

## 常见问题

### 为什么我不能使用gpu加速？

`autosv` 会通过 `nvcc -V` 检测机器上是否可用 `cuda`，如果您的机器有 NVIDIA GPU，请确保显卡的驱动已正确安装并且 `cuda` 可用。