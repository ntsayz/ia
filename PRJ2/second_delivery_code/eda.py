import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
file_path = '../dataset/processed_dataset.csv'
data = pd.read_csv(file_path)

# Convert date columns to numeric
data['Close Approach Date'] = pd.to_datetime(data['Close Approach Date'], errors='coerce').astype(int) / 10**9
data['Orbit Determination Date'] = pd.to_datetime(data['Orbit Determination Date'], errors='coerce').astype(int) / 10**9

# Convert all columns to numeric, coercing errors to NaN
data = data.apply(pd.to_numeric, errors='coerce')

# Drop rows with any NaN values
data = data.dropna()

# Class distribution
plt.figure(figsize=(8, 6))
sns.countplot(x='Hazardous', data=data)
plt.title('Class Distribution')
plt.xlabel('Hazardous')
plt.ylabel('Count')
plt.show()

# Remove date-related columns for descriptive statistics
columns_to_exclude = ['Close Approach Date', 'Epoch Date Close Approach', 'Orbit Determination Date', 'Perihelion Time', 'Neo Reference ID', 'Epoch Osculation']
data_for_stats = data.drop(columns=columns_to_exclude)

# Descriptive statistics
descriptive_stats = data_for_stats.describe().transpose()
plt.figure(figsize=(14, 8))
sns.heatmap(descriptive_stats, annot=True, fmt='.2f', cmap='viridis', cbar=True)
plt.title('Descriptive Statistics')
plt.show()

# Correlation matrix
correlation_matrix = data.corr()
plt.figure(figsize=(14, 12))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', cbar=True)
plt.title('Correlation Matrix')
plt.show()

# Pairplot for a subset of features
sns.pairplot(data[['Absolute Magnitude', 'Est Dia in KM(min)', 'Relative Velocity km per sec', 'Miss Dist.(Astronomical)', 'Hazardous']], hue='Hazardous')
plt.show()
