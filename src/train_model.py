import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

DATA_FILE = "data/processed/timeline_15_features.csv"

df = pd.read_csv(DATA_FILE)

df = df[df["team_id"] == 100]

X = df[
    [
        "gold_diff_15",
        "xp_diff_15",
        "cs_diff_15"
    ]
]

y = df["win"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
}

for model_name, model in models.items():
    print()
    print("=" * 40)
    print(model_name)
    print("=" * 40)

    model.fit(X_train, y_train)

    print()

    if hasattr(model, "coef_"):
        print("Coefficients:")
        for feature, coefficient in zip(X.columns, model.coef_[0]):
            print(f"{feature}: {coefficient:.4f}")

    elif hasattr(model, "feature_importances_"):
        print("Feature Importances:")
        for feature, importance in zip(X.columns, model.feature_importances_):
            print(f"{feature}: {importance:.4f}")

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("Accuracy:", accuracy)

    print()
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    print()
    print("Classification Report:")
    print(classification_report(y_test, predictions))

    
