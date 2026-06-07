# Thesis Experiment Survey Analysis

Analysis script for my thesis investigating how emotional tone and situation 
severity affect perceived social appropriateness and perceived credibility of 
digital healthcare assistant responses.

## Files
- `analysis.py` — main analysis script
- `columns.py` — column definitions for the survey data

## Requirements
Install dependencies with:
pip install -r requirements.txt

## Usage
1. Place your survey data file in the `data/` folder
2. Update the `file_path` variable in `analysis.py` to match your filename
3. Run `analysis.py`
4. Results are saved to `results/analysis_results.txt`

## Analysis
- Cronbach's alpha for scale reliability
- Repeated Measures ANOVA (emotion x severity)
- Mixed Linear Models with demographic covariates and baseline mood

## Note
Raw data is not included in this repository.
