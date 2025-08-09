import pandas as pd
import re

class transofrm:
    def __init__(self, data,  dirty_paterns,exchange_rate=16000):
        self.dirty_patterns = dirty_paterns
        self.data = data
        self.exchange_rate = exchange_rate

    def to_df(self):
        "change data to dataframe"
        if not isinstance(self.data, list):
            raise ValueError("data must be list or dict")
        if len(self.data) == 0:
            raise ValueError("No data found")
        df = pd.DataFrame(self.data)
        print(f" {len(df)} data found")
        print(df.head(5))
        return df
    
    def is_row_dirty(self):
        "Remove rows that contain 'dirty' patterns"
        df = self.to_df()
        if not isinstance(self.dirty_patterns, dict):
            raise ValueError("dirty patterns must be dictionary")
        
        for column, patterns in self.dirty_patterns.items():
            if column in df.columns:
                df = df[~df[column].isin(patterns)]
        return df
    
    def clean_and_transfrom(self):
        """
        Remove unwanted characters and clean specific columns
        clean columns: Rating
        """
        df_clean = self.to_df()
        df_clean['Rating'] = df_clean['Rating'].str.replace(r'Rating: ⭐\s*', '', regex=True)
        df_clean['Rating'] = df_clean['Rating'].str.replace(r'\s*/\s*5', '', regex=True).str.strip()

        # clean size column
        df_clean['Size'] = df_clean['Size'].str.replace(r'Size:\s*', '', regex=True).str.strip()

        # Clean gender column
        if 'Gender' in df_clean.columns:
            df_clean['Gender'] = df_clean['Gender'].str.replace(r'Gender:\s*', '', regex=True)
            df_clean['Gender'] = df_clean['Gender'].str.strip()
        
        # clean colors column
        if 'Colors' in df_clean.columns:
            df_clean['Colors'] = df_clean['Colors'].str.replace(r'\s*Colors$', '', regex=True).str.strip( )

        df_clean = df_clean[~df_clean.isin(['not available']).any(axis=1)]
        try:
            df_clean['Rating'] = pd.to_numeric(df_clean['Rating'], errors='coerce')
            df_clean['Colors'] = pd.to_numeric(df_clean['Colors'], errors='coerce')
        except:
            pass
        print(df_clean.head(5))
        return df_clean
    
    def transform_price(self):
        df_rupiah = self.clean_and_transfrom()

        try:
            df_rupiah['Price_in_dolar'] = df_rupiah['Price'].replace({r'\$': '', r',':''}, regex=True).astype(float)
        
            df_rupiah['Price'] = (df_rupiah['Price_in_dolar'] * self.exchange_rate).round(2)
        
            df_rupiah = df_rupiah.drop(columns=['Price_in_dolar'])
            print(df_rupiah.head(5))
        except Exception as e:
            print(f"error while changing prices : {e}")
        
        return df_rupiah
    
    def remove_duplicates_and_nulls(self):
        df_final = self.transform_price()
        """Remove duplicate rows and null values."""
        try:
            df_final = df_final.drop_duplicates().dropna()
            print(df_final.head(5))
            return df_final.to_csv("fashion_clean.csv", index=False)
        except Exception as e:
            print(f"error while remove duplicate value : {e}")
    