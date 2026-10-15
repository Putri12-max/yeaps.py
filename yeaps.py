import datetime
import pandas as pd
import streamlit as st


# Fungsi pembantu untuk memformat angka ke format Rupiah titik (.) Indonesia
def format_rupiah(angka):
    return f"{int(angka):,}".replace(",", ".")


# Fungsi untuk mengosongkan kembali seluruh sesi transaksi
def reset_data():
    st.session_state["input_nama"] = ""
    st.session_state["metode_pembayaran"] = "Cash"
    st.session_state["produk_dipilih"] = "Laptop Gaming ASUS"
    st.session_state["jumlah_produk_key"] = 0
    st.session_state["pesanan"] = []
    st.rerun()


# Inisialisasi session state agar memori web tetap terjaga dengan baik
if "input_nama" not in st.session_state:
    st.session_state["input_nama"] = ""
if "metode_pembayaran" not in st.session_state:
    st.session_state["metode_pembayaran"] = "Cash"
if "produk_dipilih" not in st.session_state:
    st.session_state["produk_dipilih"] = "Laptop Gaming ASUS"
if "jumlah_produk_key" not in st.session_state:
    st.session_state["jumlah_produk_key"] = 0
if "pesanan" not in st.session_state:
    st.session_state["pesanan"] = []

# Header & Identitas Web Aplikasi Mahasiswa
st.title("ELECTRONIC GERAI")
st.subheader("Sistem Kasir Digital Berbasis Web & Analisis Data Penjualan")
st.markdown(
    "Selamat datang di portal pelayanan *Electronic Gerai*. Silakan lakukan"
    " simulasi transaksi di bawah ini."
)
st.write("📍 *Jl. Teknologi No. 5, Kota Digital, Indonesia | Telp: (021) 87654321*")
st.write("---")


# Komponen Waktu Real-Time (Disesuaikan ke Zona Waktu WIB / UTC+7)
@st.fragment(run_every=1)
def tampilkan_jam_realtime():
    zona_waktu_wib = datetime.timezone(datetime.timedelta(hours=7))
    now = datetime.datetime.now(zona_waktu_wib)
    waktu_sekarang = now.strftime("%d-%m-%Y | Pukul %H:%M:%S WIB")
    st.info(f"📅 Waktu Sistem Berjalan: **{waktu_sekarang}**")


# Memanggil fungsi jam real-time
tampilkan_jam_realtime()

# Waktu statis untuk nota (disesuaikan ke WIB)
zona_waktu_wib = datetime.timezone(datetime.timedelta(hours=7))
waktu_sekarang_static = datetime.datetime.now(zona_waktu_wib).strftime(
    "%d-%m-%Y | Pukul %H:%M:%S WIB"
)

# Form Data Pelanggan
st.markdown("### 👤 Data Pelanggan")
nama_pelanggan = st.text_input(
    "Nama Lengkap Pelanggan",
    placeholder="Silakan masukkan nama pelanggan...",
    key="input_nama",
)
metode_pembayaran = st.selectbox(
    "Pilih Metode Pembayaran yang Digunakan",
    ["Cash", "Debit", "E-Wallet"],
    key="metode_pembayaran",
)

st.write("---")
st.markdown("### 🛒 Katalog & Transaksi Produk")

# Pilihan produk elektronik spesifik
produk_dipilih = st.selectbox(
    "Silakan Pilih Kategori Produk Elektronik",
    [
        "Laptop Gaming ASUS",
        "Smart TV 4K",
        "Smartphone Pro",
        "AC Inverter",
        "Microwave Digital",
    ],
    key="produk_dipilih",
)

# Kamus harga produk spesifik (skala jutaan rupiah)
harga_produk_dict = {
    "Laptop Gaming ASUS": 12000000,
    "Smart TV 4K": 6500000,
    "Smartphone Pro": 5000000,
    "AC Inverter": 4000000,
    "Microwave Digital": 1500000,
}

# Input jumlah barang dengan format bilangan bulat murni (%d)
jumlah_produk = st.number_input(
    "Tentukan Kuantitas Pembelian",
    min_value=0,
    max_value=100,
    step=1,
    format="%d",
    key="jumlah_produk_key",
)

# Kalkulasi subtotal barang saat ini
subtotal_sekarang = harga_produk_dict[produk_dipilih] * jumlah_produk
st.success(
    f"Sub sementara untuk produk **{produk_dipilih}** ({jumlah_produk}"
    f" unit): **Rp {format_rupiah(subtotal_sekarang)}**"
)

# Tombol aksi memasukkan ke keranjang sesi
if st.button("➕ Masukkan ke Daftar Keranjang Belanja"):
    if jumlah_produk > 0:
        st.session_state.pesanan.append({
            "produk": produk_dipilih,
            "jumlah": jumlah_produk,
            "subtotal": subtotal_sekarang,
        })
        st.toast(
            f"Berhasil menambahkan {jumlah_produk} unit {produk_dipilih} ke"
            " keranjang!",
            icon="✅",
        )
    else:
        st.warning("⚠️ Mohon tentukan kuantitas produk dengan benar (minimal 1 unit).")

# Menampilkan rincian daftar belanjaan sementara
if st.session_state.pesanan:
    st.write("---")
    st.markdown("#### 📋 Rekapitulasi Produk dalam Keranjang:")
    for item in st.session_state.pesanan:
        st.write(
            f"• **{item['produk']}** sebanyak **{item['jumlah']} unit** — Total: Rp"
            f" {format_rupiah(item['subtotal'])}"
        )

    # Perhitungan Total, Diskon Tetap Rp200.000, dan Grand Total
    total_belanja = sum(item["subtotal"] for item in st.session_state.pesanan)
    diskon = 200000
    grand_total = max(0, total_belanja - diskon)

    st.warning(
        "🎉 **Promo Spesial Toko / Bulanan:** Anda mendapatkan potongan diskon"
        " loyalitas sebesar **Rp 200.000**!"
    )
    st.write(f"• Total Keseluruhan Belanja: Rp {format_rupiah(total_belanja)}")
    st.write(f"• Potongan Diskon Toko: Rp {format_rupiah(diskon)}")
    st.markdown(
        f"### **Grand Total yang Harus Dibayar: Rp"
        f" {format_rupiah(grand_total)}**"
    )

st.write("---")

# Tombol Proses Transaksi, Cetak Nota, & Visualisasi Analitik
if st.button("💾 Proses & Simpan Transaksi"):
    if st.session_state.pesanan:
        # Konversi data ke format DataFrame Pandas
        df = pd.DataFrame(st.session_state.pesanan)

        # Ekspor otomatis ke berkas CSV lokal
        df.to_csv("pesanan.csv", index=False)
        st.success(
            "📁 Data transaksi berhasil direkam dan diekspor ke format 'pesanan.csv'."
        )

        # ------------------- CETAK NOTA DIGITAL -------------------
        st.markdown("### 🧾 STRUK NOTA DIGITAL RESMI")

        with st.container(border=True):
            st.markdown("### **ELECTRONIC GERAI OFFICIAL**")
            st.caption("Pusat Penjualan & Layanan Perangkat Elektronik Terpadu")
            st.write("--------------------------------------------------")

            nama_tampil = (
                nama_pelanggan if nama_pelanggan.strip() != "" else "Pelanggan Umum"
            )
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Waktu Transaksi** : {waktu_sekarang_static}")
                st.write(f"**Nama Konsumen** : {nama_tampil}")
            with col_b:
                st.write(f"**Metode Bayar** : {metode_pembayaran}")
                st.write("**Status Kasir** : Lunas / Terverifikasi")

            st.write("--------------------------------------------------")
            st.markdown("**Rincian Pembelian Barang:**")

            for item in st.session_state.pesanan:
                st.write(
                    f"• {item['produk']} (x{item['jumlah']}) — Rp"
                    f" {format_rupiah(item['subtotal'])}"
                )

            st.write("--------------------------------------------------")
            st.write(f"Subtotal Sebelum Diskon : Rp {format_rupiah(total_belanja)}")
            st.write(f"Potongan Promo Khusus : Rp {format_rupiah(diskon)}")
            st.markdown(
                f"### **GRAND TOTAL PEMBAYARAN : Rp"
                f" {format_rupiah(grand_total)}**"
            )
            st.write("--------------------------------------------------")
            st.caption(
                "~ Terima kasih atas kunjungan dan kepercayaan Anda kepada Electronic"
                " Gerai ~"
            )
            st.caption("Dokumen digital ini sah dicetak otomatis oleh sistem.")

        st.write("---")

        # Visualisasi Tabel Pandas yang Bersih (Tanpa Indeks)
        st.markdown("### 📊 Tabel Rekapitulasi Data (Pandas DataFrame Terstruktur)")
        st.markdown("Berikut adalah tabel bersih dari struktur data transaksi saat ini:")

        df_tampil = df.copy()
        df_tampil["subtotal"] = df_tampil["subtotal"].apply(
            lambda x: f"Rp {format_rupiah(x)}"
        )
        st.dataframe(df_tampil, hide_index=True)

        # Visualisasi Grafik Statistik Penjualan
        st.markdown("### 📈 Grafik Analisis Statistik Volume Produk")
        st.bar_chart(df.set_index("produk")[["jumlah"]])
    else:
        st.warning(
            "⚠️ Keranjang belanja Anda masih kosong. Silakan tambahkan produk"
            " terlebih dahulu sebelum memproses transaksi."
        )

# Tombol Reset / Clear Sesi Transaksi
st.markdown("---")
st.markdown("*(Gunakan tombol di bawah ini untuk membersihkan sesi formulir)*")
st.button("🔄 Bersihkan Formulir & Mulai Transaksi Baru", on_click=reset_data)
  st.markdown("#### 📋 Rekapitulasi Produk dalam Keranjang:")
  for item in st.session_state.pesanan:
    st.write(
        f"• **{item['produk']}** sebanyak **{item['jumlah']} unit** — Total: Rp"
        f" {format_rupiah(item['subtotal'])}"
    )

  # Perhitungan Total, Diskon Tetap Rp200.000, dan Grand Total
  total_belanja = sum(item["subtotal"] for item in st.session_state.pesanan)
  diskon = 200000
  grand_total = max(0, total_belanja - diskon)

  st.warning(
      "🎉 **Promo Spesial Toko / Bulanan:** Anda mendapatkan potongan diskon"
      " loyalitas sebesar **Rp 200.000**!"
  )
  st.write(f"• Total Keseluruhan Belanja: Rp {format_rupiah(total_belanja)}")
  st.write(f"• Potongan Diskon Toko: Rp {format_rupiah(diskon)}")
  st.markdown(
      f"### **Grand Total yang Harus Dibayar: Rp"
      f" {format_rupiah(grand_total)}**"
  )

st.write("---")

# Tombol Proses Transaksi, Cetak Nota, & Visualisasi Analitik
if st.button("💾 Proses & Simpan Transaksi"):
  if st.session_state.pesanan:
    # Konversi data ke format DataFrame Pandas
    df = pd.DataFrame(st.session_state.pesanan)

    # Ekspor otomatis ke berkas CSV lokal
    df.to_csv("pesanan.csv", index=False)
    st.success(
        "📁 Data transaksi berhasil direkam dan diekspor ke format 'pesanan.csv'."
    )

    # ------------------- CETAK NOTA DIGITAL -------------------
    st.markdown("### 🧾 STRUK NOTA DIGITAL RESMI")

    with st.container(border=True):
      st.markdown("### **ELECTRONIC GERAI OFFICIAL**")
      st.caption("Pusat Penjualan & Layanan Perangkat Elektronik Terpadu")
      st.write("--------------------------------------------------")

      nama_tampil = (
          nama_pelanggan if nama_pelanggan.strip() != "" else "Pelanggan Umum"
      )
      col_a, col_b = st.columns(2)
      with col_a:
        st.write(f"**Waktu Transaksi** : {waktu_sekarang_static}")
        st.write(f"**Nama Konsumen** : {nama_tampil}")
      with col_b:
        st.write(f"**Metode Bayar** : {metode_pembayaran}")
        st.write("**Status Kasir** : Lunas / Terverifikasi")

      st.write("--------------------------------------------------")
      st.markdown("**Rincian Pembelian Barang:**")

      for item in st.session_state.pesanan:
        st.write(
            f"• {item['produk']} (x{item['jumlah']}) — Rp"
            f" {format_rupiah(item['subtotal'])}"
        )

      st.write("--------------------------------------------------")
      st.write(f"Subtotal Sebelum Diskon : Rp {format_rupiah(total_belanja)}")
      st.write(f"Potongan Promo Khusus : Rp {format_rupiah(diskon)}")
      st.markdown(
          f"### **GRAND TOTAL PEMBAYARAN : Rp"
          f" {format_rupiah(grand_total)}**"
      )
      st.write("--------------------------------------------------")
      st.caption(
          "~ Terima kasih atas kunjungan dan kepercayaan Anda kepada Electronic"
          " Gerai ~"
      )
      st.caption("Dokumen digital ini sah dicetak otomatis oleh sistem.")

    st.write("---")

    # Visualisasi Tabel Pandas yang Bersih (Tanpa Indeks)
    st.markdown("### 📊 Tabel Rekapitulasi Data (Pandas DataFrame Terstruktur)")
    st.markdown("Berikut adalah tabel bersih dari struktur data transaksi saat ini:")

    df_tampil = df.copy()
    df_tampil["subtotal"] = df_tampil["subtotal"].apply(
        lambda x: f"Rp {format_rupiah(x)}"
    )
    st.dataframe(df_tampil, hide_index=True)

    # Visualisasi Grafik Statistik Penjualan
    st.markdown("### 📈 Grafik Analisis Statistik Volume Produk")
    st.bar_chart(df.set_index("produk")[["jumlah"]])
  else:
    st.warning(
        "⚠️ Keranjang belanja Anda masih kosong. Silakan tambahkan produk"
        " terlebih dahulu sebelum memproses transaksi."
    )

# Tombol Reset / Clear Sesi Transaksi
st.markdown("---")
st.markdown("*(Gunakan tombol di bawah ini untuk membersihkan sesi formulir)*")
st.button("🔄 Bersihkan Formulir & Mulai Transaksi Baru", on_click=reset_data)
