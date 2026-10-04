# 📰 Fake News Detection

**Classify a news article as real or fake with NLP: TF-IDF features, 4 models compared, SVM best at 85.8% accuracy.**

[![Live demo](https://img.shields.io/badge/Live%20demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://fahan-fakenews.streamlit.app)
[![Portfolio](https://img.shields.io/badge/Portfolio-Fatima%20Zahrae%20Ahannuk-0ea5e9)](https://fatima-zahrae-ahannuk.vercel.app/projects/fakenews)

> Team project (4 students) — Machine Learning course, ENSA Tétouan (Big Data & AI), supervised by Ms Imane Hachchane · May 2025.

## Try it
👉 **https://fahan-fakenews.streamlit.app** — paste a headline and get a prediction, a confidence score and the words that pushed the decision.
The online demo uses a lightweight version of the pipeline (TF-IDF 1–2-grams + logistic regression on FakeNewsNet headlines, **82.1% accuracy** on its test split).

## Problem
Misinformation spreads faster than manual fact-checking. The goal was a classifier that flags suspicious articles and an app that makes it usable by non-technical users.

## What we built
- **Data**: labelled news datasets enriched with recent articles fetched through **NewsAPI**; cleaning, normalisation and stop-word removal.
- **Features**: TF-IDF vectorisation.
- **Models compared** (in the project report): SVM, Random Forest, Logistic Regression, Naive Bayes → **SVM best with 85.8% accuracy**.
- **This repository** contains the production pipeline: TF-IDF (1–2-grams, 20k features) + class-balanced Logistic Regression (`train_model.py`), and the **Flask web app**: sign-up / login (SQLite, hashed passwords), `/api/detect` returning the prediction with a confidence score, and `/api/fetch_news` to pull recent articles from NewsAPI.

| Model | Role |
|---|---|
| **SVM** | best model — 85.8% accuracy |
| Logistic Regression | production model in this repo and in the online demo |
| Random Forest, Naive Bayes | compared |

## Tech stack
Python · scikit-learn · TF-IDF · NewsAPI · Flask · SQLite · HTML/CSS/JS · Streamlit (demo)

## Project structure
```text
src/fake_news_detection/
├── api/          # Flask app + routes (auth, analysis)
├── data/         # dataset builder (NewsAPI + labelled sources)
├── ml/           # training + predictor
├── services/     # NewsAPI client
├── database/     # user repository
└── config.py     # settings from environment variables
static/           # web interface
main.py · create_dataset.py · train_model.py   # entry points
```

## Run locally
```bash
pip install -r requirements.txt
# environment variables
export FLASK_SECRET_KEY="change-me"
export NEWS_API_KEY="..."      # optional, only to fetch new articles
python create_dataset.py       # build the dataset
python train_model.py          # train and save the model
python main.py                 # start the web app → http://127.0.0.1:5000
```

## Limitations
The model learns words and writing style, not factual truth. It is biased toward the topics of its training data (US politics, celebrity news) and should be used as a triage tool, not as a fact-checker.

## Author
**Fatima Zahrae Ahannuk** — Big Data & AI engineering student · [Portfolio](https://fatima-zahrae-ahannuk.vercel.app) · [LinkedIn](https://www.linkedin.com/in/fatima-zahrae-ahannuk-b936b1351/) · [GitHub](https://github.com/fahan860)
