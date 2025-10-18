# scripts/load_dataset.py

import seaborn as sns


# Load Titanic dataset from Seaborn
df = sns.load_dataset('titanic')

# Save dataset as CSV in the 'data' folder
df.to_csv('data/titanic.csv', index=False)

# Preview first 5 rows
print("Initial dataset preview:")
print(df.head())
