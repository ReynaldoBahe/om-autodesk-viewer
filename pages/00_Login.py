import streamlit as st

st.set_page_config(page_title="Acesso", page_icon="🔐", layout="centered")

# Inicializa um banco de dados temporário na memória da sessão
if "usuarios_db" not in st.session_state:
    st.session_state["usuarios_db"] = {"admin": "1234"}  # Usuário padrão

st.title("Acesso ao Sistema")

# Estilização do checkbox ciano
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

aba_login, aba_cadastro = st.tabs(["🔒 Entrar na Conta", "📝 Criar Nova Conta"])

# --- CONTEÚDO DA ABA 1: LOGIN ---
with aba_login:
    with st.form(key="login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu usuário", key="login_user")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha", key="login_pass")
        lembrar = st.checkbox("Lembrar de mim")
        submit_button = st.form_submit_button(label="Entrar")

    if submit_button:
        # Valida contra o banco de dados temporário da sessão
        if username in st.session_state["usuarios_db"] and st.session_state["usuarios_db"][username] == password:
            st.success(f"Login realizado com sucesso! Bem-vindo, {username}.")
        else:
            st.error("Usuário ou senha incorretos.")

# --- CONTEÚDO DA ABA 2: CADASTRO ---
with aba_cadastro:
    st.subheader("Cadastro de Novo Usuário")
    with st.form(key="register_form", clear_on_submit=True):
        novo_usuario = st.text_input("Escolha um Usuário (E-mail)", placeholder="Ex: seu_email@gmail.com")
        nova_senha = st.text_input("Escolha uma Senha", type="password", placeholder="Digite sua senha")
        confirma_senha = st.text_input("Confirme a Senha", type="password", placeholder="Digite novamente")
        register_button = st.form_submit_button(label="Cadastrar")
        
    if register_button:
        if not novo_usuario or not nova_senha:
            st.error("Preencha todos os campos.")
        elif nova_senha != confirma_senha:
            st.error("As senhas não coincidem.")
        elif novo_usuario in st.session_state["usuarios_db"]:
            st.warning("Este usuário já está cadastrado.")
        else:
            # Salva o novo usuário na memória de forma segura
            st.session_state["usuarios_db"][novo_usuario] = nova_senha
            st.success("Conta criada com sucesso! Agora você já pode mudar para a aba 'Entrar na Conta'.")
