from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.models.online_user import OnlineUser
from app.utils.security import verify_password
from app.logger import get_logger

logger = get_logger(__name__)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        logger.warning("Login attempt with missing username or password.")
        return jsonify({"error": "Username and password are required."}), 400

    user = User.query.filter_by(username=username).first()

    # Return the same error for both invalid username and wrong password
    # to prevent user enumeration attacks.
    if not user or not verify_password(password, user.password_hash):
        logger.warning(f"Failed login attempt for username: {username}")
        return jsonify({"error": "Invalid username or password."}), 401

    already_online = OnlineUser.query.filter_by(username=username).first()
    if already_online:
        logger.info(f"User already online: {username}")
        return jsonify({"message": "User is already logged in."}), 200

    ip_address = request.headers.get("X-Real-IP", request.remote_addr)

    online_entry = OnlineUser(
        username=username,
        ipaddress=ip_address,
    )
    db.session.add(online_entry)
    db.session.commit()

    logger.info(f"User logged in: {username} from {ip_address}")
    return jsonify({
        "message": f"Login successful. Welcome, {username}!",
        "user": username,
        "ip": ip_address,
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    username = data.get("username")
    if not username:
        return jsonify({"error": "Username is required."}), 400

    online_entry = OnlineUser.query.filter_by(username=username).first()
    if not online_entry:
        logger.warning(f"Logout attempt for non-online user: {username}")
        return jsonify({"error": "User is not currently logged in."}), 404

    db.session.delete(online_entry)
    db.session.commit()

    logger.info(f"User logged out: {username}")
    return jsonify({"message": f"Logout successful. Goodbye, {username}!"}), 200
