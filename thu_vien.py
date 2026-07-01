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
    except:
        # Chạy trên Windows
        json_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            ten_json
        )
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            json_path,
            SCOPE
        )
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id)
