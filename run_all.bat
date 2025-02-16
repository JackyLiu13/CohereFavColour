@echo off
setlocal enabledelayedexpansion

:: Launch a process for each temperature
for /l %%i in (0,1,10) do (
    set /a "num=%%i"
    set /a "dec=!num! * 10"
    set "temperature=0.!num!"
    if %%i == 10 (
        set "temperature=1.0"
    )
    start /b python main.py --temperature !temperature!
)

:: Wait for all processes to complete
wait

:: Merge the results
python main.py --merge
python src/analysis/count.py
python src/analysis/frequency.py
python src/visualization/plot.py
python src/visualization/pie_chart.py   
