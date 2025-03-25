# Copyright (c) 2025 auto-slice-video

from .calculate.selection import find_dense_periods

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

timestamps = extract_timestamps('./sample.ass')
dense_periods = find_dense_periods(timestamps, 300, 3, 60)
print(dense_periods)