from .api.app import create_app
from .config import ensure_project_dirs

ensure_project_dirs()
app = create_app()


def run(debug: bool = True) -> None:
    app.run(debug=debug)


if __name__ == "__main__":
    run(debug=True)
