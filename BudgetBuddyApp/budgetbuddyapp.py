import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

<<<<<<< Updated upstream
=======
# Fungsi untuk membuat koneksi ke database
db_path = '~\BudgetBuddyApp\users.db'
def create_connection():
    conn = sqlite3.connect(db_path)
    return conn
>>>>>>> Stashed changes

st.set_page_config(page_title="BudgetBuddy", page_icon="💰")


if 'transactions' not in st.session_state:
    st.session_state['transactions'] = []

st.title("BudgetBuddy 💰")

st.header("Tambah Transaksi Baru")
with st.form("transaction_form"):
    date = st.date_input("Tanggal")
    category = st.selectbox("Kategori", ["Pendapatan", "Pengeluaran"])
    description = st.text_input("Deskripsi")
    amount = st.number_input("Jumlah", step=1000.0, format="%.2f")
    submit = st.form_submit_button("Tambahkan Transaksi")

    if submit:
        st.session_state['transactions'].append({"Tanggal": date, "Kategori": category, "Deskripsi": description, "Jumlah": amount})
        st.success("Transaksi berhasil ditambahkan!")

st.header("Riwayat Transaksi")
if st.session_state['transactions']:
    df = pd.DataFrame(st.session_state['transactions'])
    st.dataframe(df)

    st.header("Ringkasan Pengeluaran")
    income = df[df['Kategori'] == "Pendapatan"]['Jumlah'].sum()
    expense = df[df['Kategori'] == "Pengeluaran"]['Jumlah'].sum()
    balance = income - expense

    st.metric("Total Pendapatan", f"Rp.{income:,.2f}")
    st.metric("Total Pengeluaran", f"Rp.{expense:,.2f}")
    st.metric("Saldo Saat Ini", f"Rp.{balance:,.2f}")

    st.header("Pendapatan vs Pengeluaran")
    fig, ax = plt.subplots()
    ax.pie([income, expense], labels=["Pendapatan", "Pengeluaran"], autopct='%1.1f%%', colors=["#76c7c0", "#ff6f69"])
    st.pyplot(fig)
else:
    st.info("Belum ada transaksi yang ditambahkan.")


st.markdown("---")
st.markdown("Developed with ❤️ by nopal")
