from datetime import datetime
from data_store import load_excel, save_excel, MOVIES_FILE, USERS_FILE, TRANSACTIONS_FILE
from visualisasi import tampilkan_error, tampilkan_peringatan, tampilkan_sukses, tampilkan_header
from search_filter import tampilkan_tabel_film
from prettytable import PrettyTable


def tekan_enter():
    input("\nTekan Enter untuk kembali ke menu")


# untuk mengecek format jadwal yang dimasukkan admin
def cek_jadwal(teks):
    daftar_jam = []
    for potongan in teks.split(","):
        daftar_jam.append(potongan.strip())

    # jam harus dalam format HH:MM
    for jam in daftar_jam:
        if len(jam) != 5:
            return None
        try:
            datetime.strptime(jam, "%H:%M")
        except ValueError:
            return None
    return ", ".join(daftar_jam)


# ===== MANAJEMEN FILM =====
def tambah_film_baru():
    movies = load_excel(MOVIES_FILE)
    tampilkan_header("Tambah Film Baru")
    m_id = f"M{len(movies) + 1}"

    while True:
        judul = input("Masukkan Judul Film: ").strip()
        if judul:
            break
        tampilkan_error("Judul film tidak boleh kosong ya. Coba masukkan lagi!")

    while True:
        genre = input("Masukkan Genre: ").strip()
        ada_angka = False
        for huruf in genre:
            if huruf.isdigit():
                ada_angka = True

        if genre == "":
            tampilkan_error("Genre film tidak boleh kosong ya. Coba masukkan lagi!")
        elif ada_angka:
            tampilkan_error("Genre tidak boleh berupa angka ya. Coba masukkan lagi!")
        else:
            break

    while True:
        try:
            harga = int(input("Masukkan Harga Tiket (Rp): "))
            break
        except ValueError:
            tampilkan_error("Harga harus berupa angka ya. Coba masukkan lagi!")

    while True:
        try:
            kapasitas = int(input("Kapasitas Kursi Studio: "))
            break
        except ValueError:
            tampilkan_error("Kapasitas harus berupa angka ya. Coba masukkan lagi!")

    while True:
        studio = input("Masukkan Nama Studio (Contoh: Studio 1): ").strip()
        if studio == "":
            tampilkan_error("Nama studio tidak boleh kosong ya. Coba masukkan lagi!")
        else:
            break

    while True:
        jadwal = cek_jadwal(input("Jadwal Tayang (pisahkan dengan koma, contoh: 13:00, 16:00): ").strip())
        if jadwal:
            break
        tampilkan_error("Format jadwal ada yang salah! Pakai jam HH:MM dipisah koma, contoh: 13:00, 16:00")

    movies.append({
        "movie_id": m_id, "judul": judul, "genre": genre,
        "harga": harga, "studio": studio, "kapasitas": kapasitas, "jadwal": jadwal
    })
    save_excel(MOVIES_FILE, movies)
    tampilkan_sukses(f"Mantap! Film '{judul}' berhasil ditambahkan dengan ID: {m_id}")


def daftar_film():
    movies = load_excel(MOVIES_FILE)
    tampilkan_header("Daftar Film")
    if not movies:
        tampilkan_peringatan("Belum ada film yang terdaftar.")
        tekan_enter()
        return
    tampilkan_tabel_film(movies)
    tekan_enter()


def perbarui_detail_film():
    movies = load_excel(MOVIES_FILE)
    tampilkan_header("Update Harga / Jadwal Tayang Film")

    # tampilkan daftar film yang sedang tayang saat ini
    print("\nDaftar Film yang Sedang Tayang:")
    tampilkan_tabel_film(movies)

    while True:
        m_id = input("\nMasukkan ID Film yang mau diubah (atau 'batal'): ").strip().upper()
        if m_id == 'BATAL':
            return
        film_dipilih = next((m for m in movies if m["movie_id"] == m_id), None)
        if film_dipilih != None:
            break
        else:
            tampilkan_error("ID Film tidak ditemukan. Coba cek lagi daftar di atas ya.")

    print(f"Oke, kamu sedang mengedit Film: {film_dipilih['judul']}")

    while True:
        try:
            harga_baru = input(f"Harga Baru (Kosongkan jika tetap Rp{film_dipilih['harga']}): ")
            if harga_baru:
                film_dipilih["harga"] = int(harga_baru)
            break
        except ValueError:
            tampilkan_error("Harga harus berupa angka ya. Coba masukkan lagi!")

    while True:
        jadwal_baru = input("Jadwal Baru (Kosongkan jika tidak berubah, pisah koma): ").strip()
        if jadwal_baru == "":
            break
        hasil_jadwal = cek_jadwal(jadwal_baru)
        if hasil_jadwal:
            film_dipilih["jadwal"] = hasil_jadwal
            break
        tampilkan_error("Format jadwal ada yang salah! Pakai jam HH:MM dipisah koma, contoh: 13:00, 16:00")

    save_excel(MOVIES_FILE, movies)
    tampilkan_sukses("Selesai! Data film berhasil diperbarui!")


