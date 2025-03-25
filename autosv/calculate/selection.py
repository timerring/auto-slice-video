# Copyright (c) 2025 auto-slice-video

import subprocess
from .sliding_cpu import find_dense_periods_cpu


def check_cuda_available():
    """Check if CUDA is available by testing nvcc command."""
    try:
        subprocess.run(
            ["nvcc", "-V"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


USE_GPU = check_cuda_available()
if USE_GPU:
    try:
        from .sliding_gpu import find_dense_periods_gpu
    except ImportError:
        USE_GPU = False


def find_dense_periods(log, timestamps, window_size, top_n, max_overlap, step):
    """Find dense periods using either GPU or CPU implementation based on GPU availability."""
    if USE_GPU:
        log.info("Using GPU implementation")
        return find_dense_periods_gpu(timestamps, window_size, top_n, max_overlap, step)

    log.info("Using CPU implementation")
    return find_dense_periods_cpu(timestamps, window_size, top_n, max_overlap, step)
