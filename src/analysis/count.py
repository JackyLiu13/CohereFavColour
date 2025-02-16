import json
from collections import defaultdict
from scipy.spatial import KDTree
import numpy as np
import matplotlib.pyplot as plt
import os

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Update colour definitions and naming
BASIC_COLOURS = {
    # Standard colours
    '#00FF00': 'Lime',
    '#007FFF': 'Azure',
    '#FF5733': 'Persimmon',
    '#00FFFF': 'Aqua',
    '#0000FF': 'Blue',
    '#FF4500': 'Orange Red',
    '#3498DB': 'Steel Blue',
    '#FF8C00': 'Dark Orange',
    '#008000': 'Green',
    '#000000': 'Black',
    '#660066': 'Purple',
    '#FF0000': 'Red',
    
    # Blue variants
    '#0077B6': 'Star Command Blue',
    '#0077BE': 'Star Command Blue',
    '#0077C8': 'Star Command Blue',
    '#0074D9': 'Brandeis Blue',
    '#002366': 'Royal Blue',
    '#007BFF': 'Azure Radiance',
    '#0080FF': 'Azure Radiance',
    '#0072BB': 'Star Command Blue',
    '#3498db': 'Steel Blue',
    '#0074D9': 'Brandeis Blue'
}

HEX_TO_NAME = {hex_code.upper(): name for hex_code, name in BASIC_COLOURS.items()}

def get_colour_name(hex_code):
    """Get exact colour name for a hex code"""
    if hex_code == "N/A":
        return "Not Available"
    try:
        return HEX_TO_NAME.get(hex_code.upper(), "Unknown")
    except:
        return "Unknown"

def plot_colour_frequencies(colour_counts):
    # Sort colours by frequency
    sorted_items = sorted(colour_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Prepare data for plotting
    hex_codes = []
    frequencies = []
    colours = []
    labels = []
    
    for hex_code, freq in sorted_items:
        hex_codes.append(hex_code)
        frequencies.append(freq)
        if hex_code == "N/A":
            colours.append('#CCCCCC')  # Light grey for N/A
            labels.append("N/A\n(Not Available)")
        else:
            colours.append(hex_code)
            labels.append(f"{hex_code}\n({get_colour_name(hex_code)})")
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    bars = plt.bar(range(len(frequencies)), frequencies, color=colours)
    
    # Customize the plot
    plt.xticks(range(len(frequencies)), labels, rotation=45, ha='right')
    plt.title("Colour Frequencies in Cohere's Responses")
    plt.xlabel("Colours (Hex Code and Name)")
    plt.ylabel("Frequency")
    
    # Add frequency labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    # Save visualization to data directory
    viz_path = os.path.join(PROJECT_ROOT, 'visualizations', 'colour_frequencies.png')
    os.makedirs(os.path.dirname(viz_path), exist_ok=True)
    plt.savefig(viz_path)
    plt.close()
    return viz_path

def count_colours():
    # Read from data directory
    data_path = os.path.join(PROJECT_ROOT, 'data', 'colours.json')
    with open(data_path, 'r') as f:
        colour_data = json.load(f)
    
    # Initialize counter for all colours
    colour_counts = defaultdict(int)
    
    # Count occurrences of each colour across all temperatures
    for temp, colours in colour_data.items():
        for colour in colours:
            colour_counts[colour] += 1
    
    # Sort by count in descending order
    sorted_counts = sorted(colour_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Print results
    print("\nColour frequency across all temperatures:")
    print("-" * 65)
    print(f"{'Hex Code':<15} | {'Colour Name':<25} | {'Count':>8}")
    print("-" * 65)
    
    for colour, count in sorted_counts:
        colour_name = get_colour_name(colour)
        print(f"{colour:<15} | {colour_name:<25} | {count:>8}")
    
    print("-" * 65)
    print(f"{'Total':<43} | {sum(colour_counts.values()):>8}")
    
    # Generate the visualization
    viz_path = plot_colour_frequencies(colour_counts)
    print("\nVisualization saved as 'visualizations/colour_frequencies.png'")

def plot_temperature_distribution(colour_data):
    """Create temperature-specific colour distribution table"""
    temp_dist = {}
    
    # Process data
    for temp, colours in colour_data.items():
        counts = {}
        for colour in colours:
            if colour == "N/A":
                continue
            counts[colour] = counts.get(colour, 0) + 1
        # Get top 3 colours per temperature
        top_colours = sorted(counts.items(), key=lambda x: -x[1])[:3]
        temp_dist[float(temp)] = top_colours
    
    # Create plot
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    ax.axis('off')
    
    # Create table
    cell_text = []
    for temp in sorted(temp_dist.keys(), reverse=True):
        row = [f"{temp:.1f}"]
        for colour, count in temp_dist[temp]:
            row.append(f"{colour} ({count})")
        cell_text.append(row)
    
    table = plt.table(cellText=cell_text,
                     colLabels=['Temperature', '1st', '2nd', '3rd'],
                     loc='center',
                     cellLoc='center')
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    
    plt.title("Top Colours per Temperature")
    viz_path = os.path.join(PROJECT_ROOT, 'visualizations', 'temperature_ranking.png')
    os.makedirs(os.path.dirname(viz_path), exist_ok=True)
    plt.savefig(viz_path)
    plt.close()

if __name__ == "__main__":
    count_colours()
