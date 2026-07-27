# Bu dosya modelleri tek noktadan dışa aktarır.
# Flask-Migrate'in tabloları görebilmesi için
# create_app() çalışmadan önce import edilmiş olmalılar.
from app.models.user import User
from app.models.online_user import OnlineUser

__all__ = ["User", "OnlineUser"]
