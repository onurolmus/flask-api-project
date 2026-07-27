from app import create_app

# Uygulamayı yarat
app = create_app()

if __name__ == "__main__":
    # debug=True: Kod değiştiğinde sunucu otomatik yeniden başlar.
    # Sadece geliştirme ortamında kullanılır, production'da ASLA açılmaz.
    app.run(host="0.0.0.0", port=5000, debug=True)
