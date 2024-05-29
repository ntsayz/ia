import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt
import seaborn as sns
import time


print("Loading dataset...")
file_path = '../dataset/processed_dataset.csv'
data = pd.read_csv(file_path)

print("Processing date columns...")
data['Close Approach Date'] = pd.to_datetime(data['Close Approach Date']).astype(int) / 10**9
data['Orbit Determination Date'] = pd.to_datetime(data['Orbit Determination Date']).astype(int) / 10**9

print("Converting all columns to numeric and handling NaNs...")
data = data.apply(pd.to_numeric, errors='coerce')

data = data.dropna()

features_to_remove = ['Orbit Uncertainity', 'Absolute Magnitude', 'Minimum Orbit Intersection', 'Perihelion Distance']
# data = data.drop(columns=features_to_remove)  # added this bc of RF overperforming


print("Splitting data into features and target variable...")
X = data.drop('Hazardous', axis=1) 
y = data['Hazardous']  # target variable

# Feature scaling
print("Scaling features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


print("Applying PCA...")
pca = PCA(n_components=0.95)  # 95% of variance
X_pca = pca.fit_transform(X_scaled)


print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.4, random_state=42, stratify=y)


print("Initializing models...")
models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    'SVM (rbf)': SVC(kernel='rbf', probability=True, random_state=42),
    'K-NN': KNeighborsClassifier(n_neighbors=5),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Neural Network': MLPClassifier(random_state=42, max_iter=1000)
}



# train and evaluate models
print("Training and evaluating models...")
results = {}
for model_name, model in models.items():
    print(f"Training {model_name}...")
    start_time = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - start_time

    print(f"Evaluating {model_name}...")
    y_pred = model.predict(X_test)
    y_scores = model.decision_function(X_test) if 'SVM' in model_name else model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    fpr, tpr, _ = roc_curve(y_test, y_scores)
    roc_auc = auc(fpr, tpr)
    prec, rec, _ = precision_recall_curve(y_test, y_scores)

    results[model_name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm,
        'roc_auc': roc_auc,
        'precision_recall_curve': (prec, rec),
        'train_time': train_time,
        'y_scores': y_scores  
    }

# Display results
print("Displaying results...")
for model_name, metrics in results.items():
    print(f"Model: {model_name}")
    print(f"Accuracy: {metrics['accuracy']}")
    print(f"Precision: {metrics['precision']}")
    print(f"Recall: {metrics['recall']}")
    print(f"F1 Score: {metrics['f1']}")
    print(f"Training Time: {metrics['train_time']} seconds")
    print("Confusion Matrix:\n", metrics['confusion_matrix'])
    print("=====================================================================")




print("Plotting ROC and Precision-Recall Curves...")
plt.figure(figsize=(8, 6))
for model_name, metrics in results.items():
    fpr, tpr, _ = roc_curve(y_test, metrics['y_scores'])
    plt.plot(fpr, tpr, label=f'{model_name} (AUC = {metrics["roc_auc"]:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

plt.figure(figsize=(8, 6))
for model_name, metrics in results.items():
    prec, rec, _ = precision_recall_curve(y_test, metrics['y_scores'])
    plt.plot(rec, prec, label=model_name)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.legend(loc="lower left")
plt.show()



print("Plotting Training Time Bar Plot...")
model_names = list(results.keys())
train_times = [metrics['train_time'] for metrics in results.values()]

plt.figure(figsize=(10, 6))
sns.barplot(x=model_names, y=train_times)
plt.xlabel('Model')
plt.ylabel('Training Time (seconds)')
plt.title('Training Time for Different Models')
plt.xticks(rotation=45)
plt.show()



for model_name, metrics in results.items():
    plt.figure(figsize=(8, 6))
    sns.heatmap(metrics['confusion_matrix'], annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix for {model_name}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()
