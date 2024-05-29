import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

source_folder = '../dataset/'
dest_folder = '../dataset/training/'
dest_folder_test = '../dataset/testing/'
# Load the dataset
data = pd.read_csv(source_folder + 'processed_dataset.csv')


# converting dates to a processable format or extract useful components
data['Close Approach Date'] = pd.to_datetime(data['Close Approach Date']).astype(int) / 10**9
data['Orbit Determination Date'] = pd.to_datetime(data['Orbit Determination Date']).astype(int) / 10**9

# features and the target variable
X = data.drop('Hazardous', axis=1)  # Features
y = data['Hazardous']  # Target variable
start_time = time.time()
# Splitting the data into a 70% training set and a 30% testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Random Forest to determine feature importance
forest = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
print("Starting model training...")
forest.fit(X_train, y_train)
print(f"Model trained. Duration: {time.time() - start_time:.2f} seconds")



# Get feature importances
importances = forest.feature_importances_
indices = np.argsort(importances)[::-1]
print(f"Feature Importance Operation took {time.time() - start_time} seconds")
# Print the feature ranking
print("Feature ranking:")
for f in range(X_train.shape[1]):
    print(f"{f + 1}. feature {X_train.columns[indices[f]]} ({importances[indices[f]]})")


# Plot the feature importances of the forest
plt.figure(figsize=(12, 8))
plt.title("Feature importances")
sns.barplot(x=importances[indices], y=X_train.columns[indices], orient='h')
plt.xlabel('Relative Importance')
plt.show()


# model with the selected features only
sfm = SelectFromModel(forest, threshold='median') 
sfm.fit(X_train, y_train)
selected_features = X_train.columns[sfm.get_support()]

print("Selected features based on importance threshold:", selected_features)

# Saving the reduced feature sets
print("Transforming training and testing datasets...")
X_train_reduced = sfm.transform(X_train)
X_test_reduced = sfm.transform(X_test)
print(f"Model Select Operation took {time.time() - start_time} seconds")
# Save the splits into new CSV files

print("Saving transformed datasets to CSV files...")
pd.DataFrame(X_train_reduced, columns=selected_features).to_csv( dest_folder + 'train_features_reduced.csv', index=False)
pd.DataFrame(y_train).to_csv(dest_folder + 'train_labels.csv', index=False)
pd.DataFrame(X_test_reduced, columns=selected_features).to_csv(dest_folder_test + 'test_features_reduced.csv', index=False)
pd.DataFrame(y_test).to_csv(dest_folder_test + 'test_labels.csv', index=False)


print(f"All processes completed. Total duration: {time.time() - start_time:.2f} seconds")