import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from feature_extraction import extract_features

# Load dataset
data = pd.read_csv("dataset/phishing.csv")

# Clean dataset
data = data.dropna(subset=["url", "label"])
data["url"] = data["url"].astype(str)
data["label"] = pd.to_numeric(data["label"], errors="coerce")
data = data.dropna()

X = []
y = []

expected_len = None  # we will detect it automatically

for url, label in zip(data["url"], data["label"]):
    features = extract_features(url)

    if isinstance(features, list):
        if expected_len is None:
            expected_len = len(features)
            print("Detected feature count:", expected_len)

        if len(features) == expected_len:
            X.append(features)
            y.append(int(label))

# Convert to NumPy arrays
X = np.array(X, dtype=float)
y = np.array(y)

print("Final feature matrix shape:", X.shape)

# 🚨 SAFETY CHECK
if X.shape[0] == 0:
    raise ValueError("No valid samples found. Check feature extraction or CSV.")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model/phishing_model.pkl")

print("✅ Model trained successfully.")
