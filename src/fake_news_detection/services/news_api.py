import requests

from ..config import NEWS_API_KEY, NEWS_API_URL


def fetch_scored_news(query: str, score_fn):
    if not NEWS_API_KEY:
        return None, "NEWS_API_KEY is not configured"

    params = {
        "q": query,
        "apiKey": NEWS_API_KEY,
        "pageSize": 10,
        "language": "en",
    }
    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=20)
    except requests.RequestException as exc:
        return None, f"News API request failed: {exc}"

    if response.status_code != 200:
        return None, f"News API error {response.status_code}: {response.text}"

    articles = response.json()["articles"]
    results = []
    for article in articles:
        text = article.get("title", "")
        if text:
            prediction, confidence = score_fn(text)
            results.append(
                {
                    "title": text,
                    "prediction": prediction,
                    "confidence": confidence,
                }
            )
    return results, None
