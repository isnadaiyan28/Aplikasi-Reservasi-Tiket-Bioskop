from data_store import USERS_FILE, init_storage, load_excel
from auth import login, register_customer, change_password
from search_filter import search_and_filter_movies
from customer_features import view_customer_history, change_seat_choice, cancel_reservation, tampilkan_header
from admin_features import (add_new_movie, update_movie_detail, delete_movie, 
                            view_all_customers, delete_customer_account, view_and_update_transactions)
from visualisasi import show_sales_analytics

def main():
    init_storage()
    current_user = None
    user_role = None

    while True:
        if not current_user:
            tampilkan_header("APLIKASI RESERVASI TIKET BIOSKOP")
            print("1. Login Akun")
            print("2. Registrasi Pelanggan Baru")
            print("3. Cari & Lihat Film (Guest/Public)")
            print("4. Keluar Program")

            pilihan = input("pilih menu (1-4): ").strip()

            if pilihan == "1":
                current_user, user_role = login()
            elif pilihan == "2":
                register_customer()
            elif pilihan == "3":
                nama_tamu = search_and_filter_movies(None)

                if nama_tamu:
                    daftar_pengguna = load_excel(USERS_FILE)
                    apakah_admin = False

                    for akun in daftar_pengguna:
                        if akun.get("username") == nama_tamu and akun.get("role") == "admin":
                            apakah_admin = True
                            break

                    if apakah_admin:
                        print("\n[!] Akun admin tidak dapat memesan tiket dari menu tamu.")
                        print("[!] Silakan login sebagai pelanggan untuk memesan tiket.")
                    else:
                        current_user = nama_tamu
                        user_role = "customer"
                        print(f"\n[!] Selamat datang, {current_user}! Anda sekarang dapat memesan tiket.")
            elif pilihan == "4":
                print("Terima kasih telah menggunakan sistem bioskop!")
                break
            else:
                print("\n[!] Error: Pilihan menu tidak valid! Harap masukkan angka 1 sampai 4.")

def menu_admin(current_user):
        tampilkan_header(f"MENU UTAMA ADMIN - {current_user}")
        print("1. Tambah Film Baru")
        print("2. Update Harga / Jadwal Tayang")
        print("3. Hapus Film Turun Layar")
        print("4. Lihat Daftar Pelanggan Terdaftar")
        print("5. Hapus Akun Pelanggan Palsu")
        print("6. Rekapitulasi & Update Status Transaksi")
        print("7. Analytics & Visualisasi Pendapatan")
        print("8. Logout")

        pilihan = input("Pilih Menu Admin (1-8): ").strip()

        if pilihan == "1":
            add_new_movie()
        elif pilihan == "2":
            update_movie_detail()
        elif pilihan == "3":
            delete_movie()
        elif pilihan == "4":
            view_all_customers()
        elif pilihan == "5":
            delete_customer_account()
        elif pilihan == "6":
            view_and_update_transactions()
        elif pilihan == "7":
            show_sales_analytics()
        elif pilihan == "8":
            print("\n[✓] Berhasil logout dari akun admin.")
            return None, None
        else:
            print("\n[!] Error: Pilihan menu admin tidak valid! Harap masukkan angka 1 sampai 8.")

        return current_user, "admin"

def menu_customer(current_user):
        tampilkan_header(f"MENU UTAMA PELANGGAN - {current_user}")
        print("1. Cari & Filter Film Tayang & Pesan Tiket")
        print("2. Lihat Riwayat Pesanan Tiket")
        print("3. Tukar Pilihan Kursi [Pending Payment]")
        print("4. Batalkan Pesanan Tiket")
        print("5. Ubah Password Akun")
        print("6. Logout")

        pilihan = input("Pilih Menu Pelanggan (1-6): ").strip()
        if pilihan == "1":
            search_and_filter_movies(current_user)
        elif pilihan == "2":
            view_customer_history(current_user)
        elif pilihan == "3":
            change_seat_choice(current_user)
        elif pilihan == "4":
            cancel_reservation(current_user)
        elif pilihan == "5":
            change_password(current_user)
        elif pilihan == "6":
            print("\n[✓] Berhasil logout dari akun pelanggan.")
            return None, None
        else:
            print("\n[!] Error: Pilihan menu pelanggan tidak valid! Harap masukkan angka 1 sampai 6.")

        return current_user, "customer"

if __name__ == "__main__":
    main()