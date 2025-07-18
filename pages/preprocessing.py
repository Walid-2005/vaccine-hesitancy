"""
Data preprocessing module for survey response normalization.

This module contains functions to transform raw survey response data into a
numerical format suitable for machine learning models. It includes:

- Categorical encoding (e.g., age groups, education levels)
- Manual one-hot encoding for demographic variables
- Type coercion and cleanup
"""

import pandas as pd

def preprocess_data(responses_df):
    """
    Preprocess survey responses before feeding into the prediction model.

    Args:
        responses_df (pd.DataFrame): Raw survey data including categorical variables.

    Returns:
        pd.DataFrame: Processed DataFrame with numeric and one-hot encoded columns.
    """

    # ---------------------------
    # 1. Age Group Mapping
    # ---------------------------
    age_mapping = {"<20": 1, "20-30": 2, "30-50": 3, ">50": 4}
    responses_df["age"] = responses_df["age"].map(age_mapping)

    # ---------------------------
    # 2. Normalize Number of Children
    # Convert ">2" to numeric 3
    # ---------------------------
    responses_df["no_of_children"] = responses_df["no_of_children"].replace(">2", 3)

    # ---------------------------
    # 3. Encode Education Levels
    # Ordinal mapping from lowest to highest education
    # ---------------------------
    qualification_order = {
        "Primary/Secondary": 0,
        "Tertiary Education": 1,
        "Higher Secondary": 2,
        "Higher Education": 3
    }
    responses_df["qualification"] = responses_df["qualification"].map(qualification_order)

    # ---------------------------
    # 4. One-hot Encoding for Demographics
    # Manually define expected binary features
    # ---------------------------
    expected_columns = [
        "Marital Status_Unmarried", "Sex_Male", "Sex_Others", "Place_Urban",
        "Job_Clerical Job", "Job_Daily earners", "Job_Housewife",
        "Job_Professional (Eg. Teachers, Engineers, Dr. Pharmacist etc)", "Job_Student"
    ]

    # Initialize all one-hot columns to 0
    for col in expected_columns:
        responses_df[col] = 0

    # Set correct one-hot flags based on conditions
    responses_df.loc[responses_df["marital_status"] == "Unmarried", "Marital Status_Unmarried"] = 1
    responses_df.loc[responses_df["sex"] == "Male", "Sex_Male"] = 1
    responses_df.loc[responses_df["sex"] == "Others", "Sex_Others"] = 1
    responses_df.loc[responses_df["place"] == "Urban", "Place_Urban"] = 1

    # Map job category strings to one-hot columns
    job_mapping = {
        "Clerical Job": "Job_Clerical Job",
        "Daily earners": "Job_Daily earners",
        "Housewife": "Job_Housewife",
        "Professional (Eg. Teachers, Engineers, Dr. Pharmacist etc)": "Job_Professional (Eg. Teachers, Engineers, Dr. Pharmacist etc)",
        "Student": "Job_Student"
    }

    for job, column in job_mapping.items():
        responses_df.loc[responses_df["job"] == job, column] = 1

    # ---------------------------
    # 5. Drop original categorical columns
    # ---------------------------
    responses_df.drop(columns=["marital_status", "sex", "place", "job"], inplace=True)

    # ---------------------------
    # 6. Convert all columns to numeric (handles any leftover non-numeric entries)
    # ---------------------------
    responses_df = responses_df.apply(pd.to_numeric, errors='coerce')

    return responses_df
