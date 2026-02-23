import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

from ..config import BASE_DIR, DATASET_PATH, MODEL_PATH, VECTORIZER_PATH, ensure_project_dirs


def _load_training_data() -> pd.DataFrame:
    dataset_files = [
        (BASE_DIR / "FakeNewsNet" / "dataset" / "gossipcop_fake.csv", 1),
        (BASE_DIR / "FakeNewsNet" / "dataset" / "gossipcop_real.csv", 0),
        (BASE_DIR / "FakeNewsNet" / "dataset" / "politifact_fake.csv", 1),
        (BASE_DIR / "FakeNewsNet" / "dataset" / "politifact_real.csv", 0),
    ]

    rows = []
    for file_path, label in dataset_files:
        try:
            dataframe = pd.read_csv(file_path, usecols=["title"])
            dataframe = dataframe.rename(columns={"title": "texte"})
            dataframe["valeur"] = label
            rows.append(dataframe)
        except Exception:
            continue

    if rows:
        merged = pd.concat(rows, ignore_index=True)
        merged = merged.dropna(subset=["texte"])
        merged["texte"] = merged["texte"].astype(str).str.strip()
        merged = merged[merged["texte"] != ""]
        return merged[["texte", "valeur"]]

    data = pd.read_excel(DATASET_PATH)
    return data[["texte", "valeur"]]


def train_model() -> None:
    ensure_project_dirs()

    print("Loading dataset...")
    data = _load_training_data()
    x_values = data["texte"]
    y_values = data["valeur"]

    print("Splitting data and vectorizing...")
    x_train, x_test, y_train, y_test = train_test_split(
        x_values, y_values, test_size=0.2, random_state=42, stratify=y_values
    )
    vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), min_df=2)
    x_train_vec = vectorizer.fit_transform(x_train)
    x_test_vec = vectorizer.transform(x_test)
    print(f"Training samples: {len(x_train)}, Test samples: {len(x_test)}")

    print("Training model...")
    model = LogisticRegression(class_weight="balanced", max_iter=200)
    model.fit(x_train_vec, y_train)

    print("Evaluating model...")
    y_pred = model.predict(x_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("Saving model and vectorizer...")
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print("Model and vectorizer saved successfully!")


if __name__ == "__main__":
    train_model()
