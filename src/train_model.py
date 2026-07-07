import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

DATA_FILE = "data/processed/team_features.csv"

df = pd.read_csv(DATA_FILE)

df = df[df["team_id"] == 100]

X = df[
    [
        "gold_diff",
        "kill_diff",
        "cs_diff",
        "vision_diff"
    ]
]

y = df["win"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)

accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

print()
print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions))

print()
print("Classification Report:")
print(classification_report(y_test, predictions))

print()
print("Feature Importance (Coefficients):")
for feature, coefficient in zip(X.columns, model.coef_[0]):
    print(f"{feature}: {coefficient:.4f}")

print()
print("Actual vs Predicted:")
for actual, prediction, probability in zip(y_test, predictions, probabilities):
    print(
        f"Actual: {actual} | "
        f"Predicted: {prediction} | "
        f"Win Probability: {probability[1]:.2%}"
    )