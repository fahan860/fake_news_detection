import joblib

from ..config import BASE_DIR, MODEL_PATH, VECTORIZER_PATH
from ..utils.file_utils import resolve_with_legacy


_MODEL = None
_VECTORIZER = None
_LOAD_ATTEMPTED = False


def _get_model_and_vectorizer():
    global _MODEL, _VECTORIZER, _LOAD_ATTEMPTED

    if _MODEL is not None and _VECTORIZER is not None:
        return _MODEL, _VECTORIZER

    if _LOAD_ATTEMPTED:
        return None, None

    _LOAD_ATTEMPTED = True

    model_path = resolve_with_legacy(MODEL_PATH, BASE_DIR / "fake_news_model.pkl")
    vectorizer_path = resolve_with_legacy(VECTORIZER_PATH, BASE_DIR / "tfidf_vectorizer.pkl")

    if model_path is None or vectorizer_path is None:
        return None, None

    _MODEL = joblib.load(model_path)
    _VECTORIZER = joblib.load(vectorizer_path)
    return _MODEL, _VECTORIZER


def predict_fake_news(text: str):
    model, vectorizer = _get_model_and_vectorizer()
    if model is None or vectorizer is None:
        return "Model not found", 0.0

    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    confidence = model.predict_proba(text_vectorized)[0][prediction] * 100

    label = "Fake" if prediction == 1 else "Real"
    return label, float(round(confidence, 2))
