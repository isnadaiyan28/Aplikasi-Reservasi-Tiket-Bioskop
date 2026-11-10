import os
import pandas as pd

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.xlsx")
MOVIES_FILE = os.path.join(DATA_DIR, "movies.xlsx")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.xlsx")

def init_storage():
    """Membuat folder data dan file Excel default jika belum ada."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # 1. Inisialisasi Users Excel
    if not os.path.exists(USERS_FILE):
        default_users = [
            {"username": "admin", "password": "admin123", "role": "admin", "nama": "Administrator"},
            {"username": "isna", "password": "isna123", "role": "customer", "nama": "Isna Daiyan"}
        ]
        df_users = pd.DataFrame(default_users)
        df_users.to_excel(USERS_FILE, index=False)
        
    # 2. Inisialisasi Movies Excel
    if not os.path.exists(MOVIES_FILE):
        default_movies = [
            {
                "movie_id": "M1",
                "judul": "Interstellar",
                "genre": "Sci-Fi",
                "harga": 45000,
                "studio": "Studio 1",
                "kapasitas": 12,
                "jadwal": "13:00, 16:00, 19:00"  # Disimpan sebagai string terpisah koma
            },
            {
                "movie_id": "M2",
                "judul": "Avatar: The Way of Water",
                "genre": "Action",
                "harga": 50000,
                "studio": "Studio 2",
                "kapasitas": 12,
                "jadwal": "14:00, 18:00"
            }
        ]
        df_movies = pd.DataFrame(default_movies)
        df_movies.to_excel(MOVIES_FILE, index=False)
        
    # 3. Inisialisasi Transactions Excel
    if not os.path.exists(TRANSACTIONS_FILE):
        columns = ["booking_code", "username", "movie_id", "judul", "jadwal", "kursi", "harga", "status", "tanggal"]
        df_tx = pd.DataFrame(columns=columns)
        df_tx.to_excel(TRANSACTIONS_FILE, index=False)

def load_excel(filepath):
    """Membaca file Excel dan mengembalikan list of dicts."""
    try:
        df = pd.read_excel(filepath)
        # Mengatur agar nilai NaN/kosong tidak merusak tipe data string
        df = df.fillna("")
        return df.to_dict(orient="records")
    except Exception:
        return []

def save_excel(filepath, data_list):
    """Menyimpan list of dicts kembali ke file Excel."""
    df = pd.DataFrame(data_list)
    df.to_excel(filepath, index=False)