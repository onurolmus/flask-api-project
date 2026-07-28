# Flask RESTful API

Staj görevi kapsamında geliştirilen kullanıcı yönetim API'ı.  
Nginx + ModSecurity WAF projesiyle entegre çalışacak şekilde tasarlanmıştır.

## Teknolojiler

| Teknoloji | Versiyon | Kullanım Amacı |
|---|---|---|
| Python | 3.12 | Ana programlama dili |
| Flask | 3.1.0 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | ORM (veritabanı katmanı) |
| Flask-Migrate | 4.1.0 | Veritabanı şema yönetimi |
| PostgreSQL | 16 | İlişkisel veritabanı |
| uWSGI | 2.0.28 | Production WSGI sunucusu |
| Docker & Compose | - | Konteynerleştirme |

## Mimari

```
İstemci (curl / Postman)
        │
        ▼
  uWSGI (port 5000)
        │
        ▼
  Flask Application
  ├── routes/auth.py      → /login, /logout
  ├── routes/users.py     → /user/* CRUD
  └── routes/online.py    → /onlineusers
        │
        ▼
  PostgreSQL
  ├── users tablosu
  └── online_users tablosu
```

## Güvenlik Özellikleri

- **SHA-256 + Salt** şifre hash'leme — düz metin şifre asla saklanmaz
- **Şifre karmaşıklık kuralları** — min 8 karakter, büyük/küçük harf, rakam
- **Email format doğrulama** — regex ile kontrol
- **User Enumeration koruması** — yanlış şifre ve olmayan kullanıcı için aynı hata mesajı
- **Activity Logging** — tüm işlemler konsola ve `logs/app.log` dosyasına yazılır

## Kurulum ve Çalıştırma

### Gereksinimler
- Docker ve Docker Compose
- Python 3.12 (yerel geliştirme için)

### 1. Repoyu klonla
```bash
git clone <repo-url>
cd flask-api-project
```

### 2. `.env` dosyası oluştur
```bash
cp .env.example .env   # veya aşağıdaki içeriği elle oluştur
```

`.env` içeriği:
```
SECRET_KEY=guclu-bir-secret-key-yaz
DB_USER=flaskuser
DB_PASSWORD=flaskpass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=flaskdb
```

### 3. Sistemi başlat
```bash
# PostgreSQL'i başlat
docker compose up -d db

# Veritabanı tablolarını oluştur
export FLASK_APP=run.py
flask db upgrade

# Tüm sistemi başlat
docker compose up -d
```

### 4. Çalıştığını doğrula
```bash
docker compose ps
```

## API Endpoint'leri

### Kullanıcı İşlemleri

| Method | Endpoint | Açıklama |
|---|---|---|
| `POST` | `/user/create` | Yeni kullanıcı oluştur |
| `GET` | `/user/list` | Tüm kullanıcıları listele |
| `PUT` | `/user/update/<id>` | Kullanıcı güncelle |
| `DELETE` | `/user/delete/<id>` | Kullanıcı sil |

### Kimlik Doğrulama

| Method | Endpoint | Açıklama |
|---|---|---|
| `POST` | `/login` | Giriş yap |
| `POST` | `/logout` | Çıkış yap |
| `GET` | `/onlineusers` | Online kullanıcıları listele |

### Örnek İstekler

**Kullanıcı oluştur:**
```bash
curl -X POST http://localhost:5000/user/create \
  -H "Content-Type: application/json" \
  -d '{
    "username": "onur",
    "firstname": "Onur",
    "lastname": "Olmus",
    "birthdate": "2000-01-01",
    "email": "onur@example.com",
    "password": "Guclu1234"
  }'
```

**Giriş yap:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "onur", "password": "Guclu1234"}'
```

### Veri Yapıları

**`POST /user/create` — Request Body:**
```json
{
  "username": "string (zorunlu, unique)",
  "firstname": "string (zorunlu)",
  "middlename": "string (opsiyonel)",
  "lastname": "string (zorunlu)",
  "birthdate": "string (zorunlu)",
  "email": "string (zorunlu, unique, email formatı)",
  "password": "string (zorunlu, min 8 karakter, büyük/küçük harf + rakam)"
}
```

**`GET /onlineusers` — Response:**
```json
{
  "online_count": 1,
  "online_users": [
    {
      "username": "onur",
      "ipaddress": "172.18.0.1",
      "logindatetime": "2024-01-15T10:30:00"
    }
  ]
}
```

## HTTP Durum Kodları

| Kod | Anlam |
|---|---|
| 200 | Başarılı |
| 201 | Kayıt oluşturuldu |
| 400 | Geçersiz istek (eksik alan, hatalı format) |
| 401 | Kimlik doğrulama başarısız |
| 404 | Kayıt bulunamadı |
| 409 | Çakışma (username/email zaten mevcut) |

## Testleri Çalıştırma

```bash
source .venv/bin/activate
python tests/test_api.py
```

Sistem çalışır durumdayken (docker compose up -d) çalıştırılmalıdır.  
Başarılı çıktı: `29/29 test geçti 🎉`

## Proje Yapısı

```
flask-api-project/
├── app/
│   ├── __init__.py       # Application Factory
│   ├── logger.py         # Merkezi loglama
│   ├── models/
│   │   ├── user.py       # User veritabanı modeli
│   │   └── online_user.py # OnlineUser veritabanı modeli
│   ├── routes/
│   │   ├── auth.py       # /login, /logout
│   │   ├── users.py      # CRUD endpoint'leri
│   │   └── online.py     # /onlineusers
│   └── utils/
│       └── security.py   # SHA-256+Salt, validasyon
├── migrations/           # Flask-Migrate şema dosyaları
├── tests/
│   └── test_api.py       # Otomatik test paketi
├── logs/                 # Uygulama logları
├── config.py             # Uygulama yapılandırması
├── run.py                # Geliştirme sunucusu giriş noktası
├── uwsgi.ini             # uWSGI production yapılandırması
├── Dockerfile            # Flask container tanımı
├── compose.yaml          # Multi-container orkestrasyon
└── requirements.txt      # Python bağımlılıkları
```
