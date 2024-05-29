import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned dataset
file_path = '../dataset/processed_dataset.csv'
data = pd.read_csv(file_path)

# Convert date columns to timestamps (in seconds)
data['Close Approach Date'] = pd.to_datetime(data['Close Approach Date']).astype(int) / 10**9
data['Orbit Determination Date'] = pd.to_datetime(data['Orbit Determination Date']).astype(int) / 10**9

# Convert all columns to numeric, coercing errors to NaN
data = data.apply(pd.to_numeric, errors='coerce')

# Drop rows with any NaN values (optional: handle NaN values differently if needed)
data = data.dropna()

# Compute the correlation matrix
correlation_matrix = data.corr()

# Plot the correlation matrix
plt.figure(figsize=(14, 12))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', cbar=True)
plt.title('Correlation Matrix')
plt.show()

# Identify highly correlated features with the target variable 'Hazardous'
target_correlation = correlation_matrix['Hazardous'].abs().sort_values(ascending=False)
print("Correlation with target variable 'Hazardous':\n", target_correlation)

# Select features with a high correlation (e.g., > 0.8)
high_correlation_features = target_correlation[target_correlation > 0.8].index
print("Features with high correlation to 'Hazardous':\n", high_correlation_features)
