from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html', nilai_ds=0, nilai_nlp=0, nilai_cv=0, nilai_tech=0, hasil="")

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Memvalidasi data siswa, jika sesuai akan menampilkan nilainya.
    '''
    nama, nim, univ, prodi, nomor_hp  = [x for x in request.form.values()]

    data = []

    data.append(str(nama).lower())
    data.append(str(nim).lower())
    data.append(str(univ).lower())
    data.append(str(prodi).lower())
    data.append(int(nomor_hp))

    dir = "database/database.xlsx"
    df = pd.read_excel(dir)
    
    df['nim'] = str(df['nim'])
    # df['ds'] = int(df['ds'])
    # ds['nlp'] = int(ds['nlp'])
    # ds['cv'] = int(ds['cv'])
    # ds['tech'] = int(ds['tech'])

    df['nama'] = df['nama'].str.lower()
    df['nim'] = df['nim'].str.lower()
    df['univ'] = df['univ'].str.lower()
    df['prodi'] = df['prodi'].str.lower()

    size = df.shape
    size = size[0] - 1

    ds = 0
    nlp = 0
    cv = 0
    tech = 0
    hasil = ''

    for x in df.index:
        name = df['nama'][x]
        
        if data[0] == name:
            ds = (df['ds'][x])
            nlp = (df['nlp'][x])
            cv = (df['cv'][x])
            tech = (df['tech'][x])

            hasil = 'Selamat, Data ditemukan !'
            break
        
        elif x == size:
            hasil = 'Data tidak ditemukan !'
    

    return render_template('index.html', nilai_ds=ds, nilai_nlp=nlp, nilai_cv=cv, nilai_tech=tech, nama=nama, nim=nim, univ=univ, prodi=prodi, nomor_hp=nomor_hp, hasil=hasil)


if __name__ == '__main__':
    app.run(debug=True)