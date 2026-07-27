from flask import Blueprint, jsonify
from app.models.online_user import OnlineUser
from app.logger import get_logger

logger = get_logger(__name__)

online_bp = Blueprint("online", __name__)


@online_bp.route("/onlineusers", methods=["GET"])
def get_online_users():
    """
    Şu an sistemde aktif olan tüm kullanıcıları listeler.
    online_users tablosundaki tüm kayıtları döner.
    """
    online_users = OnlineUser.query.all()
    logger.info(f"Online users requested. Currently online: {len(online_users)}")
    return jsonify({
        "online_count": len(online_users),
        "online_users": [u.to_dict() for u in online_users],
    }), 200
