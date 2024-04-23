import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv("./dataset/nasa.csv")

# Basic info
#print(data.info())

# Explore 'Hazardous' class distribution
print(data['Hazardous'].value_counts())

# Visualizing data distributions
sns.histplot(data['Relative Velocity km per hr'], kde=True)
plt.title('Distribution of Relative Velocity (km/hr)')
plt.show()
