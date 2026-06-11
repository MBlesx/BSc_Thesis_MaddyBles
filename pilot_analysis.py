"""
Analysis script for my thesis pilot test survey.
For each participant, average scores are calculated for happiness (Q1) and
energy (Q2) across three conditions: neutral, happy, and exaggerated happy.
Repeated-measures ANOVAs are conducted separately for happiness and energy.
Compares male and female stimulus ratings by calculating mean happiness and 
energy scores for each condition. 
An interpretation section classifies the mean ratings as being closer to the 
low/neutral (1), medium/happy (3), or high/exag. happy (5) end of the Likert scale. 
"""

import pandas as pd
from statsmodels.stats.anova import AnovaRM
import sys


# Loading Data
file_path = "pilot_data.xlsx"
df = pd.read_excel(file_path, header=1)


# Cleaning column names
df.columns = (
    df.columns
    .astype(str)
    .str.replace("\n", " ", regex=False)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip())


# Only take valid responses
df = df[
    (df["Finished"].astype(str).str.strip() == "True") &
    (df["DistributionChannel"].astype(str).str.strip().str.lower() == "anonymous")
].copy()

print("N participants:", len(df))


# Transforming into likert scale
scale = {
    "Not happy at all": 1,
    "Slightly happy": 2,
    "Somewhat happy": 3,
    "Very happy": 4,
    "Extremely happy": 5,

    "Not energetic at all": 1,
    "Slightly energetic": 2,
    "Somewhat energetic": 3,
    "Very energetic": 4,
    "Extremely energetic": 5}


# Convert into numeric
columns_to_convert = [
    "Male neutral q1",
    "Male neutral q2",
    "Male happy q1",
    "Male happy q2",
    "Male exag. happy q1",
    "Male exag. happy q2",
    "Female neutral q1",
    "Female neutral q2",
    "Female happy q1",
    "Female happy q2",
    "Female exag.happy q1",
    "Female exag.happy q2"]

for col in columns_to_convert:
    df[col + "_score"] = df[col].map(scale)


# Condition scores
# Q1 = happiness, Q2 = ENERGY

# Happiness (Q1 only)
df["neutral_happiness"] = df[["Male neutral q1_score", "Female neutral q1_score"]].mean(axis=1)
df["happy_happiness"] = df[["Male happy q1_score", "Female happy q1_score"]].mean(axis=1)
df["exag_happiness"] = df[["Male exag. happy q1_score", "Female exag.happy q1_score"]].mean(axis=1)

# Energy (Q2 only)
df["neutral_energy"] = df[["Male neutral q2_score", "Female neutral q2_score"]].mean(axis=1)
df["happy_energy"] = df[["Male happy q2_score", "Female happy q2_score"]].mean(axis=1)
df["exag_energy"] = df[["Male exag. happy q2_score", "Female exag.happy q2_score"]].mean(axis=1)



# redirect all output to a .txt file instead of console
output_path = "pilot_results.txt"
original_stdout = sys.stdout

with open(output_path, "w") as f:
    sys.stdout = f
    
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    # Results ordered in a nice way
    conditions = ["neutral", "happy", "exag"]
    
    print("=============================== RESULTS ===============================")
    
    for i in conditions:
        print(f"\n{i.upper()}")
        print("Happiness:", round(df[f"{i}_happiness"].mean(), 2))
        print("Energy:", round(df[f"{i}_energy"].mean(), 2))
    
    
    # Repeated Measures ANOVA
    anova_df = pd.DataFrame({
        "participant": df.index,
    
        "neutral_happiness": df["neutral_happiness"],
        "happy_happiness": df["happy_happiness"],
        "exag_happiness": df["exag_happiness"],
    
        "neutral_energy": df["neutral_energy"],
        "happy_energy": df["happy_energy"],
        "exag_energy": df["exag_energy"]})
    
    
    # Long format, happiness
    happiness_long = pd.melt(
        anova_df,
        id_vars=["participant"],
        value_vars=["neutral_happiness", "happy_happiness", "exag_happiness"],
        var_name="condition",
        value_name="happiness")
    
    happiness_long["condition"] = happiness_long["condition"].replace({
        "neutral_happiness": "neutral",
        "happy_happiness": "happy",
        "exag_happiness": "exag. happy"})
    
    
    # Long format, energy
    energy_long = pd.melt(
        anova_df,
        id_vars=["participant"],
        value_vars=["neutral_energy", "happy_energy", "exag_energy"],
        var_name="condition",
        value_name="energy")
    
    energy_long["condition"] = energy_long["condition"].replace({
        "neutral_energy": "neutral",
        "happy_energy": "happy",
        "exag_energy": "exag. happy"})
    
    
    # ANOVA happiness
    anova_happiness = AnovaRM(
        happiness_long,
        depvar="happiness",
        subject="participant",
        within=["condition"]).fit()
    
    print("\n========================== ANOVA, HAPPINESS ==========================")
    print(anova_happiness)
    
    
    # ANOVA energy
    anova_energy = AnovaRM(
        energy_long,
        depvar="energy",
        subject="participant",
        within=["condition"]).fit()
    
    print("\n=========================== ANOVA, ENERGY ===========================")
    print(anova_energy)
    
    
    # Male vs Female comparing
    comparison = pd.DataFrame({
        "condition": ["neutral", "happy", "exag. happy"],
    
        "male_happiness": [
            df["Male neutral q1_score"].mean(),
            df["Male happy q1_score"].mean(),
            df["Male exag. happy q1_score"].mean()],
    
        "female_happiness": [
            df["Female neutral q1_score"].mean(),
            df["Female happy q1_score"].mean(),
            df["Female exag.happy q1_score"].mean()],
    
        "male_energy": [
            df["Male neutral q2_score"].mean(),
            df["Male happy q2_score"].mean(),
            df["Male exag. happy q2_score"].mean()],
    
        "female_energy": [
            df["Female neutral q2_score"].mean(),
            df["Female happy q2_score"].mean(),
            df["Female exag.happy q2_score"].mean()]
    })
    
    print("\n=================== MALE vs FEMALE PER CONDITION ===================")
    print(comparison)
    
    
    # Calculate if 1,3 or 5 is closer (neutral, happy, exaggerated happy) with a simple function
    def closeness(x):
        if abs(x - 1) < abs(x - 3) and abs(x - 1) < abs(x - 5):
            return "closer to 1 (low)"
        elif abs(x - 3) < abs(x - 1) and abs(x - 3) < abs(x - 5):
            return "closer to 3 (medium)"
        else:
            return "closer to 5 (high)"
    
    
    print("\n=========================== INTERPRETATION ===========================")
    # Using the created closeness function
    for _, row in comparison.iterrows():
        print(f"\nCondition: {row['condition']}")
    
        print("Happiness:")
        print("- Male:", round(row["male_happiness"], 2),closeness(row["male_happiness"]))
        print("- Female:", round(row["female_happiness"], 2),closeness(row["female_happiness"]))
    
        print("Energy:")
        print("- Male:", round(row["male_energy"], 2),closeness(row["male_energy"]))
        print("- Female:", round(row["female_energy"], 2),closeness(row["female_energy"]))

        
# Without this I wil get 'I/O operation on closed file' error
sys.stdout = original_stdout
print(f"Results saved to: {output_path}")