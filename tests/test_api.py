"""
Flask API Otomatik Test Paketi
==============================
Bu dosya tüm endpoint'leri sırayla test eder.
Çalıştırmak için: python tests/test_api.py

Sistem çalışır durumdayken (docker compose up -d) çalıştırılmalıdır.
"""

import requests
import sys

BASE_URL = "http://localhost:5000"

# Test sonuçlarını takip etmek için sayaçlar
passed = 0
failed = 0


def test(name, condition, response=None):
    """
    Test sonucunu değerlendirir ve ekrana basar.
    condition True ise PASS, False ise FAIL yazar.
    """
    global passed, failed
    if condition:
        print(f"  ✅ PASS | {name}")
        passed += 1
    else:
        print(f"  ❌ FAIL | {name}")
        if response:
            print(f"          Cevap: {response.status_code} → {response.text[:200]}")
        failed += 1


def separator(title):
    print(f"\n{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}")


# ─────────────────────────────────────────────────
# TEST 1: KULLANICI OLUŞTURMA
# ─────────────────────────────────────────────────
separator("POST /user/create")

# Önce varsa eski test kullanıcısını temizle
# (birden fazla test çalıştırıldığında conflict olmasın)
requests.delete(f"{BASE_URL}/user/delete/999")  # olmayabilir, sorun değil

# Başarılı kullanıcı oluşturma
r = requests.post(f"{BASE_URL}/user/create", json={
    "username": "testuser",
    "firstname": "Test",
    "lastname": "User",
    "birthdate": "1995-05-15",
    "email": "testuser@example.com",
    "password": "Secure123"
})
test("Geçerli veriyle kullanıcı oluşturuldu", r.status_code == 201, r)
test("Cevap 'message' içeriyor", "message" in r.json(), r)
test("Cevap 'user' içeriyor", "user" in r.json(), r)
test("Şifre cevatta YOK (güvenlik)", "password_hash" not in r.json().get("user", {}), r)

# Kullanıcı ID'sini sonraki testler için saklıyoruz
user_id = r.json().get("user", {}).get("id")

# Aynı username ile tekrar kayıt — 409 Conflict bekliyoruz
r = requests.post(f"{BASE_URL}/user/create", json={
    "username": "testuser",
    "firstname": "Test",
    "lastname": "User",
    "birthdate": "1995-05-15",
    "email": "different@example.com",
    "password": "Secure123"
})
test("Aynı username ile kayıt reddedildi (409)", r.status_code == 409, r)

# Geçersiz email formatı — 400 bekliyoruz
r = requests.post(f"{BASE_URL}/user/create", json={
    "username": "testuser2",
    "firstname": "Test",
    "lastname": "User",
    "birthdate": "1995-05-15",
    "email": "gecersiz-email",
    "password": "Secure123"
})
test("Geçersiz email formatı reddedildi (400)", r.status_code == 400, r)

# Zayıf şifre — 400 bekliyoruz
r = requests.post(f"{BASE_URL}/user/create", json={
    "username": "testuser3",
    "firstname": "Test",
    "lastname": "User",
    "birthdate": "1995-05-15",
    "email": "testuser3@example.com",
    "password": "zayif"  # 8 karakterden az, büyük harf yok, rakam yok
})
test("Zayıf şifre reddedildi (400)", r.status_code == 400, r)

# Eksik zorunlu alan — 400 bekliyoruz
r = requests.post(f"{BASE_URL}/user/create", json={
    "username": "testuser4"
    # firstname, lastname, email, password eksik
})
test("Eksik zorunlu alanlar reddedildi (400)", r.status_code == 400, r)


# ─────────────────────────────────────────────────
# TEST 2: KULLANICI LİSTELEME
# ─────────────────────────────────────────────────
separator("GET /user/list")

r = requests.get(f"{BASE_URL}/user/list")
test("Kullanıcı listesi alındı (200)", r.status_code == 200, r)
test("Cevap 'users' listesi içeriyor", "users" in r.json(), r)
test("Liste boş değil", len(r.json().get("users", [])) > 0, r)


# ─────────────────────────────────────────────────
# TEST 3: KULLANICI GÜNCELLEME
# ─────────────────────────────────────────────────
separator("PUT /user/update/<id>")

r = requests.put(f"{BASE_URL}/user/update/{user_id}", json={
    "firstname": "Updated"
})
test("Kullanıcı güncellendi (200)", r.status_code == 200, r)
test("Güncellenen alan değişti", r.json().get("user", {}).get("firstname") == "Updated", r)

# Olmayan kullanıcı — 404 bekliyoruz
r = requests.put(f"{BASE_URL}/user/update/99999", json={"firstname": "Ghost"})
test("Olmayan kullanıcı güncellenemedi (404)", r.status_code == 404, r)


# ─────────────────────────────────────────────────
# TEST 4: LOGIN
# ─────────────────────────────────────────────────
separator("POST /login")

r = requests.post(f"{BASE_URL}/login", json={
    "username": "testuser",
    "password": "Secure123"
})
test("Geçerli bilgilerle login başarılı (200)", r.status_code == 200, r)
test("Cevap 'ip' içeriyor", "ip" in r.json(), r)
test("Cevap 'message' içeriyor", "message" in r.json(), r)

# Yanlış şifre — 401 bekliyoruz
r = requests.post(f"{BASE_URL}/login", json={
    "username": "testuser",
    "password": "YanlisŞifre99"
})
test("Yanlış şifre reddedildi (401)", r.status_code == 401, r)
test("Hata mesajı user enumeration yapmıyor",
     r.json().get("error") == "Invalid username or password.", r)

# Olmayan kullanıcı — yine 401 (aynı mesaj, user enumeration koruması)
r = requests.post(f"{BASE_URL}/login", json={
    "username": "olmayan_kullanici",
    "password": "HerhangiSifre1"
})
test("Olmayan kullanıcı aynı hata mesajını veriyor (401)",
     r.status_code == 401 and r.json().get("error") == "Invalid username or password.", r)


# ─────────────────────────────────────────────────
# TEST 5: ONLINE KULLANICILAR
# ─────────────────────────────────────────────────
separator("GET /onlineusers")

r = requests.get(f"{BASE_URL}/onlineusers")
test("Online kullanıcılar alındı (200)", r.status_code == 200, r)
test("'online_count' alanı var", "online_count" in r.json(), r)
test("'online_users' listesi var", "online_users" in r.json(), r)
test("testuser online listede", any(
    u["username"] == "testuser"
    for u in r.json().get("online_users", [])
), r)


# ─────────────────────────────────────────────────
# TEST 6: LOGOUT
# ─────────────────────────────────────────────────
separator("POST /logout")

r = requests.post(f"{BASE_URL}/logout", json={"username": "testuser"})
test("Logout başarılı (200)", r.status_code == 200, r)

# Çıkış yaptıktan sonra tekrar çıkış — 404 bekliyoruz
r = requests.post(f"{BASE_URL}/logout", json={"username": "testuser"})
test("Zaten offline kullanıcı tekrar logout edemez (404)", r.status_code == 404, r)

# Logout sonrası online listede olmamalı
r = requests.get(f"{BASE_URL}/onlineusers")
test("Logout sonrası online listeden çıktı", not any(
    u["username"] == "testuser"
    for u in r.json().get("online_users", [])
), r)


# ─────────────────────────────────────────────────
# TEST 7: KULLANICI SİLME
# ─────────────────────────────────────────────────
separator("DELETE /user/delete/<id>")

r = requests.delete(f"{BASE_URL}/user/delete/{user_id}")
test("Kullanıcı silindi (200)", r.status_code == 200, r)

# Silinen kullanıcıyı tekrar sil — 404 bekliyoruz
r = requests.delete(f"{BASE_URL}/user/delete/{user_id}")
test("Silinen kullanıcı tekrar silinemiyor (404)", r.status_code == 404, r)


# ─────────────────────────────────────────────────
# SONUÇ
# ─────────────────────────────────────────────────
total = passed + failed
print(f"\n{'═'*50}")
print(f"  SONUÇ: {passed}/{total} test geçti", end="")
if failed == 0:
    print(" 🎉 Tüm testler başarılı!")
else:
    print(f" ⚠️  {failed} test başarısız!")
print(f"{'═'*50}\n")

# CI/CD ortamlarında kullanılabilsin diye:
# Başarısız test varsa exit code 1 döner
sys.exit(0 if failed == 0 else 1)
