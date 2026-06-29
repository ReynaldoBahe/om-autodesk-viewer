import streamlit as st
import time

# 1. Configuração da página (DEVE SER A PRIMEIRA LINHA EXECUTÁVEL)
st.set_page_config(page_title="Acesso ao Sistema", page_icon="🔐", layout="centered")

# 2. Inicializa a variável de controle de login no sistema, se não existir
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

# ==============================================================================
# 🔐 TELA DE LOGIN (Caso o usuário NÃO esteja autenticado)
# ==============================================================================
if not st.session_state["autenticado"]:
    
    # Espaço reservado para a Logomarca (Centralizada)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Quando tiver a imagem, basta substituir o link abaixo pelo arquivo local ou URL
        st.image("https://placeholder.com", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center;'>Acesso ao Sistema</h2>", unsafe_allow_html=True)
    
    # Abas organizadas para a experiência do usuário
    aba_login, aba_cadastro = st.tabs(["🔒 Entrar na Conta", "📝 Criar Nova Conta"])
    
    with aba_login:
        with st.form("formulario_login"):
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            st.checkbox("Lembrar de mim", key="lembrar")
            
            botao_entrar = st.form_submit_button("Entrar", use_container_width=True)
            
            if botao_entrar:
                # Validação temporária (Substitua depois pelas credenciais reais)
                if usuario == "admin" and senha == "1234":
                    st.session_state["autenticado"] = True
                    st.success("Autenticação bem-sucedida! Liberando módulos...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Usuário ou senha incorretos. Tente novamente.")
                    
    with aba_cadastro:
        st.write("Área para cadastro de novos operadores/usuários.")
        # Seu formulário de cadastro pode entrar aqui...

# ==============================================================================
# 🌐 TELA DE BOAS-VINDAS PÓS-LOGIN (Caso o usuário JÁ esteja autenticado)
# ==============================================================================
else:
    st.title("👋 Bem-vindo ao Portal de Gestão de Ativos")
    st.write("Você está conectado com sucesso ao ambiente operacional.")
    st.info("Acesse o **Menu Lateral** à esquerda para navegar e abrir a página de **Telemetria em Tempo Real**.")
    
    # Botão para efetuar o logout
    if st.button("Desconectar Sessão", use_container_width=True):
        st.session_state["autenticado"] = False
        st.rerun()
