import random
from datetime import datetime
from data_store import load_excel, save_excel, MOVIES_FILE, TRANSACTIONS_FILE
from prettytable import PrettyTable
import inquirer
from colorama import init, Fore, Style

init()

ABU = Fore.LIGHTBLACK_EX
HIJAU = Fore.GREEN
RESET = Style.RESET_ALL

HURUF_BARIS = "ABCDEFGH"
KURSI_PER_BARIS = 4


def tampilkan_header(judul):
    print()
    print("========================================")
    print(judul.upper().center(40))
    print("========================================")


def buat_kode_booking(kode_lama):
    karakter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    while True:
        acak = ""
        for urutan in range(6):
            acak = acak + random.choice(karakter)
        kode = "TKT-" + acak
        if kode not in kode_lama:
            return kode


def tampilkan_kursi(kapasitas, kursi_terisi):
    tampilkan_header("Layar Cinema")

    kursi_kosong = []
    kursi_ke = 0
    jumlah_baris = -(-kapasitas // KURSI_PER_BARIS)

    for indeks_baris in range(jumlah_baris):
        huruf_baris = HURUF_BARIS[indeks_baris]
        teks_baris = huruf_baris + " | "
        for nomor_kursi in range(1, KURSI_PER_BARIS + 1):
            kursi_ke = kursi_ke + 1
            if kursi_ke > kapasitas:
                break
            kode_kursi = huruf_baris + str(nomor_kursi)
            if kode_kursi in kursi_terisi:
                teks_baris = teks_baris + ABU + "[X]" + RESET + " "
            else:
                teks_baris = teks_baris + HIJAU + "[" + kode_kursi + "]" + RESET + " "
                kursi_kosong.append(kode_kursi)
        print(teks_baris)
    return kursi_kosong


def tampilkan_error(pesan):
    print("[!]", pesan)


def input_kursi(kursi_terisi, kursi_kosong, pertanyaan):
    while True:
        print()
        kursi = input(pertanyaan).strip().upper()
        if kursi == "BATAL":
            return None
        if kursi in kursi_terisi:
            tampilkan_error("Kursi sudah terisi. Pilih yang berwarna hijau.")
        elif kursi not in kursi_kosong:
            tampilkan_error("Kode kursi tidak valid.")
        else:
            return kursi


def tampilkan_tabel_pesanan(daftar_pesanan):
    tabel = PrettyTable()
    tabel.field_names = ["No", "Kode Booking", "Judul Film", "Jadwal", "Kursi", "Status"]
    nomor = 1
    for pesanan in daftar_pesanan:
        tabel.add_row([nomor, pesanan["booking_code"], pesanan["judul"],
                       pesanan["jadwal"], pesanan["kursi"], pesanan["status"]])
        nomor = nomor + 1
    print(tabel)


def pilih_pesanan_pending(username, judul_menu, pertanyaan):
    semua_transaksi = load_excel(TRANSACTIONS_FILE)

    daftar_pending = []
    for transaksi in semua_transaksi:
        if str(transaksi["username"]) == str(username) and transaksi["status"] == "Pending":
            daftar_pending.append(transaksi)

    if len(daftar_pending) == 0:
        print("[!] Tidak ada pesanan berstatus Pending.")
        return None, None

    tampilkan_header(judul_menu)
    tampilkan_tabel_pesanan(daftar_pending)

    pilihan_menu = []
    for pesanan in daftar_pending:
        pilihan_menu.append(pesanan["booking_code"] + " - " + pesanan["judul"])
    pilihan_menu.append("Batal")

    jawaban = inquirer.prompt([
        inquirer.List("pesanan", message=pertanyaan, choices=pilihan_menu)
    ])
    if not jawaban or jawaban["pesanan"] == "Batal":
        return None, None

    kode_dipilih = jawaban["pesanan"].split(" - ")[0]
    for pesanan in daftar_pending:
        if pesanan["booking_code"] == kode_dipilih:
            return semua_transaksi, pesanan


def cari_film(daftar_film, id_film):
    for film in daftar_film:
        if film["movie_id"] == id_film:
            return film
    return None


def make_reservation(username, pre_selected_movie_id=None):
    daftar_film = load_excel(MOVIES_FILE)
    semua_transaksi = load_excel(TRANSACTIONS_FILE)

    tampilkan_header("Reservasi Tiket Bioskop")

    film = None
    while film is None:
        if pre_selected_movie_id:
            id_film = pre_selected_movie_id
            pre_selected_movie_id = None
        else:
            id_film = input("Masukkan ID Film (atau 'batal'): ").strip().upper()
            if id_film == "BATAL":
                return
        film = cari_film(daftar_film, id_film)
        if film is None:
            tampilkan_error("ID Film tidak ditemukan.")

    daftar_jadwal = []
    for jam in str(film["jadwal"]).split(","):
        daftar_jadwal.append(jam.strip())

    tampilkan_header("Jadwal Tayang " + film["judul"])
    nomor = 1
    for jam in daftar_jadwal:
        print(str(nomor) + ".", jam)
        nomor = nomor + 1

    while True:
        input_jadwal = input("Pilih nomor jadwal (atau 'batal'): ").strip()
        if input_jadwal.lower() == "batal":
            return
        if input_jadwal.isdigit() and 1 <= int(input_jadwal) <= len(daftar_jadwal):
            jadwal = daftar_jadwal[int(input_jadwal) - 1]
            break
        tampilkan_error("Masukkan nomor jadwal yang ada di daftar.")

    kursi_terisi = []
    for transaksi in semua_transaksi:
        if (transaksi["movie_id"] == id_film
                and transaksi["jadwal"] == jadwal
                and transaksi["status"] != "Batal"):
            kursi_terisi.append(transaksi["kursi"])

    kursi_kosong = tampilkan_kursi(int(film["kapasitas"]), kursi_terisi)
    if len(kursi_kosong) == 0:
        tampilkan_error("Maaf, semua kursi untuk jadwal ini sudah penuh.")
        return

    kursi = input_kursi(kursi_terisi, kursi_kosong,
                        "Masukkan kode kursi (contoh: A1, atau 'batal'): ")
    if kursi is None:
        return

    kode_lama = []
    for transaksi in semua_transaksi:
        kode_lama.append(transaksi["booking_code"])
    kode_booking = buat_kode_booking(kode_lama)

    semua_transaksi.append({
        "booking_code": kode_booking,
        "username": username,
        "movie_id": id_film,
        "judul": film["judul"],
        "jadwal": jadwal,
        "kursi": kursi,
        "harga": film["harga"],
        "status": "Pending",
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M"),
    })
    save_excel(TRANSACTIONS_FILE, semua_transaksi)

    print()
    print("[Sukses] Reservasi berhasil dibuat!")
    print("Kode Booking      :", kode_booking)
    print("Status Pembayaran : Pending (konfirmasi pembayaran ke Admin)")


def view_customer_history(username):
    semua_transaksi = load_excel(TRANSACTIONS_FILE)

    riwayat_user = []
    for transaksi in semua_transaksi:
        if str(transaksi["username"]) == str(username):
            riwayat_user.append(transaksi)

    tampilkan_header("Riwayat Tiket Saya")
    if len(riwayat_user) == 0:
        print("Belum ada riwayat pemesanan tiket.")
        return

    tabel = PrettyTable()
    tabel.field_names = ["Kode Booking", "Judul Film", "Jadwal", "Kursi",
                         "Total Bayar", "Status", "Tanggal"]
    for transaksi in riwayat_user:
        harga = "Rp" + format(int(transaksi["harga"]), ",")
        tabel.add_row([transaksi["booking_code"], transaksi["judul"],
                       transaksi["jadwal"], transaksi["kursi"], harga,
                       transaksi["status"], transaksi["tanggal"]])
    print(tabel)


def change_seat_choice(username):
    semua_transaksi, pesanan = pilih_pesanan_pending(
        username, "Tukar Kursi (Belum Dibayar)",
        "Pilih pesanan yang kursinya mau diganti:")
    if pesanan is None:
        return

    film = cari_film(load_excel(MOVIES_FILE), pesanan["movie_id"])

    kursi_terisi = []
    for transaksi in semua_transaksi:
        if (transaksi["movie_id"] == pesanan["movie_id"]
                and transaksi["jadwal"] == pesanan["jadwal"]
                and transaksi["status"] != "Batal"
                and transaksi["booking_code"] != pesanan["booking_code"]):
            kursi_terisi.append(transaksi["kursi"])

    kursi_kosong = tampilkan_kursi(int(film["kapasitas"]), kursi_terisi)
    kursi_baru = input_kursi(kursi_terisi, kursi_kosong,
                             "Masukkan kode kursi baru (atau 'batal'): ")
    if kursi_baru is None:
        return

    pesanan["kursi"] = kursi_baru
    save_excel(TRANSACTIONS_FILE, semua_transaksi)
    print("[Sukses] Kursi berhasil diganti menjadi", kursi_baru)


def cancel_reservation(username):
    semua_transaksi, pesanan = pilih_pesanan_pending(
        username, "Batalkan Pesanan", "Pilih pesanan yang mau dibatalkan:")
    if pesanan is None:
        return

    pesanan["status"] = "Batal"
    save_excel(TRANSACTIONS_FILE, semua_transaksi)
    print("[Sukses] Pesanan", pesanan["booking_code"], "dibatalkan.")