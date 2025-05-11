import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("chandigarh_routes.csv")

# Function to fill missing values
def fill_missing_randomly(df):
    df_filled = df.copy()
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                df_filled[col] = df[col].apply(
                    lambda x: np.random.choice(df[col].dropna()) if pd.isnull(x) else x
                )
            elif np.issubdtype(df[col].dtype, np.number):
                mean = df[col].mean()
                std = df[col].std()
                df_filled[col] = df[col].apply(
                    lambda x: np.random.normal(mean, std) if pd.isnull(x) else x
                )
            else:
                print(f"Skipping column '{col}' with unsupported type: {df[col].dtype}")
    return df_filled

# Fill the missing values
df_filled = fill_missing_randomly(df)

# Save the filled dataset
df_filled.to_csv("data/final_routes_dataset_filled.csv", index=False)
print("Missing values filled and saved to 'final_routes_dataset_filled.csv'")
