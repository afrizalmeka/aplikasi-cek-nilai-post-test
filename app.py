from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html', nilai_ds=0, nilai_nlp=0, nilai_cv=0, nilai_tech=0, hasil='')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Memvalidasi data siswa, jika sesuai akan menampilkan nilainya.
    '''
    nama, id_msib, univ, prodi, nomor_hp  = [x for x in request.form.values()]

    #wadah untuk inputan
    data = []

    #menambah value di lisr "data"
    #tujuan lowercase pada string, supaya agar kecil semua huruf nya. untuk keperluan validasi
    data.append(str(nama).lower())
    data.append(int(id_msib))
    data.append(str(univ).lower())
    data.append(str(prodi).lower())
    data.append(int(nomor_hp))

    #memanggil berkas database
    dir = "database/database.xlsx"
    df = pd.read_excel(dir)

    #didatabase pada kolom nama, univ, prodi perlu di lowercase agar perbandingan huruf nya sama dengan inputan
    df['nama'] = df['nama'].str.lower()
    df['univ'] = df['univ'].str.lower()
    df['prodi'] = df['prodi'].str.lower()

    #menentukan ukuran baris, sebagai penentu kapan berhenti dari loops
    size = df.shape
    size = size[0] - 1

    #variabel wadah untuk nilai post test
    ds, nlp, cv, tech = 0, 0, 0, 0

    #variabel wadah untuk menampilkan pesan berhasil atau gagal
    hasil = ''


    for x in df.index:
        """Fungsi Loops untuk memvalidasi input data siswa, agar output nilai nya sesuai dengan
        yang diminta. Lalu menampilkan sebuah pesan apakah data sesuai atau tidak."""

        A = df['nama'][x]
        B = df['id_msib'][x]
        C = df['univ'][x]
        D = df['prodi'][x]
        E = df['nohp'][x]
        
        #memvalidasi apakah nama, id_msib, univ, prodi, nohp sesuai atau tidak
        if (data[0] == A) and (data[1] == B) and (data[2] == C) and (data[3] == D) and (data[4] == E):
            #jika sesuai maka akan mengambil data nilai ds, nlp, cv, tech
            ds = (df['ds'][x])
            nlp = (df['nlp'][x])
            cv = (df['cv'][x])
            tech = (df['tech'][x])

            #kemudian menampilkan pesan berhasil jika sesuai datanya
            hasil = 'Selamat, Data ditemukan !'
            #akan melakukan break jika sudah berhasil menemukan data nya, dan tidak melanjutkan perulangannya
            break
        
        #jika sampai perulangan terakhir tidak ditemukan kecocokan data dari inputan, maka akan menampilkan pesan gagal
        elif x == size:
            hasil = 'Maaf, Data tidak ditemukan !'
    

    return render_template('index.html', nilai_ds=ds, nilai_nlp=nlp, nilai_cv=cv, nilai_tech=tech, nama=nama, id_msib=id_msib, univ=univ, prodi=prodi, nomor_hp=nomor_hp, hasil=hasil)


if __name__ == '__main__':
    app.run(debug=True)