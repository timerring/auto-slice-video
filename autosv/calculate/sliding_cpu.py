# Copyright (c) 2025 auto-slice-video

from collections import defaultdict


def find_dense_periods_cpu(timestamps, window_size, top_n, max_overlap, step):
    """Calculate the top N maximum density periods of timestamps in a given window size.

    Args:
        timestamps: List of dialogue timestamps
        window_size: Size of the sliding window
        top_n: Number of top density periods to return
        max_overlap: Maximum allowed overlap between periods (in seconds)
        step: Step size for sliding window (in seconds)

    Returns:
        List of tuples (start_time, density) sorted by density in descending order
    """
    time_counts = defaultdict(int)
    for time in timestamps:
        time_counts[time] += 1

    # Store (start_time, density) pairs
    density_periods = []

    # Use a sliding window to calculate density
    sorted_times = sorted(time_counts.keys())
    for i in range(0, len(sorted_times), step):
        start_time = sorted_times[i]
        end_time = start_time + window_size
        current_density = sum(
            count
            for time, count in time_counts.items()
            if start_time <= time < end_time
        )
        density_periods.append((start_time, current_density))

    # Sort by density in descending order and return top N results
    density_periods.sort(key=lambda x: x[1], reverse=True)
    # If max_overlap is not specified, return top N results directly
    if max_overlap is None:
        return density_periods[:top_n]

    # Filter periods with overlap constraint
    filtered_periods = []
    for start_time, density in density_periods:
        # Check if current period overlaps too much with any selected period
        valid_period = True
        for selected_start, _ in filtered_periods:
            overlap = min(selected_start + window_size, start_time + window_size) - max(
                selected_start, start_time
            )
            if overlap > max_overlap:
                valid_period = False
                break

        if valid_period:
            filtered_periods.append((int(start_time), density))
            if len(filtered_periods) == top_n:
                break

    return filtered_periods
