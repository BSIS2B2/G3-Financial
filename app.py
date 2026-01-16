import streamlit as st
from utils.session import SessionManager
from dashboard.dashboard import Dashboard
from dashboard.layout import load_css

st.set_page_config(
    page_title="Bankush Finance",
    layout="wide",
    initial_sidebar_state="collapsed"
)

SessionManager.initialize()
load_css()

if st.session_state.get("page", "home") == "home":

    st.markdown("""<style>
    header[data-testid="stHeader"], footer { display: none; }
    html, body, .stApp { width: 100%; margin: 0; padding: 0; overflow: hidden; height: 100vh; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 40px;
        background: white;
        width: 100%;
        position: fixed;
        top: 0;
        z-index: 10;
    }

    .hero {
        position: fixed;
        inset: 0;
        background-image: url("https://images.unsplash.com/photo-1521791136064-7986c2920216");
        background-size: cover;
        background-position: center;
        z-index: 1;
    }

    .hero::before {
        content: "";
        position: absolute;
        inset: 0;
        background: rgba(6, 95, 70, 0.85);
    }

    .hero-content {
        position: relative;
        z-index: 2;
        color: white;
        padding: 120px 80px;
        max-width: 700px;
        margin-top: 70px;
    }

    /* ✅ BUTTON POSITIONED INSIDE HERO */
    .hero-button {
        position: absolute;
        top: 360px;
        left: 80px;
        z-index: 3;
    }

    .footer {
    background: #020617;
    color: #cbd5e1;
    padding: 15px 40px;              /* 🔽 reduce height */
    display: flex;
    align-items: center;            /* vertical centering */
    justify-content: space-between; /* ⬅ left & right */
    font-size: 15px;
    position: fixed;
    bottom: 0;
    width: 100%;
    box-sizing: border-box;
    z-index: 10;
}

    div.stButton > button[key="get_started"] {
        background-color: #00ff00 !important;
        color: white;
        font-size: 16px;
        padding: 16px 28px;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }
                div.stButton {
    position: fixed;
    top: 320px;        /* aligns under hero text */
    left: 80px;        /* matches hero padding */
    z-index: 5;
}
                
    .hero-overlay-button {
    position: fixed;
    top: 420px;      /* aligns with hero text */
    left: 80px;
    z-index: 9999;   /* ABOVE hero */
}
                div.stButton {
    position: relative;
    z-index: 5;
}

    div.stButton > button[key="get_started"]:hover {
        background-color: white;
        color: #00ff7f;
    }
    </style>""", unsafe_allow_html=True)

    # NAVBAR
    st.markdown("""<div class="navbar">
        <div class="nav-left">Bankush Finance</div>
        <div class="nav-right">
            <a href="#">Home</a>
            <a href="#">About</a>
            <a href="#">Team</a>
        </div>
    </div>""", unsafe_allow_html=True)

    # HERO
    st.markdown("""<div class="hero">
    <div class="hero-content">
        <h1>We help push people<br>forward financially</h1>
        <p>Smart lending and easy financing</p>
    </div>
</div>""", unsafe_allow_html=True)

    # ✅ BUTTON OVERLAY (INSIDE HERO)
    st.markdown('<div class="hero-overlay-button">', unsafe_allow_html=True)
    if st.button("Get Started →", key="get_started"):
        st.session_state["page"] = "dashboard"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # FOOTER
    st.markdown("""<div class="footer">
        <div>© 2025 Bankush Finance. All rights reserved.</div>
        <div>Contact Us</div>
    </div>""", unsafe_allow_html=True)

elif st.session_state.get("page") == "dashboard":
    if "clients" not in st.session_state:
        st.session_state["clients"] = []
    
    # Configure Sidebar for Dashboard
    st.sidebar.title("Bankush Finance")
    
    # NEW: Add New Borrower Reset Button
    if st.sidebar.button("➕ New Evaluation", use_container_width=True):
        st.session_state.form_submitted = False
        st.session_state.just_added = False
        st.session_state.selected_dashboard = "Borrower Overview"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Navigation Buttons - form_submitted set to True, and just_added to False to allow viewing data
    if st.sidebar.button("Borrower Overview", use_container_width=True):
        st.session_state.form_submitted = True
        st.session_state.just_added = False
        st.session_state.selected_dashboard = "Borrower Overview"
    
    if st.sidebar.button("Debts Overview", use_container_width=True):
        st.session_state.form_submitted = True
        st.session_state.just_added = False
        st.session_state.selected_dashboard = "Debts Overview"
        
    if st.sidebar.button("Borrower's List", use_container_width=True):
        st.session_state.form_submitted = True
        st.session_state.just_added = False
        st.session_state.selected_dashboard = "Borrower's List"
        
    if st.sidebar.button("Loan Summary", use_container_width=True):
        st.session_state.form_submitted = True
        st.session_state.just_added = False
        st.session_state.selected_dashboard = "Loan Summary"

    if st.sidebar.button("Recommendations", use_container_width=True):
        st.session_state.form_submitted = True
        st.session_state.just_added = False
        st.session_state.selected_dashboard = "Recommendations"

    Dashboard().render()