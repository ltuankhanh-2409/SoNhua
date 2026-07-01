import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
def connect_google(ten_json,sheet_id):
    try:
        # Chạy trên Streamlit
        import streamlit as st
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            st.secrets["gcp_service_account"],
            SCOPE
        )
    except Exception as e:
        import streamlit as st
        st.error(f"Lỗi đọc secrets: {e}")
        raise
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id)
