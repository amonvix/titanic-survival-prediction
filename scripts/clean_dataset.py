# scripts/clean_dataset.py

import pandas as pd

# Load raw dataset
df = pd.read_csv('data/titanic.csv')

print("\n📋 Column data types:")
print(df.dtypes)

# Drop columns with too many missing values
df.drop(columns=['deck'], inplace=True)

# Fill missing values (safe assignment)
df['age'] = df['age'].fillna(df['age'].median())
df['embarked'] = df['embarked'].fillna(df['embarked'].mode()[0])
df['embark_town'] = df['embark_town'].fillna(df['embark_town'].mode()[0])

# Convert categorical columns to numeric
df['sex'] = df['sex'].map({'male': 0, 'female': 1})
df['embarked'] = df['embarked'].map({'C': 0, 'Q': 1, 'S': 2})

# Encode 'alive' column to numeric
df['alive'] = df['alive'].map({'no': 0, 'yes': 1})

# Map passenger class to numeric (1 = First, 2 = Second, 3 = Third)
df['class'] = df['class'].map({'First': 1, 'Second': 2, 'Third': 3})

# Encode 'who' column to numeric
df['who'] = df['who'].map({'man': 0, 'woman': 1, 'child': 2})

# Encode 'embark_town' to numeric
df['embark_town'] = df['embark_town'].map({
    'Southampton': 0,
    'Cherbourg': 1,
    'Queenstown': 2
})

# Save cleaned dataset
df.to_csv('data/titanic_clean.csv', index=False)

print("✅ Cleaned dataset saved to: data/titanic_clean.csv")

# Final check for non-numeric columns
non_numeric = df.select_dtypes(include='object').columns
if len(non_numeric):
    print("⚠️ Non-numeric columns remaining:", list(non_numeric))
else:
    print("✅ All columns are numeric. Ready for model training.")
