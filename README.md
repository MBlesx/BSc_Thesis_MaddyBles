# Thesis Experiment Survey Analysis

Analysis script for my thesis investigating how emotional expression and situation 
severity affect perceived social appropriateness and perceived credibility of 
digital healthcare assistant responses.

## Files
- `analysis.py`: main analysis script
- `columns.py`: column definitions for the survey data
- `data.xlsx`:
- `results.txt`: results from analysis scrips using `data.xlsx`

## Requirements
Install liberaries mentioned in requirements.txt, using pip install 

## Usage
1. Update the `file_path` in `analysis.py` to match your data filename
2. Run `analysis.py`
3. Results are saved to `results/analysis_results.txt`

## Analysis
- Cronbach's alpha for internal consistency of survey questions
- Repeated Measures ANOVA (emotion x severity)
- Mixed Linear Models with demographic covariates and baseline mood

## License 
MIT license is used. See [LICENSE](https://github.com/MBlesx/BSc_Thesis_MaddyBles/blob/main/LICENSE) for details. 


