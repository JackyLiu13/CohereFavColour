import json
import matplotlib.pyplot as plt
import os
import matplotlib.colors as mcolors

# Project root directory setup
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Complete color definitions (copied from original source)
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

# Create case-insensitive lookup
HEX_TO_NAME = {hex_code.upper(): name for hex_code, name in BASIC_COLOURS.items()}

def generate_pie_chart():
    """Generate pie chart from colour frequency data"""
    # Load data
    data_path = os.path.join(PROJECT_ROOT, 'data', 'colour_list.json')
    with open(data_path, 'r') as f:
        colour_list = json.load(f)
    
    # Prepare data
    sorted_colours = sorted(colour_list.items(), key=lambda x: -x[1])
    top_colours = sorted_colours[:5]
    other = sum(count for _, count in sorted_colours[5:])
    
    # Create labels with colour names
    labels = []
    na_indices = []
    for colour, _ in top_colours:
        if colour == "N/A":
            name = "Not Available"
            na_indices.append(len(labels))  # Track N/A positions
        else:
            name = HEX_TO_NAME.get(colour.upper(), "Unknown")
        labels.append(f"{colour}\n({name})")
    labels.append(f"Other\n({other})")
    
    # Prepare colors with validation
    colours = []
    for colour, _ in top_colours:
        if colour == "N/A" or not mcolors.is_color_like(colour):
            colours.append('#CCCCCC')  # Light grey for N/A/invalid
        else:
            colours.append(colour)
    colours.append('#808080')  # Darker grey for "Other"
    
    # Create plot
    plt.figure(figsize=(12, 8))
    wedges, texts, _ = plt.pie([count for _, count in top_colours] + [other], 
            labels=labels, 
            colors=colours,
            autopct='%1.1f%%', 
            startangle=140)
    
    
    plt.title("Overall Colour Distribution Across All Temperatures\nin Cohere Responses", pad=20)
    
    # Save visualization
    viz_path = os.path.join(PROJECT_ROOT, 'visualizations', 'pie_distribution.png')
    os.makedirs(os.path.dirname(viz_path), exist_ok=True)
    plt.savefig(viz_path)
    plt.close()
    return viz_path

def generate_valid_pie_chart():
    """Generate pie chart from colour frequency data, excluding N/A responses"""
    # Load data
    data_path = os.path.join(PROJECT_ROOT, 'data', 'colour_list.json')
    with open(data_path, 'r') as f:
        colour_list = json.load(f)
    
    # Filter out N/A and prepare data
    valid_colours = {k: v for k, v in colour_list.items() if k != "N/A"}
    sorted_colours = sorted(valid_colours.items(), key=lambda x: -x[1])
    
    # Create labels and data arrays
    labels = []
    counts = []
    colours = []
    
    for colour, count in sorted_colours:
        name = HEX_TO_NAME.get(colour.upper(), "Unknown")
        labels.append(f"{colour}\n({name})")
        counts.append(count)
        colours.append(colour)
    
    # Create plot
    plt.figure(figsize=(16, 10))
    wedges, texts, _ = plt.pie(counts, 
            labels=labels, 
            colors=colours,
            autopct='%1.1f%%', 
            startangle=140,
            pctdistance=0.85,
            labeldistance=1.05)
    
    # Improve readability
    plt.title("Complete Colour Distribution\n(Excluding N/A Responses)", pad=20, fontsize=14)
    plt.tight_layout()
    
    # Save visualization
    viz_path = os.path.join(PROJECT_ROOT, 'visualizations', 'full_pie_distribution.png')
    os.makedirs(os.path.dirname(viz_path), exist_ok=True)
    plt.savefig(viz_path, bbox_inches='tight')
    plt.close()
    return viz_path

if __name__ == "__main__":
    generate_pie_chart()
    generate_valid_pie_chart() 