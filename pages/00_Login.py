import streamlit as st

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

st.title("Acesso ao Sistema")

with st.form(key="login_form"):
    username = st.text_input("Usuário", placeholder="Digite seu usuário")
    password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
    
    st.markdown(
        """
        <style>
        .grande-ciano {
            font-size: 20px !important;
            color: #00ffff !important;
            font-weight: bold;
        }
        </style>
        <span class="grande-ciano">Lembrar de mim</span>
        """, 
        unsafe_allow_html=True
    )
    
    lembrar = st.checkbox("Ativar a opção acima", label_visibility="collapsed")
    submit_button = st.form_submit_button(label="Entrar")

if submit_button:
    if username == "admin" and password == "1234":
        st.success("Login realizado com sucesso!")
    else:
        st.error("Usuário ou senha incorretos.")
