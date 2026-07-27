import logging
import os

# Log dosyalarının yazılacağı klasör
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    İsme göre yapılandırılmış bir logger döner.
    Kullanım: logger = get_logger(__name__)

    Her modül kendi adıyla logger alır, böylece log satırında
    hangi dosyadan geldiği görünür.
    """
    logger = logging.getLogger(name)

    # Aynı logger'a birden fazla handler eklenmesini önle
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Log satırı formatı: 2024-01-15 10:30:00 | INFO | app.routes.auth | Login attempt for user: onur
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler 1: Terminale yaz (Docker'da docker logs ile görünür)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Handler 2: Dosyaya yaz (kalıcı kayıt)
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger
