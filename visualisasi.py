import pandas as pd
import matplotlib.pyplot as plt
from data_store import TRANSACTIONS_FILE

def show_sales_analytics():
    try:
        df = pd.read_excel(TRANSACTIONS_FILE)
    except Exception:
        print("Gagal membaca file transaksi Excel.")
        return
        
    if df.empty:
        print("Belum ada data transaksi untuk divisualisasikan.")
        return
        
    df_lunas = df[df["status"] == "Lunas"]
    if df_lunas.empty:
        print("Belum ada transaksi berstatus Lunas untuk grafik.")
        return

    income_per_movie = df_lunas.groupby("judul")["harga"].sum()
    
    plt.figure(figsize=(9, 5))
    income_per_movie.plot(kind="bar", color="teal", edgecolor="black")
    plt.title("Rekapitulasi Total Pendapatan Tiket Per Film (Status: Lunas)")
    plt.xlabel("Judul Film")
    plt.ylabel("Total Pendapatan (Rp)")
    plt.xticks(rotation=15)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()