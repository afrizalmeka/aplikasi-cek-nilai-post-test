import pandas as pd

def pandas_jalankan():
    global ds, nlp, cv, tech, df, size

    dir = "/database/database.xlsx"
    df = pd.read_excel(dir)

    df['nama'] = df['nama'].str.lower()
    df['nim'] = df['nim'].str.lower()
    df['univ'] = df['univ'].str.lower()
    df['prodi'] = df['prodi'].str.lower()

    size = df.shape
    size = size[0]

    ds = 