import sys

import pandas as pd
import requests

from ..config import DATASET_PATH, NEWS_API_KEY, NEWS_API_URL, ensure_project_dirs


def fetch_news(query: str = "current affairs", num_articles: int = 50):
    print(f"Fetching news with query: {query}, number of articles: {num_articles}")
    if not NEWS_API_KEY:
        print("Error fetching news: NEWS_API_KEY is not configured")
        return None

    try:
        params = {
            "q": query,
            "apiKey": NEWS_API_KEY,
            "pageSize": num_articles,
            "language": "en",
        }
        response = requests.get(NEWS_API_URL, params=params)
        print(f"NewsAPI response status code: {response.status_code}")
        if response.status_code == 200:
            articles = response.json()["articles"]
            print(f"Fetched {len(articles)} articles")
            data = pd.DataFrame(articles)
            data["valeur"] = 0
            return data[["title", "valeur"]].rename(columns={"title": "texte"})

        print(f"Error fetching data: {response.status_code} - {response.text}")
        return None
    except Exception as exc:
        print(f"Error fetching news: {exc}")
        return None


def build_dataset() -> None:
    print("Generating dataset...")
    ensure_project_dirs()
    try:
        data = fetch_news()
        if data is not None:
            print("Adding fake news examples...")
            fake_news = pd.DataFrame(
                {
                    "texte": [
                        "Aliens invade Earth with giant spaceships!",
                        "Moon landing was faked in a Hollywood studio!",
                    ],
                    "valeur": [1, 1],
                }
            )
            data = pd.concat([data, fake_news], ignore_index=True)
            print(f"Total dataset size: {len(data)} rows")
            print(f"Saving dataset to {DATASET_PATH}...")
            data.to_excel(DATASET_PATH, index=False)
            print(f"Dataset saved as {DATASET_PATH.name}")
        else:
            print("Failed to fetch data from NewsAPI.")
    except Exception as exc:
        print(f"Error in main block: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    build_dataset()
