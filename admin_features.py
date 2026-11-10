from data_store import load_excel, save_excel, MOVIES_FILE, USERS_FILE, TRANSACTIONS_FILE
from search_filter import display_movie_table
from prettytable import PrettyTable

def add_new_movie():
    movies = load_excel(MOVIES_FILE)
    print("\n=== TAMBAH FILM BARU ===")
    m_id = f"M{len(movies) + 1}"
    judul = input("Masukkan Judul Film: ").strip()
    genre = input("Masukkan Genre: ").strip()
    
    while True:
        try:
            harga = int(input("Masukkan Harga Tiket (Rp): "))
            break
        except ValueError:
            print("[!] Error: Harga harus berupa angka!")
            
    while True:
        try:
            kapasitas = int(input("Kapasitas Kursi Studio: "))
            break
        except ValueError:
            print("[!] Error: Kapasitas harus berupa angka!")
        
    studio = input("Nama Studio (Contoh: Studio 1): ").strip()
    jadwal = input("Jadwal Tayang (pisahkan dengan koma, contoh: 13:00, 16:00): ").strip()
    
    movies.append({
        "movie_id": m_id, "judul": judul, "genre": genre,
        "harga": harga, "studio": studio, "kapasitas": kapasitas, "jadwal": jadwal
    })
    save_excel(MOVIES_FILE, movies)
    print(f"[Sukses] Film '{judul}' berhasil ditambahkan dengan ID: {m_id}")

def update_movie_detail():
    movies = load_excel(MOVIES_FILE)
    print("\n=== UPDATE JAM TAYANG / HARGA TIKET ===")
    
    # Poin 4: Tampilkan daftar film yang sedang tayang saat ini
    print("\nDaftar Film yang Sedang Tayang:")
    display_movie_table(movies)
    
    while True:
        m_id = input("\nMasukkan ID Film yang diubah (atau 'batal'): ").strip().upper()
        if m_id == 'BATAL':
            return
        selected_movie = next((m for m in movies if m["movie_id"] == m_id), None)
        if selected_movie:
            break
        print("[!] Error: ID Film tidak ditemukan.")
        
    print(f"Mengedit Film: {selected_movie['judul']}")
    while True:
        try:
            harga_baru = input(f"Harga Baru (Kosongkan jika tetap Rp{selected_movie['harga']}): ")
            if harga_baru:
                selected_movie["harga"] = int(harga_baru)
            break
        except ValueError:
            print("[!] Error: Input harga harus berupa angka!")
            
    jadwal_baru = input("Jadwal Baru (Kosongkan jika tidak berubah, pisah koma): ")
    if jadwal_baru:
        selected_movie["jadwal"] = jadwal_baru.strip()
        
    save_excel(MOVIES_FILE, movies)
    print("[Sukses] Data film berhasil diperbarui!")

def delete_movie():
    movies = load_excel(MOVIES_FILE)
    print("\n=== HAPUS FILM (TURUN LAYAR) ===")
    
    # Poin 4: Tampilkan daftar film yang sedang tayang saat ini
    print("\nDaftar Film yang Sedang Tayang:")
    display_movie_table(movies)
    
    while True:
        m_id = input("\nMasukkan ID Film yang akan dihapus (atau 'batal'): ").strip().upper()
        if m_id == 'BATAL':
            return
            
        new_movies = [m for m in movies if m["movie_id"] != m_id]
        if len(new_movies) < len(movies):
            save_excel(MOVIES_FILE, new_movies)
            print(f"[Sukses] Film dengan ID {m_id} berhasil dihapus dari sistem.")
            break
        else:
            print("[!] Error: ID Film tidak ditemukan.")

def view_all_customers():
    users = load_excel(USERS_FILE)
    print("\n=== DAFTAR PELANGGAN TERDAFTAR ===")
    table = PrettyTable()
    table.field_names = ["Username", "Nama Lengkap", "Role"]
    
    for u in users:
        if u["role"] == "customer":
            table.add_row([u["username"], u["nama"], u["role"]])
    print(table)

def delete_customer_account():
    users = load_excel(USERS_FILE)
    print("\n=== HAPUS AKUN PELANGGAN (PALSU/AKUN FAKE) ===")
    
    while True:
        usn = input("Masukkan Username Pelanggan yang akan dihapus (atau 'batal'): ").strip().lower()
        if usn == 'batal':
            return
            
        new_users = [u for u in users if not (u["username"] == usn and u["role"] == "customer")]
        if len(new_users) < len(users):
            save_excel(USERS_FILE, new_users)
            print(f"[Sukses] Akun pelanggan '{usn}' berhasil dihapus.")
            break
        else:
            print("[!] Error: Username tidak ditemukan atau merupakan akun Admin.")

def view_and_update_transactions():
    transactions = load_excel(TRANSACTIONS_FILE)
    print("\n=== REKAPITULASI & KONFIRMASI TRANSAKSI ===")
    
    if not transactions:
        print("Belum ada transaksi tiket masuk.")
        return
        
    table = PrettyTable()
    table.field_names = ["Kode Booking", "Pelanggan", "Judul Film", "Harga", "Status"]
    for t in transactions:
        table.add_row([t["booking_code"], t["username"], t["judul"], f"Rp{int(t['harga']):,}", t["status"]])
    print(table)
    
    while True:
        pilihan = input("\nUbah status pembayaran pelanggan? (y/n): ").strip().lower()
        if pilihan in ['y', 'n']:
            break
        print("[!] Masukkan 'y' atau 'n'.")
        
    if pilihan == 'y':
        while True:
            code_input = input("Masukkan Kode Booking (atau 'batal'): ").strip().upper()
            if code_input == 'BATAL':
                return
            selected_tx = next((t for t in transactions if t["booking_code"] == code_input), None)
            if selected_tx:
                break
            print("[!] Error: Kode Booking tidak ditemukan.")
            
        while True:
            print("Pilih Status Baru: 1. Lunas | 2. Pending | 3. Batal")
            st = input("Pilihan (1-3): ").strip()
            status_map = {"1": "Lunas", "2": "Pending", "3": "Batal"}
            if st in status_map:
                selected_tx["status"] = status_map[st]
                save_excel(TRANSACTIONS_FILE, transactions)
                print(f"[Sukses] Status transaksi {code_input} diubah menjadi {status_map[st]}!")
                break
            else:
                print("[!] Error: Pilihan status tidak valid. Masukkan angka 1 sampai 3.")