
import streamlit as st
import os
import fitz  # PyMuPDF
import docx2txt
import pandas as pd

st.set_page_config(page_title="HR ATS Dashboard", layout="wide")
st.sidebar.title("🔐 HR Login")

USER_CREDENTIALS = {"admin": "hr123"}
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username in USER_CREDENTIALS and password == USER_CREDENTIALS[username]:
    st.sidebar.success("Login Berhasil ✅")
    st.title("📊 HR ATS Dashboard - Filter & Penilaian CV")

    folder_path = "uploaded_cvs"
    files = [f for f in os.listdir(folder_path) if f.endswith((".pdf", ".docx"))] if os.path.exists(folder_path) else []
    keywords = st.text_input("Masukkan kata kunci pencarian (pisahkan dengan koma):")

    def extract_text(file_path):
        if file_path.endswith(".pdf"):
            with fitz.open(file_path) as doc:
                return "".join(page.get_text() for page in doc)
        elif file_path.endswith(".docx"):
            return docx2txt.process(file_path)
        return ""

    if files and keywords:
        keys = [k.strip().lower() for k in keywords.split(",")]
        result_data = []

        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            content = extract_text(file_path)
            score = sum(1 for k in keys if k in content.lower())
            status = "Lolos" if score >= len(keys) // 2 else "Tidak Lolos"
            data = {"Nama File": file_name, "Skor": score, "Status": status}
            for k in keys:
                data[k] = "✅" if k in content.lower() else "❌"
            result_data.append(data)

        df = pd.DataFrame(result_data)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Hasil sebagai CSV", csv, "hasil_ats.csv", "text/csv")
else:
    st.warning("Masukkan username dan password untuk akses dashboard HR.")
    st.stop()
