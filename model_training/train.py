
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib


def train_model():
    df = pd.read_csv("processes_data.csv")

    features = ["burst_time", "io_frequency", "memory_usage"]
    target   = "process_type"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = DecisionTreeClassifier(max_depth=6, random_state=42)
    model.fit(X_train, y_train)

    y_pred   = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n[OK] Model trained successfully!")
    print(f"    Test Accuracy : {accuracy * 100:.2f}%")
    print(f"\n--- Classification Report ---")
    print(classification_report(y_test, y_pred, target_names=["CPU-bound", "I/O-bound"]))

    joblib.dump(model, "scheduler_model.pkl")
    print("[OK] Model saved -> scheduler_model.pkl")


if __name__ == "__main__":
    train_model()
