import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Konfigurasi halaman
df = pd.read_csv("df_baru.csv")
df['created_at_x'] = pd.to_datetime(df['created_at_x'], errors='coerce')
df['shipped_at'] = pd.to_datetime(df['shipped_at'], errors='coerce')
df['delivered_at'] = pd.to_datetime(df['delivered_at'], errors='coerce')
df['returned_at'] = pd.to_datetime(df['returned_at'], errors='coerce')

st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("📊 Dashboard Analisis Penjualan Pakaian")
# Styling Tema Gelap dan Font Putih (tetap saya pertahankan)
st.markdown("""
    <style>
    /* Umum: background dan teks utama */
    html, body, .main, .stApp {
        background-color: #0e1a2b !important;
        color: white !important;
        font-family: 'Arial', sans-serif;
    }

    h1, h2, h3, h4, h5, h6, label, span, div {
        color: white !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0083B8 !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Selectbox (dropdown) tahun filter */
    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #005f8e !important;
        color: white !important;
        border-radius: 5px !important;
        border: 1px solid white !important;
    }

    section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {
        color: white !important;
        background-color: #005f8e !important;
    }

    div[data-baseweb="popover"] {
        background-color: #005f8e !important;
        color: white !important;
    }

    li[role="option"] {
        background-color: #005f8e !important;
        color: white !important;
    }

    li[role="option"]:hover {
        background-color: #007bb8 !important;
        color: white !important;
    }

    div[role="combobox"] > div {
        color: white !important;
    }

    /* Radio button teks */
    .stRadio label, .stRadio div {
        color: white !important;
    }

    /* Metric box */
    .stMetric label, .stMetric div {
        color: white !important;
    }

    /* Plotly chart */
    .stPlotlyChart div, .stPlotlyChart text {
        color: white !important;
    }

    /* HEADER bagian atas (Deploy bar) */
    header[data-testid="stHeader"] {
        background-color: #0e1a2b !important;
        color: white !important;
        border-bottom: 1px solid #1a1a1a !important;
    }

    header[data-testid="stHeader"] * {
        color: white !important;
    }

    /* Footer dan menu Streamlit (opsional sembunyikan) */
    footer, #MainMenu {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)


# Sidebar Tahun Filter
st.sidebar.header("Filter Data")
tahun_options = ["Semua Tahun"] + sorted(df['created_at_x'].dt.year.dropna().unique().astype(int).tolist())
tahun_terpilih = st.sidebar.selectbox("Pilih Tahun", options=tahun_options)

# Filter Umur
st.sidebar.markdown("### Filter Umur Pelanggan")
min_umur = int(df['age'].min())
max_umur = int(df['age'].max())

umur_range = st.sidebar.slider(
    "Pilih Rentang Umur",
    min_value=min_umur,
    max_value=max_umur,
    value=(min_umur, max_umur)
)
if tahun_terpilih == "Semua Tahun":
    df_tahun = df.copy()
else:
    df_tahun = df[df['created_at_x'].dt.year == tahun_terpilih]

# Filter berdasarkan umur
df_tahun = df_tahun[(df_tahun['age'] >= umur_range[0]) & (df_tahun['age'] <= umur_range[1])]

# ==============================
# Styling khusus agar radio jadi horizontal dan font besar
st.markdown(
    """
    <style>
    div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 40px !important;
    }
    div[role="radiogroup"] label {
        font-size: 22px !important;
        font-weight: bold !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Radio menu fitur
st.markdown("### Pilih Fitur", unsafe_allow_html=True)
menu = st.radio("", ["🛍️ Produk", "👥 Pelanggan", "🚚 Pengiriman & Retur", "💰 Keuangan"])

st.markdown("<hr style='border: 1px solid #999999;'>", unsafe_allow_html=True)

# =============================
# FITUR 1 - PRODUK
# =============================
if menu == "🛍️ Produk":
    st.title("📦 Analisis Produk")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔝 7 Produk Terlaris")
        produk_terlaris = df_tahun['name'].value_counts().head(7)
        produk_terlaris.index = [label[:20] + '...' if len(label) > 20 else label for label in produk_terlaris.index]
        fig1, ax1 = plt.subplots()
        sns.set_style("white")
        ax1.set_facecolor("#0e1a2b")
        fig1.patch.set_facecolor('#0e1a2b')
        sns.barplot(x=produk_terlaris.values, y=produk_terlaris.index, ax=ax1, color="#0083B8")
        ax1.set_xlabel("Jumlah Terjual", color='white')
        ax1.set_ylabel("Produk", color='white')
        ax1.set_title("Top 7 Produk Terlaris", color='white')
        ax1.tick_params(colors='white')
        sns.despine()
        st.pyplot(fig1)

    with col2:
        st.markdown("#### 📊 Distribusi Kategori Produk (Top 7)")
        kategori_populer = df_tahun['category'].value_counts().head(7)
        kategori_populer.index = [label[:20] + '...' if len(label) > 20 else label for label in kategori_populer.index]
        fig2, ax2 = plt.subplots()
        sns.set_style("white")
        ax2.set_facecolor("#0e1a2b")
        fig2.patch.set_facecolor('#0e1a2b')
        sns.barplot(x=kategori_populer.values, y=kategori_populer.index, ax=ax2, color="#0083B8")
        ax2.set_xlabel("Jumlah", color='white')
        ax2.set_ylabel("Kategori", color='white')
        ax2.set_title("Top 7 Kategori Produk", color='white')
        ax2.tick_params(colors='white')
        sns.despine()
        st.pyplot(fig2)

elif menu == "👥 Pelanggan":
    st.title("👥 Analisis Pelanggan")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Distribusi Usia Pelanggan")
        usia_fig, ax = plt.subplots()
        ax.set_facecolor('#0e1a2b') 
        df_tahun['age'].dropna().astype(int).hist(bins=20, ax=ax, color="#0083B8")
        ax.set_title("Distribusi Usia", color='white')
        ax.set_xlabel("Usia", color='white')
        ax.set_ylabel("Jumlah", color='white')
        ax.tick_params(colors='white')
        usia_fig.patch.set_facecolor('#0e1a2b')
        st.pyplot(usia_fig)

    with col2:
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            st.markdown("#### 🌍 Top 5 Negara")
            st.dataframe(df_tahun['country'].value_counts().head(5))
        with subcol2:
            st.markdown("#### 🌐 Sumber Trafik")
            st.dataframe(df_tahun['traffic_source'].value_counts())

        # Visualisasi Pie Chart: Distribusi Gender Pelanggan
        gender_df = df_tahun["gender"].value_counts().reset_index()
        gender_df.columns = ["Gender", "Jumlah"]
        gender_df["Gender"] = gender_df["Gender"].replace({"M": "👨 Laki-laki", "F": "👩 Perempuan"})

        colors_gender = ['#003399', '#66B2FF']

        fig_gender = px.pie(
            gender_df,
            names="Gender",
            values="Jumlah",
            title="Distribusi Gender Pelanggan",
            color_discrete_sequence=colors_gender
        )
        fig_gender.update_traces(
            textposition='inside',
            textinfo='percent+label',
            pull=[0.03, 0.03],
            marker=dict(line=dict(color='#000000', width=1))
        )
        fig_gender.update_layout(
            showlegend=True,
            height=500,
            width=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"),
            legend=dict(font=dict(size=14))
        )
        st.plotly_chart(fig_gender, use_container_width=True, key="gender_pie_chart")

# =============================
# FITUR 3 - PENGIRIMAN & RETUR
# =============================
elif menu == "🚚 Pengiriman & Retur":
    st.title("🚚 Analisis Pengiriman & Retur")
    col1, col2, col3 = st.columns(3)

    total_transaksi = len(df_tahun)
    total_retur = df_tahun['returned_at'].notna().sum()
    persentase_retur = (total_retur / total_transaksi * 100) if total_transaksi > 0 else 0

    col1.metric("Total Transaksi", f"{total_transaksi:,}")
    col2.metric("Jumlah Retur", f"{total_retur:,}")
    col3.metric("Persentase Retur", f"{persentase_retur:.2f}%")

    df_tahun['waktu_pengiriman'] = (df_tahun['delivered_at'] - df_tahun['shipped_at']).dt.days
    rata_pengiriman = df_tahun['waktu_pengiriman'].mean()
    st.markdown(f"#### ⏱️ Rata-rata Waktu Pengiriman: {rata_pengiriman:.2f} hari")

    st.markdown("#### 🔁 Produk Paling Sering Diretur")
    st.dataframe(df_tahun[df_tahun['returned_at'].notna()]['name'].value_counts().head(5))

# =============================
# FITUR 4 - KEUANGAN
# =============================
elif menu == "💰 Keuangan":
    st.title("💰 Analisis Keuangan")

    df_tahun['margin'] = df_tahun['sale_price'] - df_tahun['cost']
    pendapatan_total = df_tahun[df_tahun['delivered_at'].notna()]['sale_price'].sum()
    rata_rata_margin = df_tahun[df_tahun['delivered_at'].notna()]['margin'].mean()
    margin_per_produk = df_tahun.groupby('name')['margin'].sum().sort_values(ascending=False).head(10).reset_index()

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        st.metric("Total Pendapatan (Penjualan Sukses)", f"${pendapatan_total:,.2f}")

    with col2:
        st.metric("Rata-rata Margin/Transaksi", f"${rata_rata_margin:,.2f}")

    with col3:
        st.markdown("#### 🥇 Produk dengan Margin Tertinggi")
        st.dataframe(margin_per_produk.rename(columns={"name": "Produk", "margin": "Total Margin"}))

    st.markdown("---")

    st.markdown("#### 📅 Tren Penjualan Harian")
    df_tahun['tanggal'] = df_tahun['created_at_x'].dt.date
    tren_penjualan = df_tahun[df_tahun['delivered_at'].notna()].groupby('tanggal')['sale_price'].sum().reset_index()

    fig_tren, ax_tren = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=tren_penjualan, x='tanggal', y='sale_price', ax=ax_tren, color="#2CA6FF")
    ax_tren.set_title("Tren Total Penjualan per Hari", color='white')
    ax_tren.set_xlabel("Tanggal", color='white')
    ax_tren.set_ylabel("Total Penjualan (USD)", color='white')
    ax_tren.tick_params(axis='x', rotation=45, colors='white')
    fig_tren.patch.set_facecolor('#0e1a2b')
    st.pyplot(fig_tren)
