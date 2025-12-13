import streamlit as st
import pandas as pd
from models.client import Client
from streamlit_lottie import st_lottie
import requests

class Dashboard:
    def render(self):
        st.title("Manual Client Credit Dashboard")

        # --- Lottie animation ---
        lottie_ani = self.load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")
        if lottie_ani:
            st_lottie(lottie_ani, speed=1, height=150)

        # --- Sidebar as single clickable boxes ---
        st.sidebar.markdown("## Dashboard Sections")
        sections = [
            "Key Metrics",
            "Eligibility Breakdown",
            "Risk Level Distribution",
            "Score Distribution",
            "Client Table"
        ]

        if "selected_dashboard" not in st.session_state:
            st.session_state["selected_dashboard"] = sections[0]

        # Display clickable boxes
        for sec in sections:
            selected = st.session_state["selected_dashboard"] == sec
            color = "#2563eb" if selected else "#1e40af"
            if st.sidebar.button(sec, key=sec):
                st.session_state["selected_dashboard"] = sec
            # Apply CSS for button color
            st.markdown(f"""
                <style>
                div.stButton > button[key="{sec}"] {{
                    background-color: {color};
                    color: white;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 14px;
                    margin-bottom: 10px;
                }}
                div.stButton > button[key="{sec}"]:hover {{
                    background-color: #2563eb;
                }}
                </style>
            """, unsafe_allow_html=True)

        option = st.session_state["selected_dashboard"]

        # --- Add client form ---
        with st.container():
            with st.form("client_form"):
                st.subheader("Add New Client")
                income = st.number_input("Income ($)", 0, 50000, 1000)
                debts = st.number_input("Debts ($)", 0, 10000, 1000)
                payment = st.slider("Payment History %", 0, 100, 100)

                if st.form_submit_button("Add Client"):
                    client_id = len(st.session_state["clients"]) + 1
                    client = Client(client_id, income, debts, payment)
                    st.session_state["clients"].append(client.to_dict())
                    st.success("Client added successfully!")

        if not st.session_state["clients"]:
            st.info("Add clients using the form above.")
            return

        df = pd.DataFrame(st.session_state["clients"])

        # --- Display selected dashboard ---
        if option == "Key Metrics":
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Avg Income", f"${int(df['Income ($)'].mean()):,}")
            col2.metric("Avg Debts", f"${int(df['Debts ($)'].mean()):,}")
            col3.metric("Approval Rate", f"{(df['Eligibility']=='Approved').mean()*100:.1f}%")
            col4.metric("High Risk Clients", len(df[df["Risk Level"] == "High"]))

        elif option == "Eligibility Breakdown":
            st.subheader("Eligibility Breakdown")
            st.bar_chart(df["Eligibility"].value_counts())

        elif option == "Risk Level Distribution":
            st.subheader("Risk Level Distribution")
            st.bar_chart(df["Risk Level"].value_counts())

        elif option == "Score Distribution":
            st.subheader("Score Distribution")
            st.line_chart(df["Score"])

        elif option == "Client Table":
            st.subheader("Client Table")

            def highlight_eligibility(val):
                if val == "Approved":
                    return "background-color: #d4edda; color: #155724; font-weight: bold"
                elif val == "Declined":
                    return "background-color: #f8d7da; color: #721c24; font-weight: bold"
                return ""

            styled_df = df.style.applymap(highlight_eligibility, subset=["Eligibility"])
            st.dataframe(styled_df, use_container_width=True)

            # Delete client
            st.subheader("Delete Client")
            client_ids = df["Client ID"].tolist()
            delete_id = st.selectbox("Select Client ID to delete", client_ids)
            if st.button("Delete Client"):
                st.session_state["clients"] = [
                    c for c in st.session_state["clients"] if c["Client ID"] != delete_id
                ]
                st.success(f"Client {delete_id} deleted.")
                st.rerun()

    @staticmethod
    def load_lottie_url(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
