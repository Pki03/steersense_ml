import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load data
df = pd.read_csv("realistic_drowsiness_mock.csv")

# Features and label
X = df[["EAR", "MOR", "neck_tilt"]]
y = df["label"]

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)  # not_drowsy → 0, drowsy → 1

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Define models
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Support Vector Machine": SVC(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "KNN": KNeighborsClassifier()
}

# Train & evaluate
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

    if acc > best_accuracy:
        best_model = model
        best_accuracy = acc

# Save best model
joblib.dump(best_model, "drowsiness_detector.pkl")
joblib.dump(le, "drowsiness_label_encoder.pkl")

print(f"\n🎉 Best model ({best_model.__class__.__name__}) saved with accuracy: {round(best_accuracy * 100, 2)}%")
