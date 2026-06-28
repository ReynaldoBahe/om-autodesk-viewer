import streamlit as st

st.set_page_config(page_title="Acesso", page_icon="🔐", layout="centered")

st.title("Acesso ao Sistema")

# CSS integrado para o checkbox nascer grande e ciano ao lado do quadrado
st.markdown(
    """
    <style>
    div[data-testid="stCheckbox"] label p {
        color: #00ffff !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    div[data-testid="stCheckbox"] input[type="checkbox"]:checked + div {
        background-color: #00ffff !important;
        border-color: #00ffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Criação das duas abas na página
aba_login, aba_cadastro = st.tabs(["🔒 Entrar na Conta", "📝 Criar Nova Conta"])

# --- CONTEÚDO DA ABA 1: LOGIN ---
with aba_login:
    with st.form(key="login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário", key="login_user")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha", key="login_pass")
        
        # O checkbox agora já nasce estilizado e alinhado corretamente
        lembrar = st.checkbox("Lembrar de mim")
        
        submit_button = st.form_submit_button(label="Entrar")

    if submit_button:
        if username == "admin" and password == "1234":
            st.success("Login realizado com sucesso!")
        else:
            st.error("Usuário ou senha incorretos.")

# --- CONTEÚDO DA ABA 2: CADASTRO OU OUTRA FUNÇÃO ---
with aba_cadastro:
    st.subheader("Cadastro de Novo Usuário")
    with st.form(key="register_form"):
        novo_usuario = st.text_input("Escolha um Usuário", placeholder="Ex: joao_silva")
        nova_senha = st.text_input("Escolha uma Senha", type="password", placeholder="Mínimo 6 caracteres")
        confirma_senha = st.text_input("Confirme a Senha", type="password", placeholder="Digite novamente")
        
        register_button = st.form_submit_button(label="Cadastrar")
        
    if register_button:
        if nova_senha == confirma_senha and novo_usuario:
            st.success("Cadastro solicitado com sucesso! Aguarde aprovação.")
        elif nova_senha != confirma_senha:
            st.error("As senhas não coincidem.")
        else:
            st.error("Preencha todos os campos.")
