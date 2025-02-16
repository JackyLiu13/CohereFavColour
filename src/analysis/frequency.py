import json
from collections import defaultdict
import os
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

# Get project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# colour dictionary with hex as keys
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

def get_colour_name(hex_code):
    """Get exact colour name for a hex code"""
    if hex_code == "N/A":
        return "Not Available"
    try:
        return HEX_TO_NAME.get(hex_code.upper(), "Unknown")
    except:
        return "Unknown"

def analyze_frequencies():
    # Load from data directory
    colours_path = os.path.join(PROJECT_ROOT, 'data', 'colours.json')
    with open(colours_path, 'r') as f:
        colour_data = json.load(f)
    
    # Create frequency dictionary
    frequency_map = defaultdict(lambda: {"frequency": 0, "temperatures": set()})
    
    # Process all entries
    for temp, colours in colour_data.items():
        for colour in colours:
            frequency_map[colour]["frequency"] += 1
            frequency_map[colour]["temperatures"].add(temp)
    
    # Convert sets to sorted lists
    sorted_data = []
    for colour, data in frequency_map.items():
        sorted_temps = sorted(data["temperatures"], key=lambda x: float(x))
        sorted_data.append({
            "hex": colour,
            "frequency": data["frequency"],
            "temperatures": sorted_temps
        })
    
    # Sort by frequency descending
    sorted_data.sort(key=lambda x: (-x["frequency"], x["hex"]))
    
    # Save to data directory
    freq_path = os.path.join(PROJECT_ROOT, 'data', 'frequency.json')
    with open(freq_path, 'w') as f:
        json.dump(sorted_data, f, indent=2)
    
    # Create and save colour_list format
    colour_list = {entry["hex"]: entry["frequency"] for entry in sorted_data}
    colour_list_path = os.path.join(PROJECT_ROOT, 'data', 'colour_list.json')
    with open(colour_list_path, 'w') as f:
        json.dump(colour_list, f, indent=2)
    
    # Print formatted table
    print("\nColour Frequency and Temperature Distribution:")
    print("-" * 85)
    print(f"{'Hex':<10} | {'Colour Name':<20} | {'Frequency':>8} | {'Temperatures'}")
    print("-" * 85)
    
    for entry in sorted_data:
        hex_code = entry["hex"]
        name = get_colour_name(hex_code)
        temps = ', '.join(entry["temperatures"])
        print(f"{hex_code:<10} | {name:<20} | {entry['frequency']:>8} | {temps}")
    
    print(f"\nFrequency data saved to frequency.json and colour_list.json")

if __name__ == "__main__":
    analyze_frequencies() 