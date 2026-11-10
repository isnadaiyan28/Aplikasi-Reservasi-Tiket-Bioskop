import random
from datetime import datetime
from data_store import load_excel, save_excel, MOVIES_FILE, TRANSACTIONS_FILE
from prettytable import PrettyTable
import inquirer
from colorama import init, Fore, Style

init(autoreset=True)

def generate_booking_code(existing_codes):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    code = "TKT-" + "".join(random.choice(chars) for _ in range(6))
    if code in existing_codes:
        return generate_booking_code(existing_codes)
    return code

def render_seat_map(kapasitas, occupied_seats):
    print(f"\n{Fore.CYAN}  [ LAYAR CINEMA ]  {Style.RESET_ALL}")
    print("--------------------")
    rows = "ABCDEFGH"
    row_count = (kapasitas // 4) + (1 if kapasitas % 4 != 0 else 0)
    
    available_seats = []
    seat_idx = 0
    for r in range(row_count):
        row_str = f"{rows[r]} | "
        for c in range(1, 5):
            seat_idx += 1
            if seat_idx > kapasitas:
                break
            seat_code = f"{rows[r]}{c}"
            if seat_code in occupied_seats:
                # Poin 9: Kursi terisi berwarna abu-abu dengan simbol [X]
                row_str += f"{Fore.LIGHTBLACK_EX}[X]{Style.RESET_ALL} "
            else:
                # Kursi kosong berwarna hijau
                row_str += f"{Fore.GREEN}[{seat_code}]{Style.RESET_ALL} "
                available_seats.append(seat_code)
        print(row_str)
    return available_seats

def make_reservation(username, pre_selected_movie_id=None):
    movies = load_excel(MOVIES_FILE)
    transactions = load_excel(TRANSACTIONS_FILE)
    
    print("\n=== RESERVASI TIKET BIOSKOP ===")
    
    while True:
        if pre_selected_movie_id:
            movie_id = pre_selected_movie_id
            pre_selected_movie_id = None 
        else:
            movie_id = input("Masukkan ID Film yang ingin dipesan (atau ketik 'batal'): ").strip().upper()
            if movie_id == 'BATAL':
                return
                
        selected_movie = next((m for m in movies if m["movie_id"] == movie_id), None)
        if selected_movie:
            break
        print(f"{Fore.RED}[!] Error: ID Film tidak ditemukan.{Style.RESET_ALL}")

    jadwal_list = [j.strip() for j in str(selected_movie["jadwal"]).split(",")]
    print(f"\nJadwal Tayang {selected_movie['judul']}:")
    for idx, j in enumerate(jadwal_list, 1):
        print(f"{idx}. {j}")
        
    while True: 
        j_input = input("Pilih Nomor Jadwal (atau ketik 'batal'): ").strip()
        if j_input.lower() == 'batal':
            return
        try:
            j_choice = int(j_input) - 1
            if 0 <= j_choice < len(jadwal_list):
                jadwal = jadwal_list[j_choice]
                break
            print(f"{Fore.RED}[!] Nomor jadwal tidak ada dalam daftar.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}[!] Harap masukkan angka yang valid!{Style.RESET_ALL}")

    occupied_seats = [
        t["kursi"] for t in transactions
        if t["movie_id"] == movie_id and t["jadwal"] == jadwal and t["status"] != "Batal"
    ]
    
    available_seats = render_seat_map(int(selected_movie["kapasitas"]), occupied_seats)
    
    if not available_seats:
        print(f"{Fore.RED}[!] Maaf, semua kursi untuk jadwal ini sudah penuh!{Style.RESET_ALL}")
        return

    while True:
        pilih_kursi = input("\nMasukkan Kode Kursi pilihan Anda (contoh: A1, atau ketik 'batal'): ").strip().upper()
        if pilih_kursi == 'BATAL':
            return
        if pilih_kursi in occupied_seats:
            print(f"{Fore.RED}[!] Kursi {pilih_kursi} sudah terisi ([X]). Silakan pilih kursi lain yang berwarna hijau.{Style.RESET_ALL}")
        elif pilih_kursi not in available_seats:
            print(f"{Fore.RED}[!] Kode kursi tidak valid atau diluar kapasitas studio.{Style.RESET_ALL}")
        else:
            break

    existing_codes = {t["booking_code"] for t in transactions}
    booking_code = generate_booking_code(existing_codes)
    now_str = datetime.now().strftime("%d-%m-%Y %H:%M")
    
    transactions.append({
        "booking_code": booking_code,
        "username": username,
        "movie_id": movie_id,
        "judul": selected_movie["judul"],
        "jadwal": jadwal,
        "kursi": pilih_kursi,
        "harga": selected_movie["harga"],
        "status": "Pending",
        "tanggal": now_str
    })
    
    save_excel(TRANSACTIONS_FILE, transactions)
    print(f"\n{Fore.GREEN}[Sukses] Reservasi Berhasil dibuat!{Style.RESET_ALL}")
    print(f"Kode Booking Anda : {booking_code}")
    print("Status Pembayaran : Pending (Silakan konfirmasi pembayaran ke Admin)")

def view_customer_history(username):
    transactions = load_excel(TRANSACTIONS_FILE)
    user_tx = [t for t in transactions if t["username"] == username]
    
    print("\n=== RIWAYAT TIKET PESANAN SAYA ===")
    if not user_tx:
        print("Belum ada riwayat pemesanan tiket.")
        return
        
    table = PrettyTable()
    table.field_names = ["Kode Booking", "Judul Film", "Jadwal", "Kursi", "Total Bayar", "Status", "Tanggal"]
    for t in user_tx:
        table.add_row([
            t["booking_code"], t["judul"], t["jadwal"], t["kursi"], 
            f"Rp{int(t['harga']):,}", t["status"], t["tanggal"]
        ])
    print(table)

def change_seat_choice(username):
    transactions = load_excel(TRANSACTIONS_FILE)
    pending_tx = [t for t in transactions if t["username"] == username and t["status"] == "Pending"]
    
    if not pending_tx:
        print(f"{Fore.YELLOW}[!] Tidak ada pesanan berstatus 'Pending' yang dapat diubah kursinya.{Style.RESET_ALL}")
        return
        
    print("\n=== TUKAR PILIHAN KURSI (BELUM DIBAYAR) ===")
    
    # Menampilkan tabel/daftar pesanan pending user secara jelas terlebih dahulu
    table = PrettyTable()
    table.field_names = ["No", "Kode Booking", "Judul Film", "Jadwal", "Kursi", "Status"]
    for idx, t in enumerate(pending_tx, 1):
        table.add_row([idx, t['booking_code'], t['judul'], t['jadwal'], t['kursi'], t['status']])
    print(table)
    
    booking_choices = [
        f"{t['booking_code']} - {t['judul']} (Kursi: {t['kursi']})" for t in pending_tx
    ]
    booking_choices.append("Batal")
    
    questions = [
        inquirer.List(
            'booking',
            message="Pilih pesanan yang ingin diubah kursinya:",
            choices=booking_choices,
        ),
    ]
    answer = inquirer.prompt(questions)
    if not answer or answer['booking'] == "Batal":
        return
        
    code_choice = answer['booking'].split(" - ")[0]
    selected_tx = next((t for t in pending_tx if t["booking_code"] == code_choice), None)
        
    movies = load_excel(MOVIES_FILE)
    movie_info = next((m for m in movies if m["movie_id"] == selected_tx["movie_id"]), {})
    
    occupied = [
        t["kursi"] for t in transactions
        if t["movie_id"] == selected_tx["movie_id"] and t["jadwal"] == selected_tx["jadwal"] 
        and t["status"] != "Batal" and t["booking_code"] != code_choice
    ]
    
    available_seats = render_seat_map(int(movie_info.get("kapasitas", 12)), occupied)
    
    while True:
        kursi_baru = input("\nMasukkan Kode Kursi Baru pilihan Anda (atau 'batal'): ").strip().upper()
        if kursi_baru == 'BATAL':
            return
        if kursi_baru in occupied:
            print(f"{Fore.RED}[!] Kursi tersebut sudah terisi! Pilih kursi lain yang berwarna hijau.{Style.RESET_ALL}")
        elif kursi_baru not in available_seats:
            print(f"{Fore.RED}[!] Kode kursi tidak valid.{Style.RESET_ALL}")
        else:
            break
        
    for t in transactions:
        if t["booking_code"] == code_choice:
            t["kursi"] = kursi_baru
            break
            
    save_excel(TRANSACTIONS_FILE, transactions)
    print(f"{Fore.GREEN}[Sukses] Kursi berhasil ditukar menjadi {kursi_baru}!{Style.RESET_ALL}")

def cancel_reservation(username):
    transactions = load_excel(TRANSACTIONS_FILE)
    pending_tx = [t for t in transactions if t["username"] == username and t["status"] == "Pending"]
    
    if not pending_tx:
        print(f"{Fore.YELLOW}[!] Tidak ada pesanan berstatus 'Pending' yang dapat dibatalkan.{Style.RESET_ALL}")
        return
        
    print("\n=== BATALKAN PESANAN TIKET ===")
    
    # Menampilkan tabel/daftar pesanan pending user secara jelas terlebih dahulu
    table = PrettyTable()
    table.field_names = ["No", "Kode Booking", "Judul Film", "Jadwal", "Kursi", "Status"]
    for idx, t in enumerate(pending_tx, 1):
        table.add_row([idx, t['booking_code'], t['judul'], t['jadwal'], t['kursi'], t['status']])
    print(table)
    
    booking_choices = [
        f"{t['booking_code']} - {t['judul']} [Kursi {t['kursi']}]" for t in pending_tx
    ]
    booking_choices.append("Batal")
    
    questions = [
        inquirer.List(
            'booking',
            message="Pilih pesanan yang ingin dibatalkan:",
            choices=booking_choices,
        ),
    ]
    answer = inquirer.prompt(questions)
    if not answer or answer['booking'] == "Batal":
        return
        
    code_choice = answer['booking'].split(" - ")[0]
    
    for t in transactions:
        if t["booking_code"] == code_choice and t["username"] == username and t["status"] == "Pending":
            t["status"] = "Batal"
            break
            
    save_excel(TRANSACTIONS_FILE, transactions)
    print(f"{Fore.GREEN}[Sukses] Pesanan {code_choice} berhasil dibatalkan!{Style.RESET_ALL}")