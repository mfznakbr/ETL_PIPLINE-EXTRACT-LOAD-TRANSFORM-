import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# main.py
from utils.extract import Extract
from utils.transform import transofrm 

if __name__ == "__main__":
    # 1. Tentukan URL
    base_url = Extract('https://fashion-studio.dicoding.dev')

    # 2. Jalankan proses extract
    extractor = base_url
    raw_data = extractor.fetching_content(start_page=1, delay=2)

    if raw_data:
        print(f"\n✅ Berhasil mengambil {len(raw_data)} data")
        
        # 3. Jalankan proses transform
        dirty_patterns = {
            "Title": ["Unknown Product", "Tidak Ada"],
            "Rating": ["Invalid Rating", "Rating: Not Rated", "Tidak Ada"],
            "Price": ['Tidak Ada']
        }
        transformer = transofrm(raw_data, dirty_patterns,exchange_rate=16000)

        df_final = transformer.remove_duplicates_and_nulls()
        print("\n📁 Data final disimpan ke fashion_clean.csv")
    else:
        print("❌ Gagal mengambil data.")

