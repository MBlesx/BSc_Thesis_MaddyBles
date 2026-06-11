# Thesis Experiment Survey Analysis

Analysis script for my thesis investigating how emotional expression and situation 
severity affect perceived social appropriateness and perceived credibility of 
digital healthcare assistant responses.

## Files
- `analysis.py`: main analysis script.
- `columns.py`: column definitions for the survey data.
- `data.xlsx`: anonymized survey dataset used for analysis. The dataset contains participant responses after cleaning, including removal of IP addresses, names, and other identifying data.
- `results.txt`: results from analysis script using `data.xlsx`.
- `pilot_analysis.py`: pilot study analysis script.
- `pilot_data.xlsx`: anonymized survey dataset used for pilot study analysis. The dataset contains participant responses after cleaning (removal of IP addresses).
- `pilot_results.txt`: results from pilot study analysis script using `pilot_data.xlsx`.

## Requirements
Install liberaries mentioned in requirements.txt, using pip install 

## Usage
1. Update the `file_path` in `analysis.py` or `pilot_data.xlsx` to match your data filename;
2. Run `analysis.py` or `pilot_data.xlsx`;
3. Results are saved to `results.txt` or `pilot_results.txt`.

## Main Analysis
- Cronbach's alpha for internal consistency of survey questions
- Repeated Measures ANOVA (emotion x severity)
- Mixed Linear Models with demographic covariates and baseline mood

## Pilot Study Analysis
- Mean happiness and energy scores per condition
- Repeated Measures ANOVA (neutral, happy, and exaggerated happy)
- Male vs Female stimulus comparisons
- Likert-scale interpretation of condition means

## License 
MIT license is used. See [LICENSE](https://github.com/MBlesx/BSc_Thesis_MaddyBles/blob/main/LICENSE) for details. 


