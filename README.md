# Dicoding Collection Dashboard - Bike Sharing Analysis 🚲

![Streamlit Badge](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python Badge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📌 Deskripsi Proyek
Proyek ini merupakan tugas akhir analisis data yang bertujuan untuk menganalisis pola penyewaan sepeda (*Bike Sharing System*). Analisis ini mencakup eksplorasi data (EDA), visualisasi tren berdasarkan waktu dan cuaca, serta pembuatan dashboard interaktif menggunakan **Streamlit**.

Tujuan utama dari proyek ini adalah menjawab pertanyaan bisnis:
1.  Bagaimana pengaruh musim (*season*) terhadap jumlah penyewaan sepeda?
2.  Bagaimana pola penyewaan sepeda berdasarkan jam dalam sehari (*hourly trend*)?

## 📂 Struktur File
- `dashboard.py`: File utama untuk menjalankan dashboard Streamlit.
- `ML_Jonatan.ipynb`: Jupyter Notebook berisi analisis data lengkap (Data Wrangling, EDA, Visualisasi).
- `day.csv`: Dataset penyewaan sepeda harian.
- `hour.csv`: Dataset penyewaan sepeda per jam.
- `requirements.txt`: Daftar library Python yang dibutuhkan.
- `README.md`: Dokumentasi proyek ini.

## 🚀 Cara Menjalankan Dashboard (Lokal)

Jika Anda ingin menjalankan dashboard ini di komputer lokal, ikuti langkah-langkah berikut:

1.  **Clone Repository ini**
    ```bash
    git clone [https://github.com/Luckybastd/bike-sharing-dashboard.git](https://github.com/Luckybastd/bike-sharing-dashboard.git)
    ```

2.  **Masuk ke Direktori Proyek**
    ```bash
    cd bike-sharing-dashboard
    ```

3.  **Install Library yang Dibutuhkan**
    Pastikan Anda sudah menginstall Python. Jalankan perintah berikut di terminal:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan Aplikasi Streamlit**
    ```bash
    streamlit run dashboard.py
    ```

## 📊 Insight & Temuan Utama
Berdasarkan hasil analisis data, diperoleh kesimpulan sebagai berikut:

- **Pengaruh Musim:**
    - Jumlah penyewaan sepeda tertinggi terjadi pada **Musim Gugur (Fall)**, diikuti oleh Musim Panas (Summer).
    - Penyewaan terendah terjadi pada **Musim Semi (Spring)**. Hal ini menunjukkan bahwa cuaca hangat dan stabil mendorong orang untuk lebih banyak menyewa sepeda.

- **Pola Jam (Hourly Trend):**
    - Terdapat pola **Bimodal** (dua puncak) yang signifikan pada pukul **08:00 pagi** dan **17:00 sore**.
    - Pola ini mengindikasikan bahwa sepeda mayoritas digunakan sebagai sarana transportasi komuter (berangkat dan pulang kerja/sekolah) dibandingkan untuk rekreasi semata.

## 🔗 Tautan Dashboard
Dashboard hasil deployment dapat diakses melalui tautan berikut:
👉 **[Klik di sini untuk melihat Dashboard Streamlit]((https://bike-sharing-dashboard-jonatan.streamlit.app/))**
