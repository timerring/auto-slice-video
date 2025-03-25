# Copyright (c) 2025 auto-slice-video

import numpy as np
from numba import cuda
import math
import warnings

warnings.filterwarnings("ignore")


@cuda.jit
def calculate_window_density(timestamps, window_size, step, results):
    """
    Calculate the density of timestamps in a given window size.

    Args:
        timestamps: List of timestamps
        window_size: Size of the window
        step: Step size
        results: Array to store the density of each window
    """
    # get the index of the current thread
    idx = cuda.grid(1)

    if idx < len(results):
        window_start = timestamps[0] + idx * step
        window_end = window_start + window_size

        count = 0
        # calculate the number of timestamps in the window
        for t in timestamps:
            if window_start <= t <= window_end:
                count += 1

        results[idx] = count / window_size


def find_dense_periods_gpu(timestamps, window_size, top_n, max_overlap, step):
    """
    Find the dense periods of timestamps in a given window size.

    Args:
        timestamps: List of timestamps
        window_size: Size of the window
        step: Step size
        top_n: Number of top density periods to return
        max_overlap: Maximum allowed overlap between periods (in seconds)

    Returns:
        List of tuples (start_time, density) sorted by density in descending order
    """
    timestamps = np.array(timestamps, dtype=np.float32)

    # calculate the number of needed windows
    start_time = timestamps.min()
    end_time = timestamps.max()
    num_windows = math.ceil((end_time - start_time) / step)

    # prepare the GPU arrays
    results = np.zeros(num_windows, dtype=np.float32)
    d_timestamps = cuda.to_device(timestamps)
    d_results = cuda.to_device(results)

    # configure the CUDA grid
    threads_per_block = 256
    blocks = (num_windows + threads_per_block - 1) // threads_per_block

    # start the CUDA cores
    calculate_window_density[blocks, threads_per_block](
        d_timestamps, window_size, step, d_results
    )

    # copy the results back to the host
    results = d_results.copy_to_host()

    # find all the density values and their indices
    density_periods = [(i, results[i]) for i in range(len(results))]
    density_periods.sort(key=lambda x: x[1], reverse=True)

    # if no need to control the overlap, return the top n results
    if max_overlap is None:
        selected_indices = [i for i, _ in density_periods[:top_n]]
    else:
        # filter the intervals with too much overlap
        selected_indices = []
        for idx, density in density_periods:
            current_start = start_time + idx * step

            # check if the interval overlaps too much with the already selected intervals
            valid_period = True
            for selected_idx in selected_indices:
                selected_start = start_time + selected_idx * step
                overlap = min(
                    selected_start + window_size, current_start + window_size
                ) - max(selected_start, current_start)
                if overlap > max_overlap:
                    valid_period = False
                    break

            if valid_period:
                selected_indices.append(idx)
                if len(selected_indices) == top_n:
                    break

    densest_periods = [
        (int(start_time + i * step), int(results[i] * window_size))
        for i in selected_indices
    ]

    return densest_periods
