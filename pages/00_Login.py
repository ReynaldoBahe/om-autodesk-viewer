import streamlit as st

st.set_page_config(page_title="Acesso ao Sistema", page_icon="🔒", layout="wide")

# 1. Inicializa o estado de login na memória global
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cliente_ativo" not in st.session_state:
    st.session_state.cliente_ativo = ""

# 2. Renderização da Interface Limpa
col_central, _ = st.columns([2, 1])

with col_central:
    st.title("Acesso ao Sistema")
    st.write("Insira suas credenciais para acessar o painel de engenharia e O&M.")
    
    # Caixa visual do formulário protegido
    with st.form("meu_formulario_login"):
        usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
        senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        lembrar = st.checkbox("Lembrar de mim")
        
        # Botão estruturado para submissão de formulários
        botao_entrar = st.form_submit_button("Entrar", use_container_width=True)

# 3. Processamento do Clique e validação do acesso
if botao_entrar:
    # Usuários autorizados para testes locais e homologação
    usuarios_validos = {
        "admin": "admin",
        "fiat": "fiat123",
        "ambev": "ambev123"
    }
    
    if usuario in usuarios_validos and senha == usuarios_validos[usuario]:
        # Ativa a ponte de segurança global na sessão do Streamlit
        st.session_state.logged_in = True
        st.session_state.cliente_ativo = usuario.upper()
        
        st.success("Acesso liberado! Use o menu lateral para navegar pelas páginas.")
        st.balloons()
    else:
        st.error("Usuário ou senha incorretos. Verifique suas credenciais.")
