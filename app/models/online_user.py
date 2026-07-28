from app import db
from datetime import datetime, timezone


class OnlineUser(db.Model):
    __tablename__ = "online_users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    ipaddress = db.Column(db.String(45), nullable=False)
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
