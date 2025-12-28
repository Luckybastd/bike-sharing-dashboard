import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "total_count": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    return daily_orders_df

def create_season_df(df):
    season_df = df.groupby("season_label").total_count.sum().sort_values(ascending=False).reset_index()
    return season_df

def create_hourly_df(df):
    hourly_df = df.groupby("hour").total_count.mean().reset_index()
    return hourly_df

def create_weather_df(df):
    weather_df = df.groupby("weather_label").total_count.mean().sort_values(ascending=False).reset_index()
    return weather_df

try:
    day_df = pd.read_csv("day.csv") 
    hour_df = pd.read_csv("hour.csv")
except FileNotFoundError:
    try:
        day_df = pd.read_csv("Day.csv")
        hour_df = pd.read_csv("Hour.csv")
    except:
        st.error("File CSV tidak ditemukan! Harap cek nama file di Repository GitHub Anda.")
        st.stop()

datetime_columns = ["dteday"]
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
if day_df['season'].dtype == 'int64':
    day_df['season_label'] = day_df['season'].map(season_map)
    hour_df['season_label'] = hour_df['season'].map(season_map)
else:
    day_df['season_label'] = day_df['season']
    hour_df['season_label'] = hour_df['season']

weather_map = {1: 'Clear/Partly Cloudy', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Ice'}
if day_df['weathersit'].dtype == 'int64':
    day_df['weather_label'] = day_df['weathersit'].map(weather_map)
else:
    day_df['weather_label'] = day_df['weathersit']

if 'cnt' in day_df.columns:
    day_df.rename(columns={'cnt': 'total_count'}, inplace=True)
if 'cnt' in hour_df.columns:
    hour_df.rename(columns={'cnt': 'total_count', 'hr': 'hour'}, inplace=True)

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    
    try:
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    except ValueError:
        st.error("Mohon tunggu hingga tanggal selesai dimuat.")
        st.stop()

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
season_df = create_season_df(main_df)
weather_df = create_weather_df(main_df)
hourly_df = create_hourly_df(hour_df) 

st.header('Bike Sharing Dashboard 🚲')
st.markdown("Dashboard ini menampilkan analisis performa penyewaan sepeda berdasarkan musim, cuaca, dan jam operasional.")

st.subheader('Overview Harian')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = main_df.total_count.sum()
    st.metric("Total Sewa", value=f"{total_orders:,}")

with col2:
    total_casual = main_df.casual.sum()
    st.metric("Pengguna Casual", value=f"{total_casual:,}")

with col3:
    total_reg = main_df.registered.sum()
    st.metric("Pengguna Terdaftar", value=f"{total_reg:,}")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Tren Harian", "Analisis Musim & Cuaca", "Pola Jam"])

with tab1:
    st.subheader("Tren Penyewaan Harian")
    
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        daily_orders_df["dteday"],
        daily_orders_df["total_count"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.set_title("Grafik Jumlah Penyewaan Harian", fontsize=20)
    ax.tick_params(axis='y', labelsize=15)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)
    
    with st.expander("Lihat Penjelasan Insight"):
        st.write("""
        - Grafik di atas menunjukkan fluktuasi jumlah penyewaan sepeda setiap harinya.
        - **Puncak-puncak tertinggi** biasanya terjadi pada pertengahan tahun (Musim Gugur/Panas).
        - **Penurunan drastis** terlihat di awal dan akhir tahun (Musim Dingin/Semi).
        """)

with tab2:
    st.subheader("Pengaruh Musim & Cuaca")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            y="total_count", 
            x="season_label",
            data=season_df.sort_values(by="total_count", ascending=False),
            palette="viridis",
            ax=ax
        )
        ax.set_title("Penyewaan Berdasarkan Musim", fontsize=15)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            y="total_count", 
            x="weather_label",
            data=weather_df.sort_values(by="total_count", ascending=False),
            palette="coolwarm",
            ax=ax
        )
        ax.set_title("Rata-rata Penyewaan per Cuaca", fontsize=15)
        st.pyplot(fig)
    
    st.info("""
    **Insight Penting:**
    1. **Musim Gugur (Fall)** adalah periode dengan performa terbaik, diikuti oleh Musim Panas.
    2. Cuaca **Cerah (Clear/Partly Cloudy)** sangat mendominasi jumlah penyewaan.
    3. Cuaca buruk (Hujan/Salju) menyebabkan penurunan aktivitas sewa yang signifikan.
    """)

with tab3:
    st.subheader("Pola Penyewaan Berdasarkan Jam")
    
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.lineplot(
        x="hour",
        y="total_count",
        data=hourly_df,
        marker="o",
        linewidth=3,
        color="#72BCD4",
        ax=ax
    )
    ax.set_title("Rata-rata Penyewaan per Jam", fontsize=20)
    ax.set_xlabel("Jam (00:00 - 23:00)", fontsize=15)
    ax.set_ylabel("Rata-rata Penyewa", fontsize=15)
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    st.pyplot(fig)
    
    st.success("""
    **Kesimpulan Pola Jam:**
    Terlihat pola **Bimodal** (dua puncak) yang jelas:
    - **Pukul 08:00 Pagi:** Puncak pertama (berangkat kerja/sekolah).
    - **Pukul 17:00 - 18:00 Sore:** Puncak kedua (pulang kerja).
    - Ini mengindikasikan sepeda banyak digunakan untuk **aktivitas komuter harian**.
    """)

st.caption('Copyright (c) Jonatan 2025')

