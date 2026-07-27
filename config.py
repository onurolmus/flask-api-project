import os


class Config:
    # ⭐ Kritik: Bu anahtar Flask session'larını imzalar.
    # Ortam değişkeninden okunur, yoksa geliştirme için varsayılan kullanılır.
    # Production'da .env dosyasında mutlaka güçlü bir değer set edilmeli.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

    # PostgreSQL bağlantı dizesi.
    # Format: postgresql://kullanici:sifre@host:port/veritabani_adi
    # Tüm parçalar .env dosyasından okunur.
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://"
        f"{os.environ.get('DB_USER', 'flaskuser')}:"
        f"{os.environ.get('DB_PASSWORD', 'flaskpass')}@"
        f"{os.environ.get('DB_HOST', 'localhost')}:"
        f"{os.environ.get('DB_PORT', '5432')}/"
        f"{os.environ.get('DB_NAME', 'flaskdb')}"
    )

    # SQLAlchemy'nin her sorguyu terminale loglamasını kapatır.
    # True yapınca debug sırasında hangi SQL sorgusu çalıştığını görebilirsin.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
