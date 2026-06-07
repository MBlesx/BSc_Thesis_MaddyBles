

"""
Analysis script for my thesis experiment survey.
Runs Cronbach's alpha, Repeated Measures ANOVA, and mixed models
for perceived social appropriateness and perceived credibility.
"""


# loading the data and libraries

import sys
import pingouin as pg
import pandas as pd
import statsmodels.formula.api as smf
import columns as clms

file_path = "data/survey_data.xlsx"
df = pd.read_excel(file_path, header=1)

# keep only the real responses
df = df[~df.iloc[:, 0].astype(str).str.contains("ImportId|Imagine|What is", na=False)]

# removing leftover headers and reset row numbers
df = df.drop(index=0).reset_index(drop=True)


# from text to numbers and invalid values to NaN
likert_map = {
    "Completely disagree": 1,
    "Disagree": 2,
    "Neither agree nor disagree": 3,
    "Agree": 4,
    "Completely agree": 5
}

for col in clms.app_cred:
    df[col] = df[col].replace(likert_map)
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(how="all")


# redirect all output to a .txt file instead of console
output_path = "results/analysis_results.txt"
original_stdout = sys.stdout

with open(output_path, "w") as f:
    sys.stdout = f
    
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)

    # Cronbach's alpha check and print it nicely
    print("CRONBACH'S ALPHA CHECK")

    alpha_tests = [("Neutral, Non-Severe - Cred", clms.neutral_nons_cred),
        ("Neutral, Non-Severe - App", clms.neutral_nons_app),
        ("Happy, Non-Severe - App", clms.happy_nons_app),
        ("Happy, Non-Severe - Cred", clms.happy_nons_cred),
        ("ExHappy, Non-Severe - App", clms.exhappy_nons_app),
        ("ExHappy, Non-Severe - Cred", clms.exhappy_nons_cred),
        ("Neutral, Severe - App", clms.neutral_s_app),
        ("Neutral, Severe - Cred", clms.neutral_s_cred),
        ("Happy, Severe - App", clms.happy_s_app),
        ("Happy, Severe - Cred", clms.happy_s_cred),
        ("ExHappy, Severe - App", clms.exhappy_s_app),
        ("ExHappy, Severe - Cred", clms.exhappy_s_cred)]

    print("\nIndividual Cronbach's alpha: ")

    for name, cols in alpha_tests:
        alpha, ci = pg.cronbach_alpha(df[cols])
        print(f"{name:<30} α = {alpha:.3f}, 95% CI = [{ci[0]:.3f}, {ci[1]:.3f}]")
    print("\nOverall Cronbach's alpha: ")

    cols_app = (clms.neutral_nons_app + clms.happy_nons_app + clms.exhappy_nons_app 
                + clms.neutral_s_app + clms.happy_s_app + clms.exhappy_s_app)
    cols_cred = (clms.neutral_nons_cred + clms.happy_nons_cred + clms.exhappy_nons_cred 
                 + clms.neutral_s_cred + clms.happy_s_cred + clms.exhappy_s_cred)
    alpha_app, ci_app = pg.cronbach_alpha(df[cols_app])
    alpha_cred, ci_cred = pg.cronbach_alpha(df[cols_cred])

    print(f"Perceived Social Appropriateness  α = {alpha_app:.3f}, 95% CI = [{ci_app[0]:.3f}, {ci_app[1]:.3f}]")

    print(f"Perceived Credibility             α = {alpha_cred:.3f}, 95% CI = [{ci_cred[0]:.3f}, {ci_cred[1]:.3f}]")

    print("\n===========================================================\n")


    # demographic checking

    print(df[clms.demographic])


    # ---------------------

    print("\n\n**************** PERCEIVED SOCIAL APPROPRIATENESS ANALYSIS ****************")

    # first analysis
    # creating mean scores for perceived social appropriateness analysis

    df["Neutral_NS_Appropriateness"] = df[clms.neutral_nons_app].mean(axis=1)
    df["Happy_NS_Appropriateness"] = df[clms.happy_nons_app].mean(axis=1)
    df["ExHappy_NS_Appropriateness"] = df[clms.exhappy_nons_app].mean(axis=1)

    df["Neutral_S_Appropriateness"] = df[clms.neutral_s_app].mean(axis=1)
    df["Happy_S_Appropriateness"] = df[clms.happy_s_app].mean(axis=1)
    df["ExHappy_S_Appropriateness"] = df[clms.exhappy_s_app].mean(axis=1)

    # converting to long format to use with RM ANOVA and mixed models

    long_df_app = pd.DataFrame()

    conditions_app = [
        ("Neutral_NS_Appropriateness","Neutral","NonSevere"),
        ("Happy_NS_Appropriateness","Happy","NonSevere"),
        ("ExHappy_NS_Appropriateness","ExtremelyHappy","NonSevere"),
        ("Neutral_S_Appropriateness","Neutral","Severe"),
        ("Happy_S_Appropriateness","Happy","Severe"),
        ("ExHappy_S_Appropriateness","ExtremelyHappy","Severe")
    ]

    for score, emotion, severity in conditions_app:

        temp = pd.DataFrame({
            "Participant": df.index,
            "Appropriateness": df[score],
            "Emotion": emotion,
            "Severity": severity,

            "Age": df["Age"],
            "Gender": df["Gender"],
            "Education": df["Level Education"],
            "TechComfort": df["Comf. Tech_1"],
            "UsedAssistant": df["Used Assistant"],
            "Familiarity": df["Familiarity_1"],
            
            "BaselineMood": df["Baseline Mood"]})

        long_df_app = pd.concat([long_df_app, temp], ignore_index=True)

    
    # Repeated Measures Anova

    print ("\n Repeated Measures ANOVA")
    anova_app = pg.rm_anova(
        data=long_df_app,
        dv="Appropriateness",
        within=["Emotion", "Severity"],
        subject="Participant",
        detailed=True)

    print(anova_app[["Source", "ddof1", "ddof2", "F", "p_GG_corr","ng2"]])

    
    # Mixed Model

    model_app = smf.mixedlm(
        "Appropriateness ~ Emotion * Severity + Age + Gender + Education + TechComfort + Familiarity + BaselineMood",
        data=long_df_app,
        groups=long_df_app["Participant"]
    )

    print(model_app.fit().summary())


    # ---------------------

    print("\n\n********************* PERCEIVED CREDIBILITY ANALYSIS *********************")

    # second analysis
    # creating mean scores for perceived credibility analysis


    df["Neutral_NS_Credibility"] = df[clms.neutral_nons_cred].mean(axis=1)
    df["Happy_NS_Credibility"] = df[clms.happy_nons_cred].mean(axis=1)
    df["ExHappy_NS_Credibility"] = df[clms.exhappy_nons_cred].mean(axis=1)

    df["Neutral_S_Credibility"] = df[clms.neutral_s_cred].mean(axis=1)
    df["Happy_S_Credibility"] = df[clms.happy_s_cred].mean(axis=1)
    df["ExHappy_S_Credibility"] = df[clms.exhappy_s_cred].mean(axis=1)


    # converting to long format

    long_df_cred = pd.DataFrame()

    conditions_cred = [
        ("Neutral_NS_Credibility","Neutral","NonSevere"),
        ("Happy_NS_Credibility","Happy","NonSevere"),
        ("ExHappy_NS_Credibility","ExtremelyHappy","NonSevere"),
        ("Neutral_S_Credibility","Neutral","Severe"),
        ("Happy_S_Credibility","Happy","Severe"),
        ("ExHappy_S_Credibility","ExtremelyHappy","Severe")]

    for score, emotion, severity in conditions_cred:

        temp = pd.DataFrame({
            "Participant": df.index,
            "Credibility": df[score],
            "Emotion": emotion,
            "Severity": severity,

            "Age": df["Age"],
            "Gender": df["Gender"],
            "Education": df["Level Education"],
            "TechComfort": df["Comf. Tech_1"],
            "UsedAssistant": df["Used Assistant"],
            "Familiarity": df["Familiarity_1"],
            
            "BaselineMood": df["Baseline Mood"]})

        long_df_cred = pd.concat([long_df_cred, temp], ignore_index=True)

    
    # Repeated Measures ANOVA

    print ("\n Repeated Measures ANOVA")
    anova_cred = pg.rm_anova(
        data=long_df_cred,
        dv="Credibility",
        within=["Emotion", "Severity"],
        subject="Participant",
        detailed=True)

    print(anova_cred[["Source", "ddof1", "ddof2", "F", "p_GG_corr","ng2"]])

    
    # Mixed Model

    model_cred = smf.mixedlm(

        "Credibility ~ Emotion * Severity + Age + Gender + Education + TechComfort + Familiarity + BaselineMood",
        data=long_df_cred,
        groups=long_df_cred["Participant"]
    )
    print(model_cred.fit().summary())


# Without this I wil get 'I/O operation on closed file' error
sys.stdout = original_stdout
print(f"Results saved to: {output_path}")