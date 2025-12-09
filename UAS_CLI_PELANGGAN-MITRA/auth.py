USERS = {
    "alice": {"password": "alice123", "role": "pelanggan", "nama": "Alice Pelanggan"},
    "budi":  {"password": "budi123",  "role": "mitra",      "nama": "Budi Mitra"},
    "tina":  {"password": "tina123",  "role": "pelanggan", "nama": "Tina Pelanggan"},
}

def login():
    print("=== LOGIN ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = USERS.get(username)
    if user and user["password"] == password:
        print(f"Login berhasil. Halo, {user['nama']} ({user['role']})")
        return {"username": username, "role": user["role"], "nama": user["nama"]}
    print("Login gagal — username/password salah.")
    return None

