import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv("C:\\Users\\USER\\Downloads\\mobile_usage_uncleaned.csv")

print("Original Dataset Shape:", df.shape)
print("\nMissing Values:")
print(df.isnull().sum())

# ============= CLEANING =============

# 1. Remove complete duplicates
df = df.drop_duplicates()

# 2. Handle missing values in numeric columns (fill with mean)
numeric_cols = ['Age', 'Screen_Time_Hours', 'Sleep_Hours', 'Social_Media_Hours', 'Battery_Usage_%']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col].fillna(df[col].mean(), inplace=True)

# 3. Handle missing values in categorical columns (fill with mode)
categorical_cols = ['Gender', 'Department', 'Most_Used_App']
for col in categorical_cols:
    df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown', inplace=True)

# 4. Standardize Gender values
df['Gender'] = df['Gender'].map({'M': 'Male', 'F': 'Female', 'Male': 'Male', 'Female': 'Female'})
df['Gender'].fillna('Unknown', inplace=True)

# 5. Standardize Department (remove empty values)
df['Department'] = df['Department'].fillna('Unknown')
df['Department'] = df['Department'].str.strip().replace('', 'Unknown')

# 6. Remove outliers (optional - using IQR method for Screen_Time_Hours)
Q1 = df['Screen_Time_Hours'].quantile(0.25)
Q3 = df['Screen_Time_Hours'].quantile(0.75)
IQR = Q3 - Q1
df = df[~((df['Screen_Time_Hours'] < Q1 - 1.5*IQR) | (df['Screen_Time_Hours'] > Q3 + 1.5*IQR))]

# 7. Round numeric columns to 2 decimal places
for col in numeric_cols:
    df[col] = df[col].round(2)

print("\n\nCleaned Dataset Shape:", df.shape)
print("Missing Values After Cleaning:")
print(df.isnull().sum())
print("\nCleaned Data Sample:")
print(df.head())

# Save cleaned data
df.to_csv('mobile_usage_cleaned.csv', index=False)
print("\n✓ Cleaned data saved to 'mobile_usage_cleaned.csv'")