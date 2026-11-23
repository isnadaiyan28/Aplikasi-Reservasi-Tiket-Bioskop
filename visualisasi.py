import pandas as pd
import matplotlib.pyplot as plt
from data_store import TRANSACTIONS_FILE
from search_filter import tampilkan_error, tampilkan_header

def show_sales_analysis():
    tampilkan_header("ANALISIS PENJUALAN TIKET")
    try:
        data_transaksi = pd.read_excel(TRANSACTIONS_FILE)
    except Exception:
        tampilkan_error("Gagal membaca file transaksi. Pastikan file transaksi excel ada dan bisa diakses.")
        return
        
    if data_transaksi.empty:
        tampilkan_error("Belum ada data transaksi yang bisa ditampilkan.")
        return
        
    transaksi_lunas = data_transaksi[data_transaksi["status"] == "Lunas"]
    if transaksi_lunas.empty:
        tampilkan_error("Belum ada transaksi berstatus Lunas, jadi grafik belum bisa dibuat.")
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