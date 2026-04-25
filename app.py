import streamlit as st
import pandas as pd
from datetime import datetime
import random

file = "donors.csv"

# Load data
df = pd.read_csv(file)

st.title("Blood Bank Management System")

# -------- DASHBOARD --------
st.subheader("Blood Availability Summary")
st.write(df["blood_group"].value_counts())

# -------- MENU --------
menu = ["Register Donor", "View Donors", "Search Blood", "Hospital Allocation"]
choice = st.sidebar.selectbox("Menu", menu)

# -------- REGISTER DONOR --------
if choice == "Register Donor":
    st.header("Register Donor")

    name = st.text_input("Name")
    blood = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    contact = st.text_input("Contact")
    date = st.date_input("Last Donation Date")

    if st.button("Register"):
        new = pd.DataFrame([[name, blood, contact, date]], columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(file, index=False)
        st.success("Donor Registered")

# -------- VIEW DONORS --------
elif choice == "View Donors":
    st.header("All Donors")

    today = datetime.today()

    def status(d):
        last = datetime.strptime(str(d), "%Y-%m-%d")
        return "Eligible" if (today - last).days >= 90 else "Not Eligible"

    df["Status"] = df["last_donation"].apply(status)
    st.dataframe(df)

# -------- SEARCH BLOOD --------
elif choice == "Search Blood":
    st.header("Smart Blood Matching System")

    blood = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])

    today = datetime.today()

    def eligible(d):
        last = datetime.strptime(str(d), "%Y-%m-%d")
        return (today - last).days >= 90

    df["eligible"] = df["last_donation"].apply(eligible)

    result = df[(df["blood_group"] == blood) & (df["eligible"] == True)]

    if not result.empty:
        st.success("Eligible Donors Found")
        st.dataframe(result)
    else:
        st.error("No eligible donors available")

# -------- HOSPITAL ALLOCATION --------
elif choice == "Hospital Allocation":
    st.header("Smart Hospital Blood Allocation System")

    hospitals = ["Apollo", "CMC", "GH", "CityCare", "LifeLine",
                 "Global", "Sunrise", "MedPlus", "CarePlus", "HealthFirst"]

    blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

    if st.button("Generate Hospital Requests"):

        requests = []

        for h in hospitals:
            requests.append({
                "hospital": h,
                "blood": random.choice(blood_groups),
                "units": random.randint(1, 3)
            })

        st.subheader("Generated Requests")
        import pandas as pd

        req_df = pd.DataFrame(requests)
        st.dataframe(req_df)

        # -------- ALLOCATION LOGIC --------
        today = datetime.today()

        def eligible(d):
            last = datetime.strptime(str(d), "%Y-%m-%d")
            return (today - last).days >= 90

        df["eligible"] = df["last_donation"].apply(eligible)

        st.subheader("Allocation Results")

        for r in requests:
            available = df[(df["blood_group"] == r["blood"]) & (df["eligible"] == True)]

            if len(available) >= r["units"]:
                st.success(f"{r['hospital']} → Allocated {r['units']} units of {r['blood']}")
            else:
                st.error(f"{r['hospital']} → Not enough donors for {r['blood']}")