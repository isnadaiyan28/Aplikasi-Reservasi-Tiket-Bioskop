from data_store import init_storage
from auth import login, register_customer, change_password
from search_filter import search_and_filter_movies
from customer_features import view_customer_history, change_seat_choice, cancel_reservation
from admin_features import (add_new_movie, update_movie_detail, delete_movie, 
                            view_all_customers, delete_customer_account, view_and_update_transactions)
from visualisasi import show_sales_analytics

def main():
    init_storage()
    current_user = None
    user_role = None

    while True:
        if not current_user:
            print("\n=========================================")
            print("  APLIKASI RESERVASI TIKET BIOSKOP")
            print("=========================================")
            print("1. Login Akun")
            print("2. Registrasi Pelanggan Baru")
            print("3. Cari & Lihat Film (Guest/Public)")
            print("4. Keluar Program")
            
            pilihan = input("Pilih Menu (1-4): ").strip()

            if pilihan == "1":
                current_user, user_role = login()
            elif pilihan == "2":
                register_customer()
            elif pilihan == "3":
                current_user = search_and_filter_movies(current_user)
                if current_user:
                    user_role = "customer"
            elif pilihan == "4":
                print("Terima kasih telah menggunakan sistem bioskop!")
                break
            else:
                print("\n[!] Error: Pilihan menu tidak valid! Harap masukkan angka 1 sampai 4.")

        elif user_role == "admin":
            print(f"\n--- MENU UTAMA ADMIN ({current_user}) ---")
            print("1. Tambah Film Baru (Create)")
            print("2. Update Harga / Jadwal Tayang (Update)")
            print("3. Hapus Film Turun Layar (Delete)")
            print("4. Lihat Daftar Pelanggan Terdaftar (Read)")
            print("5. Hapus Akun Pelanggan Palsu (Delete)")
            print("6. Rekapitulasi & Update Status Transaksi (Read/Update)")
            print("7. Analytics & Visualisasi Pendapatan (Modul 9)")
            print("8. Logout")
            
            pilihan = input("Pilih Menu Admin (1-8): ").strip()

            if pilihan == "1": add_new_movie()
            elif pilihan == "2": update_movie_detail()
            elif pilihan == "3": delete_movie()
            elif pilihan == "4": view_all_customers()
            elif pilihan == "5": delete_customer_account()
            elif pilihan == "6": view_and_update_transactions()
            elif pilihan == "7": show_sales_analytics()
            elif pilihan == "8": current_user = user_role = None
            else:
                print("\n[!] Error: Pilihan menu admin tidak valid! Masukkan angka 1-8.")

        elif user_role == "customer":
            # Menu Reservasi Tiket terpisah sudah dihapus dan disatukan di dalam menu Cari & Filter Film
            print(f"\n--- MENU UTAMA PELANGGAN ({current_user}) ---")
            print("1. Cari & Filter Film Tayang & Pesan Tiket")
            print("2. Lihat Riwayat Pesanan Tiket (Read)")
            print("3. Tukar Pilihan Kursi [Pending Payment] (Update)")
            print("4. Batalkan Pesanan Tiket (Delete)")
            print("5. Ubah Password Akun (Update)")
            print("6. Logout")
            
            pilihan = input("Pilih Menu Pelanggan (1-6): ").strip()

            if pilihan == "1": search_and_filter_movies(current_user)
            elif pilihan == "2": view_customer_history(current_user)
            elif pilihan == "3": change_seat_choice(current_user)
            elif pilihan == "4": cancel_reservation(current_user)
            elif pilihan == "5": change_password(current_user)
            elif pilihan == "6": current_user = user_role = None
            else:
                print("\n[!] Error: Pilihan menu pelanggan tidak valid! Masukkan angka 1-6.")

if __name__ == "__main__":
    main()