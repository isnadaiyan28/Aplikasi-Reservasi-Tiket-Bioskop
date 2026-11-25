import pandas as pd
import matplotlib.pyplot as plt
from data_store import TRANSACTIONS_FILE
from colorama import init, Fore, Style

init()

MERAH = Fore.RED
KUNING = Fore.YELLOW
HIJAU = Fore.GREEN
RESET = Style.RESET_ALL


def tampilkan_header(judul):
    print()
    print("========================================")
    print(judul.upper().center(40))
    print("========================================")


def tampilkan_error(pesan):
    print(MERAH + "[!] " + pesan + RESET)


def tampilkan_peringatan(pesan):
    print(KUNING + "[!] " + pesan + RESET)


def tampilkan_sukses(pesan):
    print(HIJAU + "[Sukses] " + pesan + RESET)

def show_sales_analysis():
    tampilkan_header("ANALISIS PENJUALAN TIKET")
    try:
        data_transaksi = pd.read_excel(TRANSACTIONS_FILE)
    except Exception:
        tampilkan_error("Gagal membaca file transaksi. Pastikan file transaksi excel ada dan bisa diakses.")
        return

    if data_transaksi.empty:
        tampilkan_peringatan("Belum ada data transaksi yang bisa ditampilkan.")
        return

    transaksi_lunas = data_transaksi[data_transaksi["status"] == "Lunas"]
    if transaksi_lunas.empty:
        tampilkan_peringatan("Belum ada transaksi berstatus Lunas, jadi grafik belum bisa dibuat.")
        return

    pendapatan_per_film = transaksi_lunas.groupby("judul")["harga"].sum()

    print("\nMenampilkan grafik... (tutup jendela grafik untuk kembali ke menu)")
    plt.figure(figsize=(9, 5))
    pendapatan_per_film.plot(kind="bar", color="teal", edgecolor="black")
    plt.title("Total Pendapatan Tiket per Film (Status: Lunas)")
    plt.xlabel("Judul Film")
    plt.ylabel("Total Pendapatan (Rp)")
    plt.xticks(rotation=15)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()