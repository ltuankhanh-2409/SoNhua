import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_google(ten_json, sheet_id):
    import streamlit as st

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"],
        SCOPE
    )

    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id)
