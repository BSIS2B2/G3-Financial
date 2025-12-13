import streamlit as st

class SessionManager:
    @staticmethod
    def initialize():
        if "clients" not in st.session_state:
            st.session_state["clients"] = []
