import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import plotly.express as px
sns.set(style='dark')

semuanya_df = pd.read_csv("https://raw.githubusercontent.com/shelenayn/dicoding/main/semuanya_data.csv")
semuanya_df.head()

semuanya_df.info()

datetime_columns = ["order_delivered_customer_date","review_creation_date"]
semuanya_df.sort_values(by="order_delivered_customer_date", inplace=True)
semuanya_df.reset_index(inplace=True)
 
for column in datetime_columns:
    semuanya_df[column] = pd.to_datetime(semuanya_df[column])

semuanya_df.info()

min_date = semuanya_df["order_delivered_customer_date"].min()
max_date = semuanya_df["order_delivered_customer_date"].max()
 
with st.sidebar:
    st.image("https://raw.githubusercontent.com/shelenayn/dicoding/main/logo_shelena.png")
    

st.header('Shelena Dashboard :sparkles:')

st.subheader('Rekapitulasi Penjualan')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = semuanya_df.order_item_id.count()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(semuanya_df.price.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    semuanya_df["order_delivered_customer_date"],
    semuanya_df["price"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


###########################################################
st.subheader('Grafik Kepuasan Pelanggan')
monthly_sales = semuanya_df.resample('M', on='review_creation_date').agg({
    'review_score': 'sum'
})

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=monthly_sales.index, y=monthly_sales['review_score'], marker='o', ax=ax)

plt.xlabel('Tanggal')
plt.ylabel('Score Kepuasan Pelanggan')
plt.title('Grafik Kepuasan Pelanggan')

plt.grid(True)
st.pyplot(fig)

#############################################################################################################
#Menyembunyikan peringatan tentang penggunaan global pyplot

st.subheader('Demografi Pelanggan')
st.set_option('deprecation.showPyplotGlobalUse', False)

bystate_df = semuanya_df.groupby(by="customer_state").order_item_id.nunique().reset_index()
bystate_df.rename(columns={
    "order_item_id": "customer_count"
}, inplace=True)

# Pengaturan warna
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Membuat plot
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="customer_count", 
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors_,
    ax=ax
)
ax.set_title("Number of Customer by State", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)

# Menampilkan plot menggunakan st.pyplot()
st.pyplot(fig)
