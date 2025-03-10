import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    Aotizhongxin_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Aotizhongxin_20130301-20170228.csv', index_col='No')
    Changping_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Changping_20130301-20170228.csv', index_col='No')
    Dingling_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Dingling_20130301-20170228.csv', index_col='No')
    Dongsi_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Dongsi_20130301-20170228.csv', index_col='No')
    Guanyuan_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Guanyuan_20130301-20170228.csv', index_col='No')
    Gucheng_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Gucheng_20130301-20170228.csv', index_col='No')
    Huairou_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Huairou_20130301-20170228.csv', index_col='No')
    Nongzhanguan_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Nongzhanguan_20130301-20170228.csv', index_col='No')
    Shunyi_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Shunyi_20130301-20170228.csv', index_col='No')
    Tiantan_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Tiantan_20130301-20170228.csv', index_col='No')
    Wanliu_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Wanliu_20130301-20170228.csv', index_col='No')
    Wanshouxigong_df = pd.read_csv('dataset/PRSA_Data_20130301-20170228/PRSA_Data_Wanshouxigong_20130301-20170228.csv', index_col='No')

    df = pd.concat([Aotizhongxin_df, Changping_df, Dingling_df, Dongsi_df, Guanyuan_df, Gucheng_df, Huairou_df, Nongzhanguan_df, Shunyi_df, Tiantan_df, Wanliu_df, Wanshouxigong_df], ignore_index=True)
    
    df['month'] = pd.to_datetime(df['month'], format='%m').dt.strftime('%B')  # Ubah angka bulan ke nama bulan
    return df

df = load_data()

# Sidebar navigation
st.sidebar.title("Analisis Curah Hujan 2013-2017")
option = st.sidebar.selectbox("Pilih Analisis:", [
    "Curah Hujan Tiap Bulan",
    "Faktor Penyebab Curah Hujan",
    "Daerah dengan Curah Hujan Tertinggi"
])

# Curah Hujan Tiap Bulan
if option == "Curah Hujan Tiap Bulan":
    st.title("Curah Hujan Tiap Bulan (2013-2017)")
    year = st.selectbox("Pilih Tahun:", df['year'].unique())
    months = list(df['month'].unique())
    month_range = st.slider("Pilih Rentang Bulan:", 1, 12, (1, 12))
    month_names = [pd.to_datetime(str(m), format='%m').strftime('%B') for m in range(month_range[0], month_range[1] + 1)]
    
    monthly_rainfall = df[(df['year'] == year) & (df['month'].isin(month_names))].groupby('month')['RAIN'].mean().reindex(month_names)
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=monthly_rainfall.index, y=monthly_rainfall.values, marker='o')
    plt.xlabel("Bulan")
    plt.ylabel("Curah Hujan (mm)")
    plt.title(f"Rata-rata Curah Hujan Bulanan - {year}")
    plt.xticks(rotation=45)
    st.pyplot(plt)

# Faktor Penyebab Curah Hujan
elif option == "Faktor Penyebab Curah Hujan":
    st.title("Faktor Penyebab Curah Hujan")
    st.write("Analisis hubungan antara curah hujan dan faktor lingkungan seperti suhu, tekanan udara, dan kelembaban.")
    
    selected_factor = st.selectbox("Pilih Faktor:", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'WSPM'])
    
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=df[selected_factor], y=df['RAIN'])
    plt.xlabel(selected_factor.capitalize())
    plt.ylabel("Curah Hujan (mm)")
    plt.title(f"Hubungan {selected_factor.capitalize()} dengan Curah Hujan")
    st.pyplot(plt)

    st.write(df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr())

# Daerah dengan Curah Hujan Tertinggi
elif option == "Daerah dengan Curah Hujan Tertinggi":
    st.title("Daerah dengan Curah Hujan Tertinggi")
    station = st.selectbox("Pilih Stasiun:", df['station'].unique())
    station_year_rain = df.groupby(['station', 'year'])['RAIN'].sum().reset_index().sort_values(by='RAIN', ascending=False)
    filtered_data = station_year_rain[station_year_rain['station'] == station]
    plt.figure(figsize=(10, 5))
    sns.barplot(x=filtered_data['year'], y=filtered_data['RAIN'])
    plt.title(f'Total Curah Hujan di {station} per Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Total Curah Hujan (mm)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)
