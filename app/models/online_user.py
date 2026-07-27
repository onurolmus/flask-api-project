from app import db
from datetime import datetime, timezone


class OnlineUser(db.Model):
    """
    'online_users' tablosunu temsil eder.
    Login olunca kayıt eklenir, logout olunca silinir.
    Mentörün istediği veri yapısı: username, ipaddress, logindatetime
    """

    __tablename__ = "online_users"

    id = db.Column(db.Integer, primary_key=True)

    # Hangi kullanıcı online — users tablosundaki username ile eşleşir
    username = db.Column(db.String(80), nullable=False)

    # Login isteğinin geldiği IP adresi (Flask request.remote_addr'dan alınır)
    ipaddress = db.Column(db.String(45), nullable=False)

    # 45 karakter neden? IPv4 max 15 karakter, IPv6 max 39 karakter.
    # IPv6-mapped IPv4 (::ffff:192.168.1.1) formatı 45 karaktere kadar çıkabilir.

    # Login zamanı — otomatik olarak şimdiki UTC zamanı set edilir
    logindatetime = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "ipaddress": self.ipaddress,
            "logindatetime": self.logindatetime.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<OnlineUser {self.username} from {self.ipaddress}>"