def hapus_film():
    movies = load_excel(MOVIES_FILE)
    tampilkan_header("Hapus Film (Turun layar)")

    # tampilkan daftar film yang sedang tayang saat ini
    print("\nDaftar Film yang Sedang Tayang:")
    tampilkan_tabel_film(movies)

    while True:
        m_id = input("\nMasukkan ID Film yang akan dihapus (atau 'batal'): ").strip().upper()
        if m_id == 'BATAL':
            return

        film_baru = []
        for m in movies:
            if m["movie_id"] != m_id:
                film_baru.append(m)
        if len(film_baru) < len(movies):
            save_excel(MOVIES_FILE, film_baru)
            tampilkan_sukses(f"Film dengan ID {m_id} berhasil dihapus dari sistem.")
            break
        else:
            tampilkan_error("ID Film tidak ditemukan. Coba cek lagi daftar di atas ya.")


def management_film():
    while True:
        tampilkan_header("Management Film")
        print("1. Daftar Film")
        print("2. Tambah Film Baru")
        print("3. Update Harga / Jadwal Tayang")
        print("4. Hapus Film Turun Layar")
        print("5. Kembali")

        pilihan = input("Pilih menu (1-5): ").strip()

        if pilihan == "1":
            daftar_film()
        elif pilihan == "2":
            tambah_film_baru()
        elif pilihan == "3":
            perbarui_detail_film()
        elif pilihan == "4":
            hapus_film()
        elif pilihan == "5":
            return
        else:
            tampilkan_error("Pilihan menu tidak valid. Masukkan angka 1 sampai 5.")


# ===== MANAJEMEN PELANGGAN =====
def tampilkan_tabel_pelanggan(users):
    table = PrettyTable()
    table.field_names = ["Username", "Nama Lengkap", "Role"]

    for u in users:
        if u["role"] == "customer":
            table.add_row([u["username"], u["nama"], u["role"]])
    print(table)

def lihat_semua_pelanggan():
    users = load_excel(USERS_FILE)
    tampilkan_header("Daftar Pelanggan yang Terdaftar")
    tampilkan_tabel_pelanggan(users)
    tekan_enter()


def hapus_akun_pelanggan():
    users = load_excel(USERS_FILE)
    tampilkan_header("Hapus Akun Pelanggan")
    
    print("\nDaftar Pelanggan yang Terdaftar:")
    tampilkan_tabel_pelanggan(users)
    

    while True:
        usn = input("Masukkan Username Pelanggan yang mau dihapus (atau 'batal'): ").strip().lower()
        if usn == 'batal':
            return

        user_baru = []
        for u in users:
            if u["username"] == usn and u["role"] == "customer":
                pass
            else:
                user_baru.append(u)
        if len(user_baru) < len(users):
            save_excel(USERS_FILE, user_baru)
            tampilkan_sukses(f"Akun pelanggan '{usn}' berhasil dihapus.")
            break
        else:
            tampilkan_error("Username tidak ditemukan atau itu akun Admin yang tidak bisa dihapus. Coba cek lagi ya.")


def management_pelanggan():
    while True:
        tampilkan_header("Management Pelanggan")
        print("1. Lihat Semua Pelanggan")
        print("2. Hapus Akun Pelanggan")
        print("3. Kembali")

        pilihan = input("Pilih menu (1-3): ").strip()

        if pilihan == "1":
            lihat_semua_pelanggan()
        elif pilihan == "2":
            hapus_akun_pelanggan()
        elif pilihan == "3":
            return
        else:
            tampilkan_error("Pilihan menu tidak valid. Silakan masukkan lagi angka 1 sampai 3.")


def lihat_dan_ubah_transaksi():
    transaksi = load_excel(TRANSACTIONS_FILE)
    tampilkan_header("Rekapitulasi & Update Status Transaksi")

    if not transaksi:
        tampilkan_peringatan("Belum ada transaksi tiket masuk.")
        return

    table = PrettyTable()
    table.field_names = ["Kode Booking", "Pelanggan", "Judul Film", "Harga", "Status"]
    for t in transaksi:
        table.add_row([t["booking_code"], t["username"], t["judul"], f"Rp{int(t['harga']):,}", t["status"]])
    print(table)

    while True:
        pilihan = input("\nApakah kamu mau ubah status pembayaran pelanggan? (y/n): ").strip().lower()
        if pilihan in ['y', 'n']:
            break
        tampilkan_error("Ketik 'y' untuk ya atau 'n' untuk tidak.")

    if pilihan == 'n':
        return

    while True:
        kode_input = input("Masukkan Kode Booking (atau 'batal'): ").strip().upper()
        if kode_input == 'BATAL':
            return
        transaksi_dipilih = next((t for t in transaksi if t["booking_code"] == kode_input), None)
        if transaksi_dipilih != None:
            break
        else:
            tampilkan_error("Kode Booking tidak ditemukan. coba cek lagi tabel di atas ya.")

    while True:
        print("Pilih Status Baru: 1. Lunas | 2. Pending | 3. Batal")
        st = input("Pilihan (1-3): ").strip()
        status_map = {"1": "Lunas", "2": "Pending", "3": "Batal"}
        if st in status_map:
            transaksi_dipilih["status"] = status_map[st]
            save_excel(TRANSACTIONS_FILE, transaksi)
            tampilkan_sukses(f"Status transaksi {kode_input} sudah diubah menjadi {status_map[st]}!")
            break
        else:
            tampilkan_error("Pilihan status tidak valid. Masukkan angka 1 sampai 3.")