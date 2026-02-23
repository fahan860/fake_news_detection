from flask import Blueprint, current_app, jsonify, request, send_from_directory, session

from ..database.repository import authenticate_user, create_user
from ..ml.predictor import predict_fake_news
from ..services.news_api import fetch_scored_news

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/")
def serve_index():
    return send_from_directory(current_app.static_folder, "index.html")


@api_blueprint.route("/<path:path>")
def serve_static(path):
    return send_from_directory(current_app.static_folder, path)

def _signup_impl():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({"message": "Missing fields"}), 400

    is_created = create_user(username=username, email=email, password=password)
    if not is_created:
        return jsonify({"message": "Email already exists"}), 400

    return jsonify({"message": "Account created"}), 201

@api_blueprint.route("/api/signup", methods=["POST"])
def signup():
    return _signup_impl()

def _login_impl():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = authenticate_user(email=email, password=password)
    if user:
        session["user_id"] = user[0]
        session["username"] = user[1]
        return jsonify({"message": "Logged in"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@api_blueprint.route("/api/login", methods=["POST"])
def login():
    return _login_impl()

@api_blueprint.route("/api/check_auth", methods=["GET"])
def check_auth():
    if "user_id" in session:
        return jsonify({"username": session["username"]}), 200
    return jsonify({"message": "Not authenticated"}), 401

@api_blueprint.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return jsonify({"message": "Logged out"}), 200

def _predict_impl():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"message": "No text provided"}), 400
    prediction, confidence = predict_fake_news(text)
    return jsonify({"prediction": prediction, "confidence": confidence}), 200

@api_blueprint.route("/api/detect", methods=["POST"])
def detect():
    return _predict_impl()

@api_blueprint.route("/api/fetch_news", methods=["POST"])
def fetch_news():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"message": "No query provided"}), 400

    results, error = fetch_scored_news(query=query, score_fn=predict_fake_news)
    if error:
        return jsonify({"message": error}), 500

    return jsonify({"data": results}), 200
