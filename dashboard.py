import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper function yang menyiapkan dataframe
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "total_count": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    return daily_orders_df

def create_season_df(df):
    season_df = df.groupby("season_label").total_count.sum().sort_values(ascending=False).reset_index()
    return season_df

def create_hourly_df(df):
    hourly_df = df.groupby("hour").total_count.mean().reset_index()
    return hourly_df

# Load Data (Pastikan file csv berada satu folder dengan dashboard.py)
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Cleaning & Process Data
datetime_columns = ["dteday"]
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])
    hour_df[column] = pd.to_datetime(hour_df[column])

# Mapping Label (Sama seperti di Notebook)
season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_label'] = day_df['season'].map(season_map)

day_df.rename(columns={'cnt': 'total_count'}, inplace=True)
hour_df.rename(columns={'cnt': 'total_count', 'hr': 'hour'}, inplace=True)

# Filter Komponen (Sidebar)
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan Logo (Opsional)
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan input tanggal
main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

# Menyiapkan berbagai dataframe untuk visualisasi
daily_orders_df = create_daily_orders_df(main_df)
season_df = create_season_df(main_df)
hourly_df = create_hourly_df(hour_df) # Gunakan full hour_df untuk pola jam umum

# --- DASHBOARD HEADER ---
st.header('Bike Sharing Dashboard :sparkles:')

# --- METRIC (Total Orders) ---
st.subheader('Daily Orders')
col1, col2 = st.columns(2)

with col1:
    total_orders = main_df.total_count.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    avg_orders = round(main_df.total_count.mean(), 2)
    st.metric("Average Daily", value=avg_orders)

# Visualisasi Tren Harian
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["total_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# --- Visualisasi 1: Season ---
st.subheader("Performance by Season")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="total_count", 
    x="season_label",
    data=season_df.sort_values(by="total_count", ascending=False),
    palette="viridis",
    ax=ax
)
ax.set_title("Number of Bike Sharing by Season", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# --- Visualisasi 2: Hourly Trend ---
st.subheader("Ordering Pattern by Hour")
fig, ax = plt.subplots(figsize=(20, 10))
sns.lineplot(
    x="hour",
    y="total_count",
    data=hourly_df,
    marker="o",
    linewidth=4,
    color="#72BCD4",
    ax=ax
)
ax.set_title("Average Sharing Bike by Hour", loc="center", fontsize=30)
ax.set_ylabel("Average Users", fontsize=20)
ax.set_xlabel("Hour (00-23)", fontsize=20)
ax.set_xticks(range(0, 24))
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
ax.grid(True)
st.pyplot(fig)

# --- Footer / Conclusion ---
st.caption('Copyright (c) Jonatan 2025')