import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="Credit Eligibility Dashboard", layout="wide")
st.title("Credit Eligibility Dashboard")
st.write("Analyze 20–50 clients using data structures, algorithms, and visual analytics.")

# Generate Clients
def generate_clients(n=30):
    clients = []
    for i in range(1, n+1):
        income = random.randint(30000, 100000)
        debts = random.randint(5000, 50000)
        payment_history = [1 if random.random() > 0.25 else 0 for _ in range(12)]
        payment_percent = sum(payment_history)/12
        score = 0.5 * (income/debts) + 0.5 * payment_percent
        eligibility = "Eligible" if score >= 1.0 else "Not Eligible"
        clients.append({
            "ID": i,
            "Income": income,
            "Debts": debts,
            "Payment %": round(payment_percent*100,1),
            "Score": round(score,2),
            "Eligibility": eligibility
        })
    return clients

num_clients = st.slider("Select number of clients:", 20, 50, 30)
if st.button("Generate Clients & Analyze"):
    clients = generate_clients(num_clients)
    df = pd.DataFrame(clients)

    # KPI metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Income", f"${int(df['Income'].mean()):,}")
    col2.metric("Average Debts", f"${int(df['Debts'].mean()):,}")
    col3.metric("Eligibility Rate", f"{round((df['Eligibility']=='Eligible').mean()*100,1)}%")

    # Display charts
    st.subheader("Eligibility Distribution")
    eligibility_counts = df['Eligibility'].value_counts()
    st.bar_chart(eligibility_counts)

    st.subheader("Client Scores")
    st.line_chart(df['Score'])

    # Display table
    st.subheader("Client Data Table")
    st.dataframe(df)