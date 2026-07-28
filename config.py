import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://"
        f"{os.environ.get('DB_USER', 'flaskuser')}:"
        f"{os.environ.get('DB_PASSWORD', 'flaskpass')}@"
        f"{os.environ.get('DB_HOST', 'localhost')}:"
        f"{os.environ.get('DB_PORT', '5432')}/"
        f"{os.environ.get('DB_NAME', 'flaskdb')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
