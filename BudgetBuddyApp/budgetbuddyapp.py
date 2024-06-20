import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import create_user, get_user, add_transaction, get_transactions
from datetime import datetime
import base64

st.set_page_config(page_title="BudgetBuddy", page_icon="💰")

# Fungsi untuk mengambil daftar bulan-tahun unik dari riwayat transaksi
def get_unique_dates(transactions):
    dates = pd.to_datetime(transactions['date'])
    unique_dates = dates.dt.strftime('%Y-%m').sort_values().unique()
    return unique_dates

# Fungsi untuk membuat tautan unduh
def get_table_download_link(df, filename, file_format):
    if file_format == 'CSV':
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Unduh file CSV</a>'
    elif file_format == 'PDF':
        pdf = df.to_html(index=False)
        href = f'<a href="data:application/pdf,{pdf}" download="{filename}">Unduh file PDF</a>'
    return href

# Fungsi untuk menampilkan form unduh transaksi per bulan
def download_transactions(transactions):
    st.subheader("Unduh Transaksi per Bulan")
    unique_dates = get_unique_dates(transactions)
    selected_date = st.selectbox("Pilih Bulan dan Tahun", unique_dates)

    if st.button("Unduh sebagai CSV"):
        filtered_transactions = transactions[pd.to_datetime(transactions['date']).dt.strftime('%Y-%m') == selected_date]
        csv_filename = f"transactions_{selected_date}.csv"
        st.markdown(get_table_download_link(filtered_transactions, csv_filename, 'CSV'), unsafe_allow_html=True)

    if st.button("Unduh sebagai PDF"):
        filtered_transactions = transactions[pd.to_datetime(transactions['date']).dt.strftime('%Y-%m') == selected_date]
        pdf_filename = f"transactions_{selected_date}.pdf"
        st.markdown(get_table_download_link(filtered_transactions, pdf_filename, 'PDF'), unsafe_allow_html=True)

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        user = get_user(username, password)
        if user:
            st.session_state["user_id"] = user[0]
            st.session_state["username"] = username
            st.success(f"Selamat datang {username}")
            st.rerun()
        else:
            st.error("Username atau password salah")

def register():
    st.subheader("Buat Akun Baru")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    if st.button("Register"):
        if new_user and new_password:
            try:
                create_user(new_user, new_password)
                st.success("Akun berhasil dibuat")
                st.info("Silakan login dengan akun yang baru dibuat")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Harap isi semua field")

def main_page():
    st.header("Tambah Transaksi Baru")
    with st.form("transaction_form"):
        date = st.date_input("Tanggal")
        category = st.selectbox("Kategori", ["Pendapatan", "Pengeluaran"])
        description = st.text_input("Deskripsi")
        amount = st.number_input("Jumlah", step=1000.0, format="%.2f")
        submit = st.form_submit_button("Tambahkan Transaksi")

        if submit:
            add_transaction(st.session_state["user_id"], date, category, description, amount)
            st.success("Transaksi berhasil ditambahkan!")

    st.header("Riwayat Transaksi")
    transactions = get_transactions(st.session_state["user_id"])
    if transactions:
        df = pd.DataFrame(transactions, columns=["ID", "User ID", "Tanggal", "Kategori", "Deskripsi", "Jumlah"])
        st.dataframe(df.drop(columns=["ID", "User ID"]))

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
        download_transactions(df)
    else:
        st.info("Belum ada transaksi yang ditambahkan.")

    st.markdown("---")
    st.markdown("Developed with ❤️ by Team BudgetBuddy")

def main():
    st.title("BudgetBuddy 💰")
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None

    if st.session_state["user_id"] is None:
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            login()
        elif choice == "Register":
            register()
    else:
        menu = ["Main Page", "Logout"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Logout":
            st.session_state["user_id"] = None
            st.session_state["username"] = None
            st.success("Anda berhasil logout")
            st.rerun()
        else:
            main_page()

if __name__ == '__main__':
    main()