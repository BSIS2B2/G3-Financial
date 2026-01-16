import streamlit as st

class SessionManager:
    @staticmethod
    def initialize():
        if "clients" not in st.session_state:
            st.session_state["clients"] = []
        if "page" not in st.session_state:
            st.session_state["page"] = "home"  # landing page by default
