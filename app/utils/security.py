import hashlib
import re
import secrets


def hash_password(plain_password: str) -> str:
    """
    Şifreyi SHA-256 + Salt ile hash'ler.

    Adımlar:
    1. secrets.token_hex(32) ile 64 karakterli kriptografik salt üretir.
    2. salt + plain_password birleştirilip SHA-256 ile hash'lenir.
    3. "salt:hash" formatında tek string olarak döner.

    Bu format veritabanında saklanır. Doğrulama sırasında salt ayrılır
    ve aynı işlem tekrar yapılarak karşılaştırılır.
    """
    salt = secrets.token_hex(32)
    hash_value = hashlib.sha256((salt + plain_password).encode()).hexdigest()
    return f"{salt}:{hash_value}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """
    Girilen şifreyi veritabanındaki hash ile karşılaştırır.

    stored_hash "salt:hash" formatında gelir.
    Salt ayrılır, aynı hash işlemi uygulanır, sonuçlar karşılaştırılır.

    secrets.compare_digest() kullanıyoruz çünkü == operatörü
    "timing attack"e karşı savunmasızdır. compare_digest her
    karşılaştırmayı sabit sürede yapar.
    """
    try:
        salt, original_hash = stored_hash.split(":", 1)
        new_hash = hashlib.sha256((salt + plain_password).encode()).hexdigest()
        return secrets.compare_digest(new_hash, original_hash)
    except ValueError:
        return False


def validate_password_complexity(password: str) -> tuple[bool, str]:
    """
    Mentörün istediği şifre karmaşıklık kurallarını kontrol eder:
    - En az 8 karakter
    - En az 1 büyük harf [A-Z]
    - En az 1 küçük harf [a-z]
    - En az 1 rakam [0-9]

    Dönüş: (geçerli_mi: bool, hata_mesajı: str)
    Geçerliyse ("", "") döner.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."

    return True, ""


def validate_email(email: str) -> bool:
    """
    Email formatını regex ile doğrular.
    Geçerli format: kullanici@domain.com

    Regex açıklaması:
    ^[a-zA-Z0-9._%+-]+   → Kullanıcı adı kısmı (harf, rakam, özel karakterler)
    @                     → @ işareti zorunlu
    [a-zA-Z0-9.-]+        → Domain adı
    \\.                   → Nokta zorunlu
    [a-zA-Z]{2,}$        → TLD (com, net, org vs.) en az 2 harf
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))
