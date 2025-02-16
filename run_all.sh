#!/bin/bash
# idk if this works lol iont have a mac to test
# someone buy me a mac or an internship to afford a mac lmaoo

# Create directories if missing
mkdir -p data
mkdir -p visualizations

# Launch a process for each temperature
for i in {0..10}
do
    temperature=$(echo "scale=1; $i/10" | bc)
    python main.py --temperature $temperature &
done

# Wait for all processes to complete
wait

# Merge the results
python main.py --merge
python src/analysis/count.py
python src/analysis/frequency.py
python src/visualization/plot.py
python src/visualization/pie_chart.py 