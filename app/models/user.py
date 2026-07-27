from app import db
from datetime import datetime, timezone


class User(db.Model):
    """
    'users' tablosunu temsil eder.
    SQLAlchemy bu sınıfı okuyarak PostgreSQL'de tabloyu otomatik oluşturur.
    """

    __tablename__ = "users"

    # PRIMARY KEY: Her satır için unique, otomatik artan tam sayı kimlik
    id = db.Column(db.Integer, primary_key=True)

    # UNIQUE + NOT NULL: Aynı username iki kez kayıt olamaz
    username = db.Column(db.String(80), unique=True, nullable=False)

    firstname = db.Column(db.String(80), nullable=False)

    # nullable=True: Orta isim zorunlu değil (mentörün veri yapısında var ama boş olabilir)
    middlename = db.Column(db.String(80), nullable=True)

    lastname = db.Column(db.String(80), nullable=False)

    birthdate = db.Column(db.String(20), nullable=False)

    # Email de unique olmalı — aynı email ile iki hesap açılmamalı
    email = db.Column(db.String(120), unique=True, nullable=False)

    # ⭐ Düz şifre asla saklanmaz. Veritabanında "salt:hash" formatı tutulur.
    # security.py'daki hash_password() fonksiyonu bu formatı üretir.
    password_hash = db.Column(db.String(256), nullable=False)

    # Kayıt zamanı otomatik set edilir, sonradan değiştirilemez
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self) -> dict:
        """
        Kullanıcıyı JSON'a dönüştürür.
        ⭐ password_hash bu dict'e DAHİL DEĞİL — API cevabında şifre gönderilmez.
        """
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "middlename": self.middlename,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<User {self.username}>"
