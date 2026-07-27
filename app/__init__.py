from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# db nesnesi burada oluşturuluyor ama henüz hiçbir uygulamaya bağlı değil.
# Blueprint'lerin ve model'lerin bu nesneyi import edebilmesi için
# modül seviyesinde tanımlanıyor.
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """
    Application Factory: Flask uygulamasını yaratır ve yapılandırır.
    Bu fonksiyon her çağrıldığında fresh bir uygulama örneği döner.
    """
    app = Flask(__name__)

    # config.py'daki Config sınıfındaki ayarları uygulamaya yükle
    app.config.from_object(Config)

    # db ve migrate nesnelerini bu uygulamaya bağla
    db.init_app(app)
    migrate.init_app(app, db)

    # Modelleri import et — Flask-Migrate tabloları bu sayede keşfeder.
    # Bu import create_app() içinde olmalı, dışarıda olursa
    # db henüz init edilmeden import çalışır ve hata verir.
    from app.models import User, OnlineUser  # noqa: F401

    # ⭐ Blueprint'ler burada register edilecek.
    # Her route dosyasını yazdıkça buraya ekleyeceğiz.
    # Şimdilik boş bırakıyoruz.

    return app
