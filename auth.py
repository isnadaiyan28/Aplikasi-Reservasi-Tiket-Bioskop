from data_store import load_excel, save_excel, USERS_FILE
from visualisasi import tampilkan_error, tampilkan_peringatan, tampilkan_sukses, tampilkan_header


def register_customer():
    tampilkan_header("Registrasi Pelanggan Baru")
    users = load_excel(USERS_FILE)
    username = input("Yuk buat username baru kamu: ").strip().lower()

    if not username:
        tampilkan_error("Duh, username nggak boleh kosong nih!")
        return

    # Mengecek apakah username sudah ada
    username_sudah_ada = False
    for u in users:
        if u["username"] == username:
            username_sudah_ada = True
            break

    if username_sudah_ada:
        tampilkan_error("Username itu sudah dipakai orang lain. Coba pakai nama lain ya.")
        return

    password = input("Masukkan password (minimal 5 karakter ya): ")

    if len(password) < 5:
        tampilkan_error("Passwordnya kependekan nih! Minimal harus 5 karakter.")
        return

    nama = input("Masukkan nama lengkap kamu: ").strip()
    users.append({
        "username": username,
        "password": str(password),
        "role": "customer",
        "nama": nama
    })
    save_excel(USERS_FILE, users)
    tampilkan_sukses("Hore! Akun kamu berhasil dibuat. Sekarang kamu sudah bisa login.")


def login():
    tampilkan_header("Login Bioskop")
    users = load_excel(USERS_FILE)
    username = input("Username: ").strip().lower()
    password = input("Password: ")

    for u in users:
        if str(u["username"]) == username and str(u["password"]) == str(password):
            tampilkan_sukses("Login berhasil! Selamat datang, " + u['nama'] + ".")
            return username, u["role"]

    tampilkan_error("Ups, username atau password kamu sepertinya salah.")
    return None, None


def change_password(username):
    users = load_excel(USERS_FILE)
    tampilkan_header("Ubah Password Akun")
    pwd_lama = input("Masukkan password lama kamu: ")

    ditemukan = False
    for u in users:
        if u["username"] == username:
            ditemukan = True
            if str(u["password"]) != str(pwd_lama):
                tampilkan_error("Password lama yang kamu masukkan kurang tepat nih.")
                return

            pwd_baru = input("Masukkan password baru (minimal 5 karakter): ")
            if len(pwd_baru) < 5:
                tampilkan_error("Password baru kamu terlalu pendek! Minimal 5 karakter ya.")
                return

            u["password"] = str(pwd_baru)
            break

    if ditemukan:
        save_excel(USERS_FILE, users)
        tampilkan_sukses("Mantap, password kamu berhasil diperbarui!")