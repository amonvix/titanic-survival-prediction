# scripts/analyze_dataset.py

import pandas as pd

# Load dataset
df = pd.read_csv('data/titanic.csv')

# Dataset dimensions
print(f"Shape (rows, columns): {df.shape}\n")

# Dataset info and data types
print("Dataset info:")
print(df.info(), "\n")

# Descriptive statistics (numerical columns only)
print("Descriptive statistics:")
print(df.describe(), "\n")

# Count of missing values per column
print("Missing values per column:")
print(df.isnull().sum())
