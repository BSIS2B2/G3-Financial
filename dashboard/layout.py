import streamlit as st

def load_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; background-color: #f5f7fa; }
    section[data-testid="stSidebar"] { background-color: #0f172a; }
    section[data-testid="stSidebar"] * { color: white !important; }
    h1, h2, h3 { font-weight: 600; color: #00ff7f; }
    div[data-testid="metric-container"] {
        background-color: white; border-radius: 12px;
        padding: 16px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .stForm {
        background-color: white; padding: 20px;
        border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        padding: 14px;
        margin-bottom: 10px;
        border-radius: 10px;
        background-color: #1e40af;
        color: white;
        font-weight: bold;
        text-align: center;
    }
    .stButton>button:hover { background-color: #2563eb; }
    thead tr th { background-color: #f1f5f9 !important; font-weight: 600; color: #0f172a; }
    tbody tr:hover { background-color: #f8fafc; }
    div[data-testid="stSuccess"], div[data-testid="stInfo"] { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)
