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
    nama, id_msib, nomor_hp  = [x for x in request.form.values()]

    #wadah untuk inputan
    data = []

    #menambah value di lisr "data"
    #tujuan lowercase pada string, supaya agar kecil semua huruf nya. untuk keperluan validasi
    data.append(str(nama).lower().strip())
    data.append(int(id_msib))
    data.append(int(nomor_hp))

    #memanggil berkas database
    dir = "database/database_apollo_class.xlsx"
    
    df1 = pd.read_excel(dir, sheet_name="intro_ai")

    df2 = pd.read_excel(dir, sheet_name="python")
    df2 = df2.drop(['nama'], axis=1)

    df3 = pd.read_excel(dir, sheet_name="siklus_ai")
    df3 = df3.drop(['nama'], axis=1)

    df4 = pd.read_excel(dir, sheet_name="intro_ml")
    df4 = df4.drop(['nama'], axis=1)

    df5 = pd.read_excel(dir, sheet_name="ds")
    df5 = df5.drop(['nama'], axis=1)

    df6 = pd.read_excel(dir, sheet_name="nlp")
    df6 = df6.drop(['nama'], axis=1)

    df7 = pd.read_excel(dir, sheet_name="cv")
    df7 = df7.drop(['nama'], axis=1)

    df8 = pd.read_excel(dir, sheet_name="tech")
    df8 = df8.drop(['nama'], axis=1)

    df9 = pd.read_excel(dir, sheet_name="lifeskill")
    df9 = df9.drop(['nama'], axis=1)

    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9], axis=1)

    #didatabase pada kolom nama, univ, prodi perlu di lowercase agar perbandingan huruf nya sama dengan inputan
    df['nama'] = df['nama'].str.lower()

    #menentukan ukuran baris, sebagai penentu kapan berhenti dari loops
    size = df.shape
    size = size[0] - 1

    #variabel wadah untuk nilai post test
    ds, nlp, cv, tech = 0, 0, 0, 0

    #variabel wadah untuk nilai dan absen intro to ai
    nilai_intro_ai_1, nilai_intro_ai_2, nilai_intro_ai_3, nilai_intro_ai_4, nilai_intro_ai_5 = 0, 0, 0, 0, 0
    absen_intro_ai_1, absen_intro_ai_2, absen_intro_ai_3, absen_intro_ai_4, absen_intro_ai_5 = "", "", "", "", ""
    posttest_intro_ai, final_intro_ai, alphabet_intro_ai = 0, 0, ""

    #varibel wadah untuk nilai dan absen python
    nilai_python_1, nilai_python_2, nilai_python_3, nilai_python_4, nilai_python_5, nilai_python_6, nilai_python_7, nilai_python_8 = 0, 0, 0, 0, 0, 0, 0, 0
    absen_python_1, absen_python_2, absen_python_3, absen_python_4, absen_python_5, absen_python_6, absen_python_7, absen_python_8 = "", "", "", "", "", "", "", ""
    posttest_python, final_python, alphabet_python = 0, 0, ""

    #varibel wadah untuk nilai dan absen siklus projek ai
    nilai_siklus_1, nilai_siklus_2, nilai_siklus_3 = 0, 0, 0
    absen_siklus_1, absen_siklus_2, absen_siklus_3 = "", "", ""
    posttest_siklus, final_siklus, alphabet_siklus = 0, 0, ""

    #varibel wadah untuk nilai dan absen intro to machine learning
    nilai_ml_1, nilai_ml_2, nilai_ml_3, nilai_ml_4, nilai_ml_5, nilai_ml_6, nilai_ml_7, nilai_ml_8 = 0, 0, 0, 0, 0, 0, 0, 0
    absen_ml_1, absen_ml_2, absen_ml_3, absen_ml_4, absen_ml_5, absen_ml_6, absen_ml_7, absen_ml_8 = "", "", "", "", "", "", "", ""
    posttest_ml, final_ml, alphabet_ml = 0, 0, ""

    #varibel wadah untuk nilai dan absen domain ds
    nilai_ds_1, nilai_ds_2, nilai_ds_3, nilai_ds_4, nilai_ds_5 = 0, 0, 0, 0, 0
    total_absen_ds = 0
    posttest_ds, final_ds, alphabet_ds = 0, 0, ""

    #varibel wadah untuk nilai dan absen domain nlp
    nilai_nlp_1, nilai_nlp_2, nilai_nlp_3, nilai_nlp_4, nilai_nlp_5 = 0, 0, 0, 0, 0
    total_absen_nlp = 0
    posttest_nlp, final_nlp, alphabet_nlp = 0, 0, ""

    #varibel wadah untuk nilai dan absen domain cv
    nilai_cv_1, nilai_cv_2, nilai_cv_3, nilai_cv_4, nilai_cv_5, mini_project_cv = 0, 0, 0, 0, 0, 0 
    total_absen_cv = 0
    posttest_cv, final_cv, alphabet_cv = 0, 0, ""

    #varibel wadah untuk nilai dan absen domain tech
    nilai_tech_1, nilai_tech_2, nilai_tech_3, nilai_tech_4, nilai_tech_5 = 0, 0, 0, 0, 0
    total_absen_tech = 0
    posttest_tech, final_tech, alphabet_tech = 0, 0, ""

    #variabel wadah untuk nilai dan absen total metode penelitian ai
    final_metode_penelitian = 0
    alphabet_metode_penelitian = ""

    #variabel wadah untuk nilai akhir life skill
    final_lifeskill = 0
    alphabet_lifeskill = ""

    #inisialisasi status absen, dikarenakan data absen hanya 0,1,K
    status_absen = {1 : 'Hadir', 0 : 'Tidak Hadir', 'K' : 'Durasi Kurang'}
    
    #variabel wadah untuk menampilkan pesan berhasil atau gagal
    hasil = ''


    for x in df.index:
        """Fungsi Loops untuk memvalidasi input data siswa, agar output nilai nya sesuai dengan
        yang diminta. Lalu menampilkan sebuah pesan apakah data sesuai atau tidak."""

        A = df['nama'][x]
        B = df['id_msib'][x]
        C = df['nohp'][x]
        

        #memvalidasi apakah nama, id_msib, univ, prodi, nohp sesuai atau tidak
        if (data[0] == A) and (data[1] == B) and (data[2] == C):
            
            #fungsi untuk menentukan alphabet nilai akhir
            def alphabet_nilai(nilai):
                if nilai >= 80:
                    return "A"
                elif nilai >= 70:
                    return "B"
                elif nilai >= 50:
                    return "C"
                elif nilai >= 40:
                    return "D"
                else:
                    return "E"

            #jika sesuai maka akan mengambil data nilai dan absen dari intro to ai
            nilai_intro_ai_1 = (df['nilai_intro_ai_1'][x])
            nilai_intro_ai_2 = (df['nilai_intro_ai_2'][x])
            nilai_intro_ai_3 = (df['nilai_intro_ai_3'][x])
            nilai_intro_ai_4 = (df['nilai_intro_ai_4'][x])
            nilai_intro_ai_5 = (df['nilai_intro_ai_5'][x])
            absen_intro_ai_1 = status_absen[(df['absen_intro_ai_1'][x])]
            absen_intro_ai_2 = status_absen[(df['absen_intro_ai_2'][x])]
            absen_intro_ai_3 = status_absen[(df['absen_intro_ai_3'][x])]
            absen_intro_ai_4 = status_absen[(df['absen_intro_ai_4'][x])]
            absen_intro_ai_5 = status_absen[(df['absen_intro_ai_5'][x])]
            posttest_intro_ai = (df['posttest_intro_ai'][x])
            final_intro_ai = (df['final_intro_ai'][x])
            alphabet_intro_ai = (df['alphabet_intro_ai'][x])

            #jika sesuai maka akan mengambil data nilai dan absen dari python
            nilai_python_1 = (df['nilai_python_1'][x])
            nilai_python_2 = (df['nilai_python_2'][x])
            nilai_python_3 = (df['nilai_python_3'][x])
            nilai_python_4 = (df['nilai_python_4'][x])
            nilai_python_5 = (df['nilai_python_5'][x])
            nilai_python_6 = (df['nilai_python_6'][x])
            nilai_python_7 = (df['nilai_python_7'][x])
            nilai_python_8 = (df['nilai_python_8'][x])
            absen_python_1 = status_absen[(df['absen_python_1'][x])]
            absen_python_2 = status_absen[(df['absen_python_2'][x])]
            absen_python_3 = status_absen[(df['absen_python_3'][x])]
            absen_python_4 = status_absen[(df['absen_python_4'][x])]
            absen_python_5 = status_absen[(df['absen_python_5'][x])]
            absen_python_6 = status_absen[(df['absen_python_6'][x])]
            absen_python_7 = status_absen[(df['absen_python_7'][x])]
            absen_python_8 = status_absen[(df['absen_python_8'][x])]
            posttest_python = (df['posttest_python'][x])
            final_python = (df['final_python'][x])
            alphabet_python = (df['alphabet_python'][x])

            #jika sesuai maka akan mengambil data nilai dan absen dari siklus ai
            nilai_siklus_1 = (df['nilai_siklus_1'][x])
            nilai_siklus_2 = (df['nilai_siklus_2'][x])
            nilai_siklus_3 = (df['nilai_siklus_3'][x])
            absen_siklus_1 = status_absen[(df['absen_siklus_1'][x])]
            absen_siklus_2 = status_absen[(df['absen_siklus_2'][x])]
            absen_siklus_3 = status_absen[(df['absen_siklus_3'][x])]
            posttest_siklus = (df['posttest_siklus'][x])
            final_siklus = (df['final_siklus'][x])
            alphabet_siklus = (df['alphabet_siklus'][x])

            #jika sesuai maka akan mengambil data nilai dan absen dari intro to machine learning
            nilai_ml_1 = (df['nilai_ml_1'][x])
            nilai_ml_2 = (df['nilai_ml_2'][x])
            nilai_ml_3 = (df['nilai_ml_3'][x])
            nilai_ml_4 = (df['nilai_ml_4'][x])
            nilai_ml_5 = (df['nilai_ml_5'][x])
            nilai_ml_6 = (df['nilai_ml_6'][x])
            nilai_ml_7 = (df['nilai_ml_7'][x])
            nilai_ml_8 = (df['nilai_ml_8'][x])
            absen_ml_1 = status_absen[(df['absen_ml_1'][x])]
            absen_ml_2 = status_absen[(df['absen_ml_2'][x])]
            absen_ml_3 = status_absen[(df['absen_ml_3'][x])]
            absen_ml_4 = status_absen[(df['absen_ml_4'][x])]
            absen_ml_5 = status_absen[(df['absen_ml_5'][x])]
            absen_ml_6 = status_absen[(df['absen_ml_6'][x])]
            absen_ml_7 = status_absen[(df['absen_ml_7'][x])]
            absen_ml_8 = status_absen[(df['absen_ml_8'][x])]
            posttest_ml = (df['posttest_ml'][x])
            final_ml = (df['final_ml'][x])
            alphabet_ml = (df['alphabet_ml'][x])

            #jika sesuai maka akan mengambil data nilai dan absen dari domain ds
            nilai_ds_1 = (df['nilai_ds_1'][x])
            nilai_ds_2 = (df['nilai_ds_2'][x])
            nilai_ds_3 = (df['nilai_ds_3'][x])
            nilai_ds_4 = (df['nilai_ds_4'][x])
            nilai_ds_5 = (df['nilai_ds_5'][x])
            total_absen_ds = int((df['total_absen_ds'][x]))
            posttest_ds = (df['posttest_ds'][x])
            final_ds = (df['final_ds'][x])
            alphabet_ds = (df['alphabet_ds'][x])

            #jika sesuai maka akan mengambil data nilai dan absen dari domain nlp
            nilai_nlp_1 = (df['nilai_nlp_1'][x])
            nilai_nlp_2 = (df['nilai_nlp_2'][x])
            nilai_nlp_3 = (df['nilai_nlp_3'][x])
            nilai_nlp_4 = (df['nilai_nlp_4'][x])
            nilai_nlp_5 = (df['nilai_nlp_5'][x])
            total_absen_nlp = int((df['total_absen_nlp'][x]))
            posttest_nlp = (df['posttest_nlp'][x])
            final_nlp = (df['final_nlp'][x])
            alphabet_nlp = (df['alphabet_nlp'][x])

            #jika sesuai maka akan mengambil data nilai dan absen dari domain cv
            nilai_cv_1 = (df['nilai_cv_1'][x])
            nilai_cv_2 = (df['nilai_cv_2'][x])
            nilai_cv_3 = (df['nilai_cv_3'][x])
            nilai_cv_4 = (df['nilai_cv_4'][x])
            nilai_cv_5 = (df['nilai_cv_5'][x])
            mini_project_cv = (df['mini_project_cv'][x])
            total_absen_cv = int((df['total_absen_cv'][x]))
            posttest_cv = (df['posttest_cv'][x])
            final_cv = (df['final_cv'][x])
            alphabet_cv = (df['alphabet_cv'][x])

            #jika sesuai maka akan mengambil data nilai dan absen dari domain tech
            nilai_tech_1 = (df['nilai_tech_1'][x])
            nilai_tech_2 = (df['nilai_tech_2'][x])
            nilai_tech_3 = (df['nilai_tech_3'][x])
            nilai_tech_4 = (df['nilai_tech_4'][x])
            nilai_tech_5 = (df['nilai_tech_5'][x])
            total_absen_tech = int((df['total_absen_tech'][x]))
            posttest_tech = (df['posttest_tech'][x])
            final_tech = (df['final_tech'][x])
            alphabet_tech = (df['alphabet_tech'][x])

            #jika sesuai maka akan menghitung nilai final metode penelitian
            final_metode_penelitian = (final_ml + final_ds + final_nlp + final_cv + final_tech) / 5
            alphabet_metode_penelitian = alphabet_nilai(final_metode_penelitian)

            #jika sesuai maka akan mengambil data nilai life skill
            final_lifeskill = (df['final_lifeskill'][x])
            alphabet_lifeskill = alphabet_nilai(final_lifeskill)

            #kemudian menampilkan pesan berhasil jika sesuai datanya
            hasil = 'Selamat, Data ditemukan !'
            #akan melakukan break jika sudah berhasil menemukan data nya, dan tidak melanjutkan perulangannya
            break
        
        #jika sampai perulangan terakhir tidak ditemukan kecocokan data dari inputan, maka akan menampilkan pesan gagal
        elif x == size:
            hasil = 'Maaf, Data tidak ditemukan !'
    

    return render_template('index.html', nama=nama, id_msib=id_msib, nomor_hp=nomor_hp, hasil=hasil,
                            
                            nilai_intro_ai_1=nilai_intro_ai_1, nilai_intro_ai_2=nilai_intro_ai_2,
                            nilai_intro_ai_3=nilai_intro_ai_3, nilai_intro_ai_4=nilai_intro_ai_4,
                            nilai_intro_ai_5=nilai_intro_ai_5,
                            absen_intro_ai_1=absen_intro_ai_1, absen_intro_ai_2=absen_intro_ai_2,
                            absen_intro_ai_3=absen_intro_ai_3, absen_intro_ai_4=absen_intro_ai_4,
                            absen_intro_ai_5=absen_intro_ai_5,
                            posttest_intro_ai=posttest_intro_ai, final_intro_ai=final_intro_ai, alphabet_intro_ai=alphabet_intro_ai,
                            
                            nilai_python_1=nilai_python_1, nilai_python_2=nilai_python_2,
                            nilai_python_3=nilai_python_3, nilai_python_4=nilai_python_4,
                            nilai_python_5=nilai_python_5, nilai_python_6=nilai_python_6,
                            nilai_python_7=nilai_python_7, nilai_python_8=nilai_python_8,
                            absen_python_1=absen_python_1, absen_python_2=absen_python_2,
                            absen_python_3=absen_python_3, absen_python_4=absen_python_4,
                            absen_python_5=absen_python_5, absen_python_6=absen_python_6,
                            absen_python_7=absen_python_7, absen_python_8=absen_python_8,
                            posttest_python=posttest_python, final_python=final_python, alphabet_python=alphabet_python,
                            
                            nilai_siklus_1=nilai_siklus_1, nilai_siklus_2=nilai_siklus_2,
                            nilai_siklus_3=nilai_siklus_3,
                            absen_siklus_1=absen_siklus_1, absen_siklus_2=absen_siklus_2,
                            absen_siklus_3=absen_siklus_3,
                            posttest_siklus=posttest_siklus, final_siklus=final_siklus, alphabet_siklus=alphabet_siklus,

                            nilai_ml_1=nilai_ml_1, nilai_ml_2=nilai_ml_2,
                            nilai_ml_3=nilai_ml_3, nilai_ml_4=nilai_ml_4,
                            nilai_ml_5=nilai_ml_5, nilai_ml_6=nilai_ml_6,
                            nilai_ml_7=nilai_ml_7, nilai_ml_8=nilai_ml_8,
                            absen_ml_1=absen_ml_1, absen_ml_2=absen_ml_2,
                            absen_ml_3=absen_ml_3, absen_ml_4=absen_ml_4,
                            absen_ml_5=absen_ml_5, absen_ml_6=absen_ml_6,
                            absen_ml_7=absen_ml_7, absen_ml_8=absen_ml_8,
                            posttest_ml=posttest_ml, final_ml=final_ml, alphabet_ml=alphabet_ml,

                            nilai_ds_1=nilai_ds_1, nilai_ds_2=nilai_ds_2,
                            nilai_ds_3=nilai_ds_3, nilai_ds_4=nilai_ds_4,
                            nilai_ds_5=nilai_ds_5,
                            total_absen_ds=total_absen_ds,
                            posttest_ds=posttest_ds, final_ds=final_ds, alphabet_ds=alphabet_ds,
                            
                            nilai_nlp_1=nilai_nlp_1, nilai_nlp_2=nilai_nlp_2,
                            nilai_nlp_3=nilai_nlp_3, nilai_nlp_4=nilai_nlp_4,
                            nilai_nlp_5=nilai_nlp_5,
                            total_absen_nlp=total_absen_nlp,
                            posttest_nlp=posttest_nlp, final_nlp=final_nlp, alphabet_nlp=alphabet_nlp,

                            nilai_cv_1=nilai_cv_1, nilai_cv_2=nilai_cv_2,
                            nilai_cv_3=nilai_cv_3, nilai_cv_4=nilai_cv_4,
                            nilai_cv_5=nilai_cv_5, mini_project_cv=mini_project_cv,
                            total_absen_cv=total_absen_cv,
                            posttest_cv=posttest_cv, final_cv=final_cv, alphabet_cv=alphabet_cv,

                            nilai_tech_1=nilai_tech_1, nilai_tech_2=nilai_tech_2,
                            nilai_tech_3=nilai_tech_3, nilai_tech_4=nilai_tech_4,
                            nilai_tech_5=nilai_tech_5,
                            total_absen_tech=total_absen_tech,
                            posttest_tech=posttest_tech, final_tech=final_tech, alphabet_tech=alphabet_tech,
                            
                            final_metode_penelitian=final_metode_penelitian, alphabet_metode_penelitian=alphabet_metode_penelitian,

                            final_lifeskill=final_lifeskill, alphabet_lifeskill=alphabet_lifeskill
                            )


if __name__ == '__main__':
    app.run(debug=True)