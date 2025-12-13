import streamlit as st
from utils.session import SessionManager
from dashboard.dashboard import Dashboard
from dashboard.layout import load_css

st.set_page_config(page_title="Client Credit Analysis", layout="wide")

# Initialize session
SessionManager.initialize()

# Load CSS
load_css()

# Render dashboard
Dashboard().render()
