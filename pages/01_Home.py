import streamlit as st

# --- ESTILIZAÇÃO CSS CUSTOMIZADA ORIGINAL ---
st.markdown("""
    <style>
        .main-title { font-size: 32px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
        .sub-title { font-size: 16px; color: #4B5563; margin-bottom: 25px; }
        .card-home { background-color: #F3F4F6; padding: 25px; border-radius: 8px; border: 1px solid #E5E7EB; min-height: 18px; }
        .card-home-title { font-size: 20px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- CONTEÚDO DA PÁGINA INICIAL ---
st.markdown('<div class="main-title">🏗️ Portal de Engenharia & Gestão de Ativos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Bem-vindo ao centro operacional de O&M.</div>', unsafe_allow_html=True)

# Mensagem informativa ou os cartões de navegação que você tinha no app.py
st.info("👋 Use o menu lateral esquerdo para navegar de forma segura entre os módulos técnicos e gerenciar seus ativos.")
