import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# Fungsi untuk membuat koneksi ke database
def create_connection():
    conn = sqlite3.connect('users.db')
    return conn

# Fungsi untuk mendaftarkan pengguna baru
def register_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# Fungsi untuk memeriksa kredensial pengguna saat login
def login_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Fungsi untuk menampilkan form register
def show_register():
    st.subheader("Buat Akun Baru")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    if st.button("Register"):
        try:
            register_user(new_user, new_password)
            st.success("Akun berhasil dibuat!")
            st.info("Silakan login ke akun Anda.")
        except sqlite3.IntegrityError:
            st.error("Username sudah ada. Silakan pilih username lain.")
            
# Fungsi untuk menampilkan form login
def show_login():
    st.subheader("Login ke Akun Anda")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Selamat datang, {username}!")
            st.rerun()
        else:
            st.error("Username atau Password salah. Silakan coba lagi.")


# Fungsi untuk logout pengguna
def logout_user():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.experimental_rerun()

# Fungsi untuk menampilkan halaman utama aplikasi setelah login
def show_main_app():
    st.subheader(f"Selamat datang, {st.session_state['username']}!")
    st.title("BudgetBuddy 💰")

# Tombol logout
    col1, col2 = st.columns([75, 10])
    with col2:
        if st.button("Logout"):
            logout_user()

    st.header("Tambah Transaksi Baru")
    with st.form("transaction_form"):
        date = st.date_input("Tanggal")
        category = st.selectbox("Kategori", ["Pendapatan", "Pengeluaran"])
        description = st.text_input("Deskripsi")
        amount = st.number_input("Jumlah (Rupiah)", step=1000.0, format="%.2f")
        submit = st.form_submit_button("Tambahkan Transaksi")

        if submit:
            if amount == 0:
                st.error("Tolong isi jumlah transaksi!")
            else:
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

# Konfigurasi halaman
st.set_page_config(page_title="BudgetBuddy", page_icon="💰")

# Inisialisasi state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'transactions' not in st.session_state:
    st.session_state['transactions'] = []

# Menampilkan halaman berdasarkan status login
if st.session_state['logged_in']:
    show_main_app()
else:
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Login":
        show_login()
    elif choice == "Register":
        show_register()
