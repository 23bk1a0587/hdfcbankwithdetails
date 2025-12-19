import streamlit as st
import pandas as pd
from supabase import create_client

# Supabase Configuration
SUPABASE_URL = "https://zrtcysjabwwnfxijxweo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpydGN5c2phYnd3bmZ4aWp4d2VvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjYwNDMzOTAsImV4cCI6MjA4MTYxOTM5MH0.0ySTS3nQVQQif_uNxkk7-olqTLeACLc0KA4rM9UqeeI"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Session State
if "user" not in st.session_state:
    st.session_state.user = None

# Streamlit UI
st.title("HDFC BANK (Supabase)")

menu = ["LOGIN", "REGISTER", "VIEW"]
choice = st.sidebar.selectbox("Menu", menu)

#LOGIN
if choice == "LOGIN":
    st.subheader("Login")

    acc = int(st.number_input("Account Number", step=1))

    if st.button("Login"):
        data = supabase.table("users").select("*").eq("account", acc).execute()

        if data.data:
            st.session_state.user = data.data[0]
            st.success("Login Successful")
        else:
            st.error("Invalid Account Number")

#HOME PAGE
if st.session_state.user:
    user = st.session_state.user
    st.subheader(f"Welcome {user['name']}")

    option = st.selectbox(
        "Choose Option",
        ["Check Balance", "Deposit", "Withdraw"]
    )

    # Check Balance
    if option == "Check Balance":
        st.info(f"Balance: ₹{user['balance']}")

    # Deposit
    if option == "Deposit":
        amt = st.number_input("Enter Amount", min_value=1)
        if st.button("Deposit"):
            new_bal = user["balance"] + amt
            supabase.table("users").update(
                {"balance": new_bal}
            ).eq("account", user["account"]).execute()
            st.session_state.user["balance"] = new_bal
            st.success("Amount Deposited")

    # Withdraw
    if option == "Withdraw":
        amt = st.number_input("Enter Amount", min_value=1)
        if st.button("Withdraw"):
            if amt <= user["balance"]:
                new_bal = user["balance"] - amt
                supabase.table("users").update(
                    {"balance": new_bal}
                ).eq("account", user["account"]).execute()
                st.session_state.user["balance"] = new_bal
                st.success("Amount Withdrawn")
            else:
                st.error("Insufficient Balance")

#REGISTER
if choice == "REGISTER":
    st.subheader("Register User")

    name = st.text_input("Enter Name")
    age = st.number_input("Age", min_value=18)
    account = int(st.number_input("Account Number"))
    bal = st.number_input("Balance", min_value=500)

    if st.button("Save"):
        supabase.table("users").insert({
            "name": name,
            "age": age,
            "account": account,
            "balance": bal
        }).execute()
        st.success("User Added Successfully")

#VIEW
if choice == "VIEW":
    st.subheader("View Users")
    data = supabase.table("users").select("*").execute()
    df = pd.DataFrame(data.data) 
    st.dataframe(df)
