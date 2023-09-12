import streamlit as st
import pandas as pd
import io



def process_files(df1, df2):
    # Menggabungkan data kolom B dari file 2 dengan data kolom C dari file 1
    df3 = pd.merge(df2, df1[['SKU', 'KO - TOKPED']], on='SKU', how='left')

    # Memindahkan data kolom 'KO - TOKPED' ke kolom 'Harga (Rp)*' jika 'KO - TOKPED' tidak kosong
    df3.loc[df3['KO - TOKPED'].notnull(), 'Harga (Rp)*'] = df3['KO - TOKPED']

    # Menghapus kolom 'KO - TOKPED'
    df3.drop(columns=['KO - TOKPED'], inplace=True)

    # Menghapus duplikasi pada kolom 'Nama Produk'
    df3.drop_duplicates(subset='Nama Produk', inplace=True)

    # Mengubah nilai 100 menjadi 99999999 dalam kolom 'Harga (Rp)*'
    df3['Harga (Rp)*'].replace(-100, 99999999, inplace=True)


    return df3



def main():
    st.title("File Processor")

    # Unggah file pertama
    st.subheader("Upload File MODAL")
    file1 = st.file_uploader("Pilih file Excel", type=["xlsx"], key="file1")

    # Unggah file kedua
    st.subheader("Upload File TOPED")
    file2 = st.file_uploader("Pilih file Excel", type=["xlsx"], key="file2")

    if file1 and file2:
        # Baca file pertama
        df1 = pd.read_excel(file1)

        # Baca file kedua
        df2 = pd.read_excel(file2)

        # Proses file
        df3 = process_files(df1, df2)

        

        # Tampilkan hasil
        st.subheader("Hasil Penggabungan")
        st.dataframe(df3)

        # Simpan file hasil
        output_file = io.BytesIO()
        with pd.ExcelWriter(output_file, mode='xlsxwriter') as writer:
            df3.to_excel(writer, index=False)
        output_file.seek(0)

        # Tampilkan tombol unduh
        st.subheader("Unduh File Hasil")
        st.download_button(label="Unduh File", data=output_file, file_name="result.xlsx")

if __name__ == "__main__":
    main()

    
