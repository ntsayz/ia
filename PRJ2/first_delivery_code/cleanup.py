import pandas as pd

# Load the dataset
file_path = '../dataset/nasa.csv'
data = pd.read_csv(file_path)

# Print the original data shape
print("Original data shape:", data.shape)

# removing unnecessary or repeated att
# dropping all imperial and redundant metric measurements, keeping KM and AU
cols_to_drop = [
    'Est Dia in M(min)', 'Est Dia in M(max)', 
    'Est Dia in Miles(min)', 'Est Dia in Miles(max)', 
    'Est Dia in Feet(min)', 'Est Dia in Feet(max)', 
    'Name',  # 'Name' is the same as 'Neo Reference ID'
    'Relative Velocity km per hr', 'Miles per hour',  # redundant with 'Relative Velocity km per sec'
    'Miss Dist.(lunar)', 'Miss Dist.(kilometers)', 'Miss Dist.(miles)',  # keep Astronomical units only
    'Orbiting Body','Equinox'  # all entries are 'Earth' and 'J200', no variation
]

data.drop(columns=cols_to_drop, inplace=True)

print("Missing values per column:\n", data.isnull().sum())




cleaned_data_path = '../dataset/processed_dataset.csv'
data.to_csv(cleaned_data_path, index=False)


print("Cleaned data shape:", data.shape)
print("Data cleanup complete and saved to", cleaned_data_path)
