from .calculate.sliding_cpu import calculate_density, extract_dialogues

dialogues = extract_dialogues('./sample.ass')
density_periods = calculate_density(dialogues, window_size=300, top_n=3, max_overlap=60)
print(density_periods)