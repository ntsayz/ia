import pandas as pd
import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, learning_curve
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
train_features = pd.read_csv('../dataset/training/train_features_reduced.csv')
train_labels = pd.read_csv('../dataset/training/train_labels.csv')
test_features = pd.read_csv('../dataset/testing/test_features_reduced.csv')
# =========================================================================
# ran into an issue so i had to add this line
non_numeric = test_features.applymap(np.isreal).all(0)
print("Non-numeric columns:", test_features.columns[~non_numeric])

# convert all columns to numeric, coercing errors to NaN
test_features = test_features.apply(pd.to_numeric, errors='coerce')

# handling missing values after coercion
test_features.fillna(test_features.mean(), inplace=True)


test_features.to_csv('../dataset/testing/test_features_reduced_clean.csv', index=False)
test_features_clean = pd.read_csv('../dataset/testing/test_features_reduced_clean.csv')

# =========================================================================
test_labels = pd.read_csv('../dataset/testing/test_labels.csv')


y_train = train_labels.iloc[:, 0]
y_test = test_labels.iloc[:, 0]


forest = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)

# Start model validation via cross-validation
start_time = time.time()
cv_scores = cross_val_score(forest, train_features, y_train, cv=5)
print("Cross-validation accuracy scores:", cv_scores)
print("Mean CV accuracy:", cv_scores.mean())

# Hyperparameter tuning using Grid Search
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_features': ['sqrt', 'log2'],  
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=forest, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(train_features, y_train)
print("Best parameters found:", grid_search.best_params_)

# Re-training using best parameters
best_forest = grid_search.best_estimator_
best_forest.fit(train_features, y_train)

# Eval on test set
y_pred = best_forest.predict(test_features_clean)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)


print("=====================================================================")
print("Cross-validation accuracy scores:", cv_scores)
print("Mean CV accuracy:", cv_scores.mean())
print("=====================================================================")
print("Test Set Evaluation Metrics:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("=====================================================================")
print("Confusion Matrix:\n", cm)
print("=====================================================================")
print(f"Total time taken: {time.time() - start_time:.2f} seconds")






# ===================================================== PLOTTING =================================================================
# Feature Importance
importances = best_forest.feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(12, 8))
plt.title("Feature Importances")
sns.barplot(x=importances[indices], y=train_features.columns[indices], orient='h')
plt.xlabel('Relative Importance')

plt.show()

# Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

# ROC Curve

y_scores = best_forest.predict_proba(test_features_clean)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_scores)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()


# Precision-Recall Curve

precision, recall, thresholds = precision_recall_curve(y_test, y_scores)

plt.figure(figsize=(8, 6))
plt.plot(recall, precision, color='purple', lw=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.show()

# Learning Curve

train_sizes, train_scores, test_scores = learning_curve(
    best_forest, train_features, y_train, cv=3, train_sizes=np.linspace(0.1, 1.0, 5))

train_scores_mean = np.mean(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)

plt.figure(figsize=(8, 6))
plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation score")
plt.xlabel('Training examples')
plt.ylabel('Score')
plt.title('Learning Curves')
plt.legend(loc="best")
plt.show()

