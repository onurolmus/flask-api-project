from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.utils.security import hash_password, validate_email, validate_password_complexity
from app.logger import get_logger

logger = get_logger(__name__)

# Bu Blueprint'in adı "users", tüm route'ları /user ile başlayacak
users_bp = Blueprint("users", __name__)


@users_bp.route("/user/create", methods=["POST"])
def create_user():
    """
    Yeni kullanıcı oluşturur.
    Body: username, firstname, middlename(opsiyonel), lastname,
          birthdate, email, password
    """
    data = request.get_json()

    # İstek body'si JSON değilse veya boşsa
    if not data:
        logger.warning("User create attempt with no JSON body.")
        return jsonify({"error": "Request body must be JSON."}), 400

    # Zorunlu alanların hepsinin gelip gelmediğini kontrol et
    required = ["username", "firstname", "lastname", "birthdate", "email", "password"]
    missing = [field for field in required if not data.get(field)]
    if missing:
        logger.warning(f"User create failed. Missing fields: {missing}")
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    # Email format kontrolü
    if not validate_email(data["email"]):
        logger.warning(f"User create failed. Invalid email: {data['email']}")
        return jsonify({"error": "Invalid email format."}), 400

    # Şifre karmaşıklık kontrolü
    is_valid, msg = validate_password_complexity(data["password"])
    if not is_valid:
        logger.warning(f"User create failed. Weak password for: {data['username']}")
        return jsonify({"error": msg}), 400

    # Aynı username veya email zaten var mı?
    if User.query.filter_by(username=data["username"]).first():
        logger.warning(f"User create failed. Username already exists: {data['username']}")
        return jsonify({"error": "Username already exists."}), 409

    if User.query.filter_by(email=data["email"]).first():
        logger.warning(f"User create failed. Email already exists: {data['email']}")
        return jsonify({"error": "Email already exists."}), 409

    # ⭐ Şifreyi hash'le — düz metin asla DB'ye yazılmaz
    hashed = hash_password(data["password"])

    new_user = User(
        username=data["username"],
        firstname=data["firstname"],
        middlename=data.get("middlename"),  # Opsiyonel, yoksa None
        lastname=data["lastname"],
        birthdate=data["birthdate"],
        email=data["email"],
        password_hash=hashed,
    )

    db.session.add(new_user)
    db.session.commit()

    logger.info(f"New user created: {new_user.username} (id={new_user.id})")
    return jsonify({"message": "User created successfully.", "user": new_user.to_dict()}), 201


@users_bp.route("/user/list", methods=["GET"])
def list_users():
    """
    Tüm kullanıcıları listeler.
    to_dict() şifre hash'ini döndürmez — güvenli.
    """
    users = User.query.all()
    logger.info(f"User list requested. Total: {len(users)} users.")
    return jsonify({"users": [u.to_dict() for u in users]}), 200


@users_bp.route("/user/update/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Belirtilen ID'li kullanıcıyı günceller.
    Sadece gönderilen alanlar güncellenir — gönderilmeyenler değişmez.
    """
    # 404: Kullanıcı bulunamazsa Flask otomatik 404 döner
    user = db.session.get(User, user_id)
    if not user:
        logger.warning(f"User update failed. User not found: id={user_id}")
        return jsonify({"error": "User not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    # Sadece gelen alanları güncelle (partial update)
    if "firstname" in data:
        user.firstname = data["firstname"]
    if "middlename" in data:
        user.middlename = data["middlename"]
    if "lastname" in data:
        user.lastname = data["lastname"]
    if "birthdate" in data:
        user.birthdate = data["birthdate"]

    # Email değişiyorsa format ve uniqueness kontrolü
    if "email" in data:
        if not validate_email(data["email"]):
            return jsonify({"error": "Invalid email format."}), 400
        existing = User.query.filter_by(email=data["email"]).first()
        if existing and existing.id != user_id:
            return jsonify({"error": "Email already in use."}), 409
        user.email = data["email"]

    # Şifre değişiyorsa tekrar hash'le
    if "password" in data:
        is_valid, msg = validate_password_complexity(data["password"])
        if not is_valid:
            return jsonify({"error": msg}), 400
        user.password_hash = hash_password(data["password"])

    db.session.commit()
    logger.info(f"User updated: {user.username} (id={user_id})")
    return jsonify({"message": "User updated successfully.", "user": user.to_dict()}), 200


@users_bp.route("/user/delete/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Belirtilen ID'li kullanıcıyı siler.
    Kullanıcı yoksa 404 döner.
    """
    user = db.session.get(User, user_id)
    if not user:
        logger.warning(f"User delete failed. User not found: id={user_id}")
        return jsonify({"error": "User not found."}), 404

    username = user.username
    db.session.delete(user)
    db.session.commit()

    logger.info(f"User deleted: {username} (id={user_id})")
    return jsonify({"message": f"User '{username}' deleted successfully."}), 200
