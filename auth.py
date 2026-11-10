from data_store import load_excel, save_excel, USERS_FILE

def register_customer():
    print("\n=== REGISTRASI PELANGGAN BARU ===")
    users = load_excel(USERS_FILE)
    username = input("Masukkan Username Baru: ").strip().lower()
    
    if not username:
        print("Error: Username tidak boleh kosong!")
        return
        
    if any(u["username"] == username for u in users):
        print("Error: Username sudah terdaftar! Gunakan username lain.")
        return
        
    password = input("Masukkan Password (min 5 karakter): ")
    try:
        if len(password) < 5:
            raise ValueError("Password terlalu pendek! Minimal 5 karakter.")
    except ValueError as e:
        print(f"Error: {e}")
        return
        
    nama = input("Masukkan Nama Lengkap: ").strip()
    users.append({
        "username": username,
        "password": str(password),
        "role": "customer",
        "nama": nama
    })
    save_excel(USERS_FILE, users)
    print("Registrasi akun berhasil! Silakan login.")

def login():
    print("\n=== SYSTEM LOGIN CINEMA ===")
    users = load_excel(USERS_FILE)
    username = input("Username: ").strip().lower()
    password = input("Password: ")
    
    for u in users:
        if str(u["username"]) == username and str(u["password"]) == str(password):
            print(f"Login Berhasil! Selamat datang, {u['nama']}.")
            return username, u["role"]
            
    print("Error: Username atau Password salah!")
    return None, None

def change_password(username):
    users = load_excel(USERS_FILE)
    print("\n=== UBAH PASSWORD AKUN ===")
    pwd_lama = input("Masukkan Password Lama: ")
    
    found = False
    for u in users:
        if u["username"] == username:
            found = True
            if str(u["password"]) != str(pwd_lama):
                print("Error: Password lama tidak sesuai!")
                return
            pwd_baru = input("Masukkan Password Baru: ")
            if len(pwd_baru) < 5:
                print("Error: Password baru minimal 5 karakter!")
                return
            u["password"] = str(pwd_baru)
            break
            
    if found:
        save_excel(USERS_FILE, users)
        print("Password berhasil diperbarui!")