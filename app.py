from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

from src.fake_news_detection.main import app, run


if __name__ == "__main__":
    run(debug=True)
    