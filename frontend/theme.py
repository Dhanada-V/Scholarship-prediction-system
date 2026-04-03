import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(180deg, #1e3a5f 0%, #0f2a44 100%);
        color: white;
    }

    .stButton>button {
        background-color: #c9a23f;
        color: black;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 20px;
    }

    .stButton>button:hover {
        background-color: #eab308;
        transform: translateY(-2px);
    }

    h1, h2, h3 {
        color: #facc15;
    }
    </style>
    """, unsafe_allow_html=True)