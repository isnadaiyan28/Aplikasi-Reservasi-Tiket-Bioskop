from data_store import load_excel, MOVIES_FILE
from prettytable import PrettyTable
import customer_features
from colorama import init, Fore, Style

init(autoreset=True)

def search_and_filter_movies(current_user=None):
    movies = load_excel(MOVIES_FILE)
    if not movies:
        print(f"{Fore.YELLOW}Belum ada film yang sedang tayang.{Style.RESET_ALL}")
        return current_user

    while True:
        print("\n=== PENCARIAN & FILTER FILM ===")
        print("1. Cari Berdasarkan Judul")
        print("2. Filter Berdasarkan Genre")
        print("3. Tampilkan Semua Film")
        print("4. Kembali ke Menu Utama")
        
        pilihan = input("Pilih Menu (1-4): ").strip()

        filtered = []
        if pilihan == "1":
            keyword = input("Masukkan kata kunci judul (atau ketik 'batal'): ").strip().lower()
            if keyword == 'batal':
                continue
            filtered = [m for m in movies if keyword in str(m["judul"]).lower()]
        elif pilihan == "2":
            genres = list({m["genre"] for m in movies})
            print("\nDaftar Genre Tersedia:")
            for idx, g in enumerate(genres, 1):
                print(f"{idx}. {g}")
            
            while True:
                g_input = input("Pilih Nomor Genre (atau ketik 'batal'): ").strip()
                if g_input.lower() == 'batal':
                    filtered = None
                    break
                try:
                    g_idx = int(g_input) - 1
                    if 0 <= g_idx < len(genres):
                        selected_genre = genres[g_idx]
                        filtered = [m for m in movies if str(m["genre"]).lower() == selected_genre.lower()]
                        break
                    else:
                        print(f"{Fore.RED}[!] Nomor genre tidak ada dalam daftar.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}[!] Error: Harap masukkan angka yang valid!{Style.RESET_ALL}")
            if filtered is None:
                continue
        elif pilihan == "3":
            filtered = movies
        elif pilihan == "4":
            break
        else:
            print(f"{Fore.RED}[!] Pilihan tidak valid. Harap masukkan angka 1 sampai 4.{Style.RESET_ALL}")
            continue

        # Poin 3: Jika film tidak ditemukan, beri opsi cari lagi
        if not filtered:
            print(f"\n{Fore.YELLOW}[!] Film yang Anda cari tidak ditemukan.{Style.RESET_ALL}")
            while True:
                sub_pilih = input("Apakah ingin mencoba mencari lagi? (y/n): ").strip().lower()
                if sub_pilih in ['y', 'n']:
                    break
                print(f"{Fore.RED}[!] Masukkan pilihan yang valid ('y' atau 'n').{Style.RESET_ALL}")
            if sub_pilih == 'y':
                continue
            else:
                break
        else:
            display_movie_table(filtered)
            
            # Poin 5: Integrasi Reservasi di dalam lihat detail film
            while True:
                m_id = input("\nMasukkan ID Film untuk melihat detail/pesan (atau ketik 'batal'): ").strip().upper()
                if m_id == 'BATAL':
                    break
                
                selected_movie = next((m for m in filtered if m["movie_id"] == m_id), None)
                if selected_movie:
                    print(f"\n--- DETAIL FILM: {selected_movie['judul']} ---")
                    print(f"Genre    : {selected_movie['genre']}")
                    print(f"Studio   : {selected_movie['studio']}")
                    print(f"Harga    : Rp{selected_movie['harga']:,}")
                    print(f"Jadwal   : {selected_movie['jadwal']}")
                    
                    # Poin 2: Redirect ke login jika guest ingin pesan
                    if not current_user:
                        print(f"\n{Fore.YELLOW}[!] Anda harus login terlebih dahulu untuk melakukan reservasi tiket.{Style.RESET_ALL}")
                        while True:
                            opsi_login = input("Ingin login sekarang? (y/n): ").strip().lower()
                            if opsi_login in ['y', 'n']:
                                break
                            print(f"{Fore.RED}[!] Masukkan 'y' atau 'n'.{Style.RESET_ALL}")
                            
                        if opsi_login == 'y':
                            from auth import login
                            usr, role = login()
                            if usr:
                                current_user = usr
                                customer_features.make_reservation(current_user, pre_selected_movie_id=m_id)
                        else:
                            print("Reservasi dibatalkan.")
                    else:
                        while True:
                            pesan = input("Ingin memesan tiket untuk film ini? (y/n): ").strip().lower()
                            if pesan in ['y', 'n']:
                                break
                            print(f"{Fore.RED}[!] Masukkan 'y' atau 'n'.{Style.RESET_ALL}")
                            
                        if pesan == 'y':
                            customer_features.make_reservation(current_user, pre_selected_movie_id=m_id)
                    break
                else:
                    print(f"{Fore.RED}[!] ID Film tidak ditemukan. Silakan masukkan ID yang benar.{Style.RESET_ALL}")
            
            while True:
                lanjut = input("\nKeluar dari menu pencarian? (y/n): ").strip().lower()
                if lanjut in ['y', 'n']:
                    break
                print(f"{Fore.RED}[!] Masukkan 'y' atau 'n'.{Style.RESET_ALL}")
            if lanjut == 'y':
                break
                
    return current_user

def display_movie_table(movies_list):
    table = PrettyTable()
    table.field_names = ["ID Film", "Judul Film", "Genre", "Studio", "Harga (Rp)", "Jadwal Tayang"]
    for m in movies_list:
        table.add_row([m["movie_id"], m["judul"], m["genre"], m["studio"], f"{m['harga']:,}", m["jadwal"]])
    print(table)