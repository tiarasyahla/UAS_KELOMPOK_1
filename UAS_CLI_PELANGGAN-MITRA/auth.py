import csv
import os
from utils import press_enter

FILE_USER = "user.csv"
TOKO_FILE = "profil_toko.csv"

def ensure_user_csv():
    if not os.path.exists(FILE_USER):
        with open(FILE_USER, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDNAMES)
            
def load_users():
    ensure_user_csv()
    users = {}
    with open(FILE_USER, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            users[row["username"]] = {
                "password": row["password"],
                "role": row["role"],
                "nama": row["nama"],
                "toko": row.get("toko", ""),
                "status": row.get("status", "aktif")
            }
    return users

def save_all_users(users):
    with open(FILE_USER, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for u, d in users.items():
            writer.writerow({
                "username": u,
                "password": d["password"],
                "role": d["role"],
                "nama": d["nama"],
                "toko": d.get("toko", ""),
                "status": d.get("status", "aktif")
            })


def input_username():
    for kesempatan in range(3):
        username = input("Username: ").strip()
        if not username:
            print(f"Username tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif not valid_username(username):
            print(f"Username harus alfanumerik dan minimal terdiri dari 4 karakter (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif username in load_users():
            print(f"Username sudah terdaftar (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        else:
            return username

def input_password():
    for kesempatan in range(3):
        password = input("Password: ").strip()
        if not password:
            print(f"Password tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif not valid_password(password):
            print(f"Password minimal 8 karakter dan kombinasi huruf & angka (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        else:
            return password

def input_role():
    for kesempatan in range(3):
        role = input("Role (pelanggan/mitra): ").strip().lower()
        if not role:
            print(f"Role tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif not valid_role(role) or role == "admin":
            print(f"Role harus 'pelanggan' atau 'mitra' (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        else:
            return role
        
def input_nama():
    for kesempatan in range(3):
        nama = input("Nama: ").strip()
        if not nama:
            print(f"Nama tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        elif not valid_name(nama):
            print(f"Nama hanya boleh mengandung alfabet dan spasi (sisa kesempatan: {2 - kesempatan}).")
            if kesempatan == 2:
                print("Registrasi gagal.")
                press_enter()
                return
        else:
            return nama

def login():
    while True:
        load_users()
        print("=== LOGIN ===")
        for kesempatan in range(3):
            username = input("Username: ").strip()
            if username == "":
                print(f"Username tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
                if kesempatan == 2:
                    print("Login pengguna gagal.")
                    press_enter()
                    return None
            elif username not in load_users():
                print(f"Username tidak ditemukan (sisa kesempatan: {2 - kesempatan}).")
                if kesempatan == 2:
                    print("Login pengguna gagal.")
                    press_enter()
                    return None
            else:
                break
        
        for kesempatan in range(3):
            user = load_users().get(username)
            password = input("Password: ").strip()
            if not password:
                print(f"Password tidak boleh kosong (sisa kesempatan: {2 - kesempatan}).")
                if kesempatan == 2:
                    print("Login pengguna gagal.")
                    press_enter()
                    return None
            elif password != user["password"]:
                print(f"Password salah (sisa kesempatan: {2 - kesempatan}).")
                if kesempatan == 2:
                    print("Login pengguna gagal.")
                    press_enter()
                    return None
            else:
                break

        if not user:
            print("Login gagal: username tidak ditemukan.")
            return None

        if password != user["password"]:
            print("Login gagal: password salah.")
            return None

        if user["status"] != "aktif":
            print("Akun nonaktif.")
            press_enter()
            return None

        print(f"Login berhasil. Selamat datang, {user['nama']}!")
        return {
            "username": username,
            "password": user["password"],
            "role": user["role"],
            "nama": user["nama"],
            "toko": user.get("toko", ""),
            "status": user.get("status", "aktif")
        }


def register_user(username, password, role, nama, toko="", allow_admin=False):
    users = load_users()
    if username in users:
        return False
    if role == "admin" and not allow_admin:
        return False
    users[username] = {
        "password": password,
        "role": role,
        "nama": nama,
        "toko": toko,
        "status": "aktif"
    }
    save_all_users(users)
    return True

def set_user_status(username, status):
    users = load_users()
    if username not in users:
        return False
    users[username]["status"] = status
    save_all_users(users)
    return True

def delete_user(username):
    users = load_users()
    if username not in users:
        return False
    del users[username]
    save_all_users(users)
    return True

def valid_username(username):
    return len(username) >= 4 and any(c.isalnum() for c in username) and any(c.isalpha() for c in username)

def valid_password(password):
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)

def valid_role(role):
    return role in ["pelanggan", "mitra", "admin"]

def valid_name(nama):
    return any(c.isalpha() for c in nama)


