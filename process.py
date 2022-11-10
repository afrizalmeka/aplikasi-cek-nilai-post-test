import pandas as pd

global df

def load():
    global df

    #memanggil berkas database
    dir = "database/database_apollo_class.xlsx"
    df = pd.read_excel(dir)

    #didatabase pada kolom nama, univ, prodi perlu di lowercase agar perbandingan huruf nya sama dengan inputan
    df['nama'] = df['nama'].str.lower()
    df['univ'] = df['univ'].str.lower()
    df['prodi'] = df['prodi'].str.lower()