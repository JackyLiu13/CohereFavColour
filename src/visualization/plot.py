import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from collections import defaultdict
import json
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

# Load from data directory
data_path = os.path.join(PROJECT_ROOT, 'data', 'colours.json')
with open(data_path, 'r') as f:
    colour_data = json.load(f)

# Create nested dictionary to count frequencies per temperature (including N/A)
color_counts = defaultdict(lambda: defaultdict(int))
for temp, colours in colour_data.items():
    for colour in colours:
        if colour == "N/A":
            color_counts[temp]["N/A"] += 1
        else:
            color_counts[temp][colour] += 1

# Convert to DataFrame and clean up formatting
df = pd.DataFrame(color_counts).T.fillna(0).astype(int)
df.index = df.index.astype(float).sort_values(ascending=False)

# Ensure N/A is the first column, then sort the rest
colour_columns = sorted([col for col in df.columns if col != "N/A"])
if "N/A" in df.columns:
    df = df[["N/A"] + colour_columns]
else:
    df = df[colour_columns]

# Create figure and axis
fig, ax = plt.subplots(figsize=(14, 10))
# plt.gca().set_facecolor('#FFFFFF')

# Plot configuration
num_rows = len(df.index)
num_cols = len(df.columns)
ax.set_xticks(range(num_cols))

# Create labels with both hex code and colour name
labels = []
for col in df.columns:
    if col == "N/A":
        labels.append("N/A\n(Not Available)")
    else:
        colour_name = get_colour_name(col)
        labels.append(f"{col}\n({colour_name})")

ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_yticks(range(num_rows))
ax.set_yticklabels(df.index)

# Draw coloured rectangles with frequency annotations
for y_idx, temp in enumerate(df.index):
    for x_idx, colour_code in enumerate(df.columns):
        count = df.loc[temp, colour_code]
        if count > 0:
            if colour_code == "N/A":
                # Special handling for N/A values - light grey
                rect = patches.Rectangle(
                    (x_idx - 0.5, y_idx - 0.5), 1, 1,
                    facecolor='#CCCCCC',
                    edgecolor='white',
                    linewidth=0.5
                )
                text_color = 'black'
            else:
                rect = patches.Rectangle(
                    (x_idx - 0.5, y_idx - 0.5), 1, 1,
                    facecolor=colour_code,
                    edgecolor='white',
                    linewidth=0.5
                )
                rgb = mcolors.to_rgb(colour_code)
                text_color = 'white' if (0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]) < 0.5 else 'black'
            
            ax.add_patch(rect)
            ax.text(x_idx, y_idx, str(count),
                    ha='center', va='center',
                    color=text_color, fontsize=8,
                    weight='bold')

# Set axis limits and labels
ax.set_xlim(-0.5, num_cols - 0.5)
ax.set_ylim(-0.5, num_rows - 0.5)
plt.title("Cohere Colour Selection Frequency by Temperature\n(N/A shown in light grey)", pad=20)
plt.xlabel("Colours (Hex Code and Name)")
plt.ylabel("Temperature (Descending Order)")
plt.tight_layout()

# Save plot to data directory
viz_path = os.path.join(PROJECT_ROOT, 'visualizations', 'temperature_distribution.png')
os.makedirs(os.path.dirname(viz_path), exist_ok=True)
plt.savefig(viz_path)
plt.close()