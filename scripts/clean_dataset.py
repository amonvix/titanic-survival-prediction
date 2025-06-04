# scripts/clean_dataset.py

import pandas as pd

# Load raw dataset
df = pd.read_csv('data/titanic.csv')

# Drop columns with too many missing values
df.drop(columns=['deck'], inplace=True)

# Fill missing values (safe assignment)
df['age'] = df['age'].fillna(df['age'].median())
df['embarked'] = df['embarked'].fillna(df['embarked'].mode()[0])
df['embark_town'] = df['embark_town'].fillna(df['embark_town'].mode()[0])

# Convert categorical columns to numeric
df['sex'] = df['sex'].map({'male': 0, 'female': 1})
df['embarked'] = df['embarked'].map({'C': 0, 'Q': 1, 'S': 2})

# Save cleaned dataset
df.to_csv('data/titanic_clean.csv', index=False)

print("✅ Cleaned dataset saved to: data/titanic_clean.csv")
