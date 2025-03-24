from collections import defaultdict

def parse_time(time_str):
    """Convert ASS time format to seconds with milliseconds."""
    h, m, s = time_str.split(':')
    s, ms = s.split('.')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 100

def format_time(seconds):
    """Format seconds to hh:mm:ss.xx."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 100)
    return f"{h:02}:{m:02}:{s:02}.{ms:02}"

def extract_dialogues(file_path):
    """Extract dialogue start times from the ASS file."""
    dialogues = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('Dialogue:'):
                parts = line.split(',')
                start_time = parse_time(parts[1].strip())
                dialogues.append(start_time)
    return dialogues

def calculate_density(dialogues, window_size=300, top_n=1, max_overlap=60):
    """Calculate the top N maximum density periods of dialogues in a given window size.
    
    Args:
        dialogues: List of dialogue timestamps
        window_size: Size of the sliding window
        top_n: Number of top density periods to return
        max_overlap: Maximum allowed overlap between periods (in seconds)
    
    Returns:
        List of tuples (start_time, density) sorted by density in descending order
    """
    time_counts = defaultdict(int)
    for time in dialogues:
        time_counts[time] += 1

    # Store (start_time, density) pairs
    density_periods = []

    # Use a sliding window to calculate density
    sorted_times = sorted(time_counts.keys())
    for i in range(len(sorted_times)):
        start_time = sorted_times[i]
        end_time = start_time + window_size
        current_density = sum(count for time, count in time_counts.items() 
                            if start_time <= time < end_time)
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
            overlap = min(selected_start + window_size, start_time + window_size) - max(selected_start, start_time)
            if overlap > max_overlap:
                valid_period = False
                break
        
        if valid_period:
            filtered_periods.append((start_time, density))
            if len(filtered_periods) == top_n:
                break
    
    return filtered_periods

