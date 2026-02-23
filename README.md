# Fake News Detection Platform

End-to-end fake news detection project combining machine learning inference, dataset generation, and a Flask backend API for user authentication and prediction workflows.

## Problem

Misinformation spreads quickly and is difficult to assess manually at scale. Teams need a lightweight service that can:
- classify incoming news text as potentially fake or real,
- support user-facing API workflows,
- and remain maintainable for future model and data pipeline improvements.

## Solution

This project provides:
- a supervised ML pipeline for training a text classifier,
- a reusable prediction service used by backend routes,
- a Flask API with authentication and detection endpoints,
- and a structured architecture under `src/` to support production-style development.

## Tech Stack

- Python 3.x
- Flask
- scikit-learn
- pandas
- SQLite
- joblib
- requests

## Architecture

```text
fake_news_detection/
├── src/
│   └── fake_news_detection/
│       ├── api/                # Flask app factory and routes
│       ├── data/               # Dataset creation and preprocessing flows
│       ├── database/           # SQLite repository/auth data access
│       ├── ml/                 # Training and inference logic
│       ├── services/           # External integrations (News API)
│       ├── config.py           # Centralized configuration and paths
│       └── main.py             # Package runtime entrypoint
├── data/
│   └── raw/                    # Raw/generated training dataset files
├── models/                     # Trained model artifacts (.pkl)
├── notebooks/                  # Experiment and EDA notebooks
├── screenshots/                # Demo screenshots for README/docs
├── static/                     # Frontend static assets
├── main.py                     # Root application entrypoint
├── app.py                      # Compatibility runner for Flask app
├── create_dataset.py           # Compatibility runner for dataset creation
├── train_model.py              # Compatibility runner for model training
```

## Results

- Clear separation of concerns for API, data, ML, DB, and external services.
- GitHub-ready layout with professional documentation and ignore rules.
- Backward compatibility retained through root-level script wrappers.
- Safer long-term maintainability with centralized config and entrypoints.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables:
   - `FLASK_SECRET_KEY` (required)
   - `NEWS_API_KEY` (optional, required only for News API integrations)
   
   Create a `.env` file from `.env.example` and set `FLASK_SECRET_KEY` to a stable value.
3. Run the API:
   ```bash
   python main.py
   ```
4. Build dataset:
   ```bash
   python create_dataset.py
   ```
5. Train model:
   ```bash
   python train_model.py
   ```
