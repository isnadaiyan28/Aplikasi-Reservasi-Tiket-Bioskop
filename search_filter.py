from data_store import load_excel, MOVIES_FILE
from prettytable import PrettyTable
import customer_features
from colorama import init, Fore, Style

init()

KUNING = Fore.YELLOW
MERAH = Fore.RED
RESET = Style.RESET_ALL


def tampilkan_header(judul):
    print()
    print("========================================")
    print(judul.upper().center(40))
    print("========================================")


def tampilkan_error(pesan):
    print(MERAH + "[!] " + pesan + RESET)


def tanya_ya_tidak(pertanyaan):
    while True:
        jawaban = input(pertanyaan).strip().lower()
        if jawaban == "y" or jawaban == "n":
            return jawaban
        tampilkan_error("Tolong ketik 'y' untuk ya, atau 'n' untuk tidak, ya.")


def tampilkan_tabel_film(daftar_film):
    tabel = PrettyTable()
    tabel.field_names = ["ID Film", "Judul Film", "Genre", "Studio", "Harga (Rp)", "Jadwal Tayang"]
    for film in daftar_film:
        harga_format = format(int(film["harga"]), ",")
        tabel.add_row([film["movie_id"], film["judul"], film["genre"], 
                       film["studio"], harga_format, film["jadwal"]])
    print(tabel)


def search_and_filter_movies(pengguna_saat_ini=None):
    daftar_film = load_excel(MOVIES_FILE)
    if len(daftar_film) == 0:
        print(KUNING + "Yah, sayang sekali belum ada film yang sedang tayang saat ini." + RESET)
        return pengguna_saat_ini

    while True:
        tampilkan_header("Pencarian & Filter Film")
        print("1. Cari judul film")
        print("2. Pilih berdasarkan genre")
        print("3. Lihat semua film yang tayang")
        print("4. Kembali ke halaman utama")
        
        pilihan = input("Mau pilih menu nomor berapa? (1-4): ").strip()

        hasil_filter = []
        if pilihan == "1":
            kata_kunci = input("Ketik judul film yang dicari (atau ketik 'batal' untuk kembali): ").strip().lower()
            if kata_kunci == "batal":
                continue
            
            for film in daftar_film:
                if kata_kunci in str(film["judul"]).lower():
                    hasil_filter.append(film)

        elif pilihan == "2":
            daftar_genre = []
            for film in daftar_film:
                genre = film["genre"]
                if genre not in daftar_genre:
                    daftar_genre.append(genre)
            
            print("\nDaftar Genre Tersedia:")
            nomor = 1
            for genre in daftar_genre:
                print(str(nomor) + ".", genre)
                nomor = nomor + 1
            
            while True:
                input_genre = input("Pilih nomor genre yang kamu suka (atau ketik 'batal'): ").strip()
                if input_genre.lower() == "batal":
                    hasil_filter = None
                    break
                
                if input_genre.isdigit() and 1 <= int(input_genre) <= len(daftar_genre):
                    genre_dipilih = daftar_genre[int(input_genre) - 1]
                    for film in daftar_film:
                        if str(film["genre"]).lower() == genre_dipilih.lower():
                            hasil_filter.append(film)
                    break
                else:
                    tampilkan_error("Duh, nomor genrenya nggak ada di daftar. Coba cek lagi ya.")
            
            if hasil_filter is None:
                continue

        elif pilihan == "3":
            hasil_filter = daftar_film

        elif pilihan == "4":
            break

        else:
            tampilkan_error("Hmm, pilihannya cuma dari angka 1 sampai 4 aja nih. Yuk coba lagi.")
            continue

        if len(hasil_filter) == 0:
            print()
            print(KUNING + "[!] Maaf ya, film yang kamu cari belum ketemu nih." + RESET)
            sub_pilih = tanya_ya_tidak("Mau coba cari film lain? (y/n): ")
            if sub_pilih == "y":
                continue
            else:
                break
        else:
            tampilkan_tabel_film(hasil_filter)
            
            while True:
                print()
                id_film = input("Ketik ID Film yang mau dicek atau dipesan (ketik 'batal' kalau mau kembali): ").strip().upper()
                if id_film == "BATAL":
                    break
                
                film_dipilih = None
                for film in hasil_filter:
                    if film["movie_id"] == id_film:
                        film_dipilih = film
                        break
                
                if film_dipilih is not None:
                    print("\n--- DETAIL FILM:", film_dipilih["judul"], "---")
                    print("Genre    :", film_dipilih["genre"])
                    print("Studio   :", film_dipilih["studio"])
                    print("Harga    : Rp" + format(int(film_dipilih["harga"]), ","))
                    print("Jadwal   :", film_dipilih["jadwal"])
                    
                    if not pengguna_saat_ini:
                        print()
                        print(KUNING + "[!] Wah, kamu harus login dulu nih kalau mau pesan tiket." + RESET)
                        opsi_login = tanya_ya_tidak("Mau login sekarang biar bisa pesan tiket? (y/n): ")
                            
                        if opsi_login == "y":
                            from auth import login
                            usr, role = login()
                            if usr:
                                pengguna_saat_ini = usr
                                customer_features.make_reservation(pengguna_saat_ini, pre_selected_movie_id=id_film)
                        else:
                            print("Oke, pemesanan tiket dibatalkan ya.")
                    else:
                        pesan = tanya_ya_tidak("Gimana, jadi pesan tiket untuk film ini? (y/n): ")
                        if pesan == "y":
                            customer_features.make_reservation(pengguna_saat_ini, pre_selected_movie_id=id_film)
                    break
                else:
                    tampilkan_error("ID Film-nya sepertinya salah ketik. Coba masukkan ID yang sesuai daftar ya.")
            
            lanjut = tanya_ya_tidak("\nApakah kamu mau keluar dari menu pencarian ini? (y/n): ")
            if lanjut == "y":
                break
                
    return pengguna_saat_ini