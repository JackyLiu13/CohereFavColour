import os
import re
import cohere
from dotenv import load_dotenv
import json
import argparse
from pathlib import Path

def process_temperature(temperature: float) -> dict:
    """Process a single temperature and return its colour results."""
    # Load API keys from .env file
    load_dotenv()
    api_key = os.getenv("CO_API_KEY")
    co = cohere.ClientV2(api_key=api_key)
    
    results = []
    print(f"Processing Temperature: {temperature}")
    
    for i in range(1, 101):
        response = co.chat(
            messages=[{
                "role": "user",
                "content": "What's your favourite colour? Give me 1 hex value"
            }],
            model="command-r-plus-08-2024",
            temperature=temperature,
        )
        
        # Extract text from response
        response_text = response.message.content[0].text
        hex_colour = re.search(r'#[0-9a-fA-F]{6}', response_text)
        if hex_colour:
            colour = hex_colour.group()
            print(f"Run {i}: {colour}")
            results.append(colour)
        else:
            print(f"Run {i}: No valid hex colour found in response: {response_text}")
            results.append("N/A")
    
    return {str(temperature): results}

def save_results(results: dict, temp: float):
    """Save results to data directory"""
    os.makedirs('data', exist_ok=True)
    output_file = f'data/colours_temp_{temp}.json'
    with open(output_file, 'w') as f:
        json.dump(results, f)
    print(f"Results saved to {output_file}")

def merge_results():
    """Merge results in data directory"""
    all_results = {}
    temp_files = Path('data').glob('colours_temp_*.json')
    
    # Read and merge all results
    for temp_file in temp_files:
        with open(temp_file, 'r') as f:
            results = json.load(f)
            all_results.update(results)
    
    # Save merged results
    if all_results:
        with open('data/colours.json', 'w') as f:
            json.dump(all_results, f)
        print("All results merged into colours.json")
        
        # Clean up temporary files
        for temp_file in Path('data').glob('colours_temp_*.json'):
            temp_file.unlink()
        print("Temporary files cleaned up")

def main():
    parser = argparse.ArgumentParser(description='Process colours for a specific temperature')
    parser.add_argument('--temperature', type=float, help='Temperature to process (0.0 to 1.0)')
    parser.add_argument('--merge', action='store_true', help='Merge all result files')
    
    args = parser.parse_args()
    
    if args.merge:
        merge_results()
    elif args.temperature is not None:
        if 0 <= args.temperature <= 1:
            results = process_temperature(args.temperature)
            save_results(results, args.temperature)
        else:
            print("Temperature must be between 0.0 and 1.0")
    else:
        print("Please specify either --temperature or --merge")

if __name__ == "__main__":
    main()

