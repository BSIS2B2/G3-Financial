import streamlit as st
import pandas as pd

st.set_page_config(page_title="Client Credit Analysis", layout="wide")

# --- Add a financial image/logo in the upper-left ---
st.image("C:/Users/MRI-USER/OneDrive/Desktop/Pic.jpg", width=120)

st.title("Manual Client Credit Dashboard")
st.write("Enter client data manually and calculate scores, eligibility, and risk levels.")

# Sidebar: Dashboard selection with emojis inside a container
# Sidebar with emojis
with st.sidebar.container():
    st.markdown("## 📊 Dashboard Sections")
    
    options = {
        "Key Metrics": "📈 Key Metrics",
        "Eligibility Breakdown": "✅ Eligibility Breakdown",
        "Risk Level Distribution": "⚠️ Risk Level Distribution",
        "Score Distribution": "📉 Score Distribution",
        "Client Table": "🗂️ Client Table"
    }

    selected_label = st.radio("Select Dashboard", list(options.values()))
    
    # Convert back to internal key
    dashboard_option = [k for k, v in options.items() if v == selected_label][0]


# Session state for storing clients
if 'clients' not in st.session_state:
    st.session_state['clients'] = []

# Input form inside a container
with st.container():
    with st.form("add_client_form"):
        st.subheader("Add New Client")
        client_id = len(st.session_state['clients']) + 1
        income = st.number_input("Income (₱)", min_value=0, value=50000, step=1000)
        debts = st.number_input("Debts (₱)", min_value=0, value=10000, step=1000)
        payment_percent = st.slider("Payment History % (0-100)", 0, 100, 100)
        
        # Emoji submit button
        submitted = st.form_submit_button("💰 Add Client")
        
        if submitted:
            # Calculate Score
            score = (income / (debts + 1)) * 0.6 + (payment_percent/100) * 0.4
            eligibility = "Approved" if score >= 2.0 else "Declined"
            risk_level = "Low" if score >= 2.5 else ("Medium" if score >= 1.5 else "High")
            
            # Save to session
            st.session_state['clients'].append({
                "Client ID": client_id,
                "Income ($)": income,
                "Debts ($)": debts,
                "Payment %": payment_percent,
                "Score": round(score,2),
                "Eligibility": eligibility,
                "Risk Level": risk_level
            })
            st.success(f"Client {client_id} added successfully!")

# Load dataframe
df = pd.DataFrame(st.session_state['clients'])

# Display selected dashboard
if not df.empty:
    if dashboard_option == "Key Metrics":
        st.subheader("Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg Income", f"${int(df['Income ($)'].mean()):,}")
        col2.metric("Avg Debts", f"${int(df['Debts ($)'].mean()):,}")
        col3.metric("Approval Rate", f"{round((df['Eligibility']=='Approved').mean()*100,1)}%")
        col4.metric("High-Risk Clients", f"{len(df[df['Risk Level']=='High'])}")

    elif dashboard_option == "Eligibility Breakdown":
        st.subheader("Eligibility Breakdown")
        st.bar_chart(df['Eligibility'].value_counts())

    elif dashboard_option == "Risk Level Distribution":
        st.subheader("Risk Level Distribution")
        st.bar_chart(df['Risk Level'].value_counts())

    elif dashboard_option == "Score Distribution":
        st.subheader("Score Distribution")
        st.line_chart(df['Score'])

    elif dashboard_option == "Client Table":
        st.subheader("Client Table")
        st.dataframe(df)
else:
    st.info("Add clients manually using the form above.")
