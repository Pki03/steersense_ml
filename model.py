import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load data
df = pd.read_csv("realistic_stress_mock.csv")

# ---------- FEATURE ENGINEERING ----------
# Compute derived features
df["accel_magnitude"] = np.sqrt(df["accel_x"]**2 + df["accel_y"]**2 + df["accel_z"]**2)
df["accel_std_dev_xy"] = df[["accel_x", "accel_y"]].std(axis=1)

# Optional: drop columns not needed for training
X = df.drop(columns=["timestamp", "label", "subject_id"])  # Drop subject_id if not using personalization
y = df["label"]

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Define models
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Support Vector Machine": SVC(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "KNN": KNeighborsClassifier()
}

# Evaluate all models
best_model = None
best_accuracy = 0.0

for name, model in models.items():
    print(f"\n🚀 Training: {name}")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {round(acc * 100, 2)}%")
    print("📊 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Save best model
    if acc > best_accuracy:
        best_model = model
        best_accuracy = acc

# Save the best model
joblib.dump(best_model, "stress_detector_model.pkl")
joblib.dump(le, "label_encoder.pkl")
print(f"\n🎉 Best model ({best_model.__class__.__name__}) saved with accuracy: {round(best_accuracy * 100, 2)}%")
