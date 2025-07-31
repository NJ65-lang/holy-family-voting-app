
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
SHEET_NAME = "HFNS_VOTES"
SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = "credentials.json"

# Load allowed student IDs
student_df = pd.read_csv("student_ids.csv")
allowed_ids = student_df["student_id"].astype(str).tolist()

# Google Sheet init
def get_gsheet_client():
    
    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    import json
    from google.auth.transport.requests import Request
    creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
   
    return gspread.authorize(creds)

def save_vote_to_sheet(student_id, votes):
    client = get_gsheet_client()
    sheet = client.open(SHEET_NAME).sheet1
    sheet.append_row([student_id] + votes)

def already_voted(student_id):
    client = get_gsheet_client()
    sheet = client.open(SHEET_NAME).sheet1
    records = sheet.get_all_records()
    return any(row["student_id"] == student_id for row in records)

# App UI
st.set_page_config(page_title="HFNS Voting", layout="centered")
st.title("🗳️ Holy Family Nirankari School")
st.subheader("Student Council Election 2025")

student_id = st.text_input("Enter your Student ID")

if student_id:
    if student_id not in allowed_ids:
        st.error("❌ Invalid Student ID. Please try again.")
    elif already_voted(student_id):
        st.warning("⚠️ You have already voted. Thank you!")
    else:
        st.success("✅ Verified. Please cast your votes below.")

        vote1 = st.radio("Head Boy", ["Rahul", "Arjun", "Dev"], key="hb")
        vote2 = st.radio("Head Girl", ["Sneha", "Priya", "Meera"], key="hg")
        vote3 = st.radio("Prefect - Discipline", ["Karan", "Amit", "Raj"], key="disc")
        vote4 = st.radio("Prefect - Dress", ["Simran", "Neha", "Anjali"], key="dress")
        vote5 = st.radio("Prefect - Cleanliness", ["Rohit", "Vikram", "Aditya"], key="clean")

        if st.button("Submit My Vote"):
            save_vote_to_sheet(student_id, [vote1, vote2, vote3, vote4, vote5])
            st.success("🎉 Vote submitted successfully! Thank you.")
