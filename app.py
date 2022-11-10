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
    data.append(str(nama).lower().strip())
    data.append(int(id_msib))
    data.append(str(univ).lower().strip())
    data.append(str(prodi).lower().strip())
    data.append(int(nomor_hp))

    #memanggil berkas database
    dir = "database/database_apollo_class.xlsx"
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

    #variabel wadah untuk nilai dan absen intro to ai
    nilai_intro_to_ai_1, nilai_intro_to_ai_2, nilai_intro_to_ai_3, nilai_intro_to_ai_4, nilai_intro_to_ai_5 = 0, 0, 0, 0, 0
    absen_intro_ai_1, absen_intro_ai_2, absen_intro_ai_3, absen_intro_ai_4, absen_intro_ai_5 = 0, 0, 0, 0, 0
    posttest_intro_ai, final_intro_ai, alphabet_intro_ai = 0, 0, ""

    #varibel wadah untuk nilai dan absen python

    #inisialisasi status absen, dikarenakan data absen hanya 0,1,K
    status_absen = {1 : 'Hadir', 0 : 'Tidak Hadir', 'K' : 'Durasi Kurang'}
    
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
            #jika sesuai maka akan mengambil data nilai dari intro to ai
            nilai_intro_to_ai_1 = (df['nilai_intro_to_ai_1'][x])
            nilai_intro_to_ai_2 = (df['nilai_intro_to_ai_2'][x])
            nilai_intro_to_ai_3 = (df['nilai_intro_to_ai_3'][x])
            nilai_intro_to_ai_4 = (df['nilai_intro_to_ai_4'][x])
            nilai_intro_to_ai_5 = (df['nilai_intro_to_ai_5'][x])

            absen_intro_ai_1 = status_absen[(df['absen_intro_ai_1'][x])]
            absen_intro_ai_2 = status_absen[(df['absen_intro_ai_2'][x])]
            absen_intro_ai_3 = status_absen[(df['absen_intro_ai_3'][x])]
            absen_intro_ai_4 = status_absen[(df['absen_intro_ai_4'][x])]
            absen_intro_ai_5 = status_absen[(df['absen_intro_ai_5'][x])]

            posttest_intro_ai = (df['posttest_intro_ai'][x])
            final_intro_ai = (df['final_intro_ai'][x])
            alphabet_intro_ai = (df['alphabet_intro_ai'][x])

            #jika sesuai maka akan mengambil data nilai dari post test ds, nlp, cv, tech
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
    

    return render_template('index.html', nilai_ds=ds, nilai_nlp=nlp, nilai_cv=cv, nilai_tech=tech, 
                            nama=nama, id_msib=id_msib, univ=univ, prodi=prodi, nomor_hp=nomor_hp, hasil=hasil,
                            
                            nilai_intro_to_ai_1=nilai_intro_to_ai_1, nilai_intro_to_ai_2=nilai_intro_to_ai_2,
                            nilai_intro_to_ai_3=nilai_intro_to_ai_3, nilai_intro_to_ai_4=nilai_intro_to_ai_4,
                            nilai_intro_to_ai_5=nilai_intro_to_ai_5,
                            
                            absen_intro_ai_1=absen_intro_ai_1, absen_intro_ai_2=absen_intro_ai_2,
                            absen_intro_ai_3=absen_intro_ai_3, absen_intro_ai_4=absen_intro_ai_4,
                            absen_intro_ai_5=absen_intro_ai_5,
                            
                            posttest_intro_ai=posttest_intro_ai, final_intro_ai=final_intro_ai, alphabet_intro_ai=alphabet_intro_ai)


if __name__ == '__main__':
    app.run(debug=True)