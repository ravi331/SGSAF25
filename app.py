
import streamlit as st
import pandas as pd
from datetime import datetime

# ---------- CONFIG ----------
ADMIN_PASSWORD = "sgs2025"
REG_FILE = "registrations.csv"
NOTICE_FILE = "notices.csv"
EVENT_DATE = "2025-12-20 17:00:00"  # YYYY-MM-DD HH:MM:SS
APP_TITLE = "SGS AnnualFunction 2025"
# -----------------------------

st.set_page_config(page_title=APP_TITLE, layout="wide")

# Load CSV files (create if not exist)
try:
    reg_df = pd.read_csv(REG_FILE)
except:
    reg_df = pd.DataFrame(columns=["Timestamp","Name","Class","Section","Item","Status"])
    reg_df.to_csv(REG_FILE,index=False)

try:
    notice_df = pd.read_csv(NOTICE_FILE)
except:
    notice_df = pd.DataFrame(columns=["Timestamp","Title","Message","PostedBy"])
    notice_df.to_csv(NOTICE_FILE,index=False)

# Tabs
tabs = st.tabs(["🏠 Home","🗞️ News & Notices","🕒 Day & Time","📝 Registration","📋 Registered List","🔐 Admin Login"])

# ---------- Tab 1: Home ----------
with tabs[0]:
    st.image("logo.png", width=200)
    st.title("St. Gregorios H.S. School")
    st.subheader("45th Annual Day - Talent Meets Opportunity")
    st.image("mascot.png", width=250)

    # Countdown Timer
    event_dt = datetime.strptime(EVENT_DATE, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    delta = event_dt - now
    if delta.total_seconds() > 0:
        days = delta.days
        hours = (delta.seconds)//3600
        minutes = (delta.seconds % 3600)//60
        st.markdown(f"### 🎉 Annual Function ({EVENT_DATE.split(' ')[0]}) starts in {days} days, {hours} hours, {minutes} minutes")
    else:
        st.markdown("### 🎉 The Annual Function has begun!")

# ---------- Tab 2: News & Notices ----------
with tabs[1]:
    st.header("Latest News & Notices")
    if notice_df.empty:
        st.write("No notices yet.")
    else:
        for idx,row in notice_df.sort_values(by="Timestamp", ascending=False).iterrows():
            st.markdown(f"**{row['Title']}**  \\  {row['Message']}  \\ *Posted by {row['PostedBy']}*")

# ---------- Tab 3: Day & Time ----------
with tabs[2]:
    st.header("Event Schedule")
    st.write("Upload or maintain schedule separately in the CSV or embed PDF for full details.")
    st.info("You can maintain a schedule CSV locally or update the app code to load a schedule file.")

# ---------- Tab 4: Registration ----------
with tabs[3]:
    st.header("Student Registration Form")
    with st.form("reg_form"):
        name = st.text_input("Student Name")
        sclass = st.text_input("Class")
        sec = st.text_input("Section")
        item = st.text_input("Item Name / Performance")
        submitted = st.form_submit_button("Register")
        if submitted:
            if not name or not sclass or not sec or not item:
                st.error("Please fill all fields before submitting.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                reg_df = pd.read_csv(REG_FILE)
                reg_df = reg_df.append({ "Timestamp":timestamp,"Name":name,"Class":sclass,
                                        "Section":sec,"Item":item,"Status":"Pending"}, ignore_index=True)
                reg_df.to_csv(REG_FILE,index=False)
                st.success(f"{name} registered successfully!")

# ---------- Tab 5: Registered List ----------
with tabs[4]:
    st.header("All Registrations")
    st.dataframe(reg_df.sort_values(by="Timestamp", ascending=False))

# ---------- Tab 6: Admin Login ----------
with tabs[5]:
    st.header("Admin Login")
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.success("Login successful! You can manage notices below.")
            # Add Notice
            st.subheader("Post a New Notice")
            with st.form("notice_form"):
                title = st.text_input("Notice Title")
                message = st.text_area("Message")
                posted_by = st.text_input("Posted By")
                post_btn = st.form_submit_button("Post Notice")
                if post_btn:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    notice_df = pd.read_csv(NOTICE_FILE)
                    notice_df = notice_df.append({ "Timestamp":timestamp,"Title":title,"Message":message,
                                                  "PostedBy":posted_by}, ignore_index=True)
                    notice_df.to_csv(NOTICE_FILE,index=False)
                    st.success("Notice posted successfully!")
        else:
            st.error("Incorrect password!")
