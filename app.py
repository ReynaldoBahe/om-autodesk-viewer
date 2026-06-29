import streamlit as st

# 1. Configuração da página (DEVE SER A PRIMEIRA LINHA EXECUTÁVEL)
st.set_page_config(page_title="Acesso ao Sistema", page_icon="🔒", layout="centered")

# 2. Inicializa as variáveis de controle de login globais
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "cliente_ativo" not in st.session_state:
    st.session_state.cliente_ativo = ""

# =========================================================================
# TELA DE LOGIN (Caso o usuário NÃO esteja autenticado)
# =========================================================================
if not st.session_state.logged_in:
    
    # Título centralizado sem emojis problemáticos
    st.markdown("<h2 style='text-align: center;'>Acesso ao Sistema</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Insira suas credenciais para acessar o painel de engenharia e O&M.</p>", unsafe_allow_html=True)
    
    # Formulário estruturado e seguro em caixa
    with st.form("formulario_login"):
        usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
        senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        lembrar = st.checkbox("Lembrar de mim")
        
        # Botão de submissão do formulário
        botao_entrar = st.form_submit_button("Entrar", use_container_width=True)

    # Processamento do clique no botão
    if botao_entrar:
        # Banco de dados temporário para validação
        usuarios_validos = {
            "admin": "admin",
            "fiat": "fiat123",
            "ambev": "ambev123"
        }
        
        if usuario in usuarios_validos and senha == usuarios_validos[usuario]:
            # Ativa a ponte de segurança global na sessão
            st.session_state.logged_in = True
            st.session_state.cliente_ativo = usuario.upper()
            st.rerun() # Recarrega a página para aplicar o acesso liberado
        else:
            st.error("❌ Usuário ou senha incorretos. Verifique suas credenciais.")

# =========================================================================
# TELA DE SUCESSO (Caso o usuário JÁ ESTEJA autenticado)
# =========================================================================
else:
    st.success(f"✅ Login realizado com sucesso como {st.session_state.cliente_ativo}!")
    st.markdown("### 🚀 O portal está liberado!")
    st.write("Utilize o menu lateral esquerdo para navegar pelas páginas **Home** ou **Telemetria em Tempo Real**.")
    st.balloons()
    
    if st.button("Sair da Conta"):
        st.session_state.logged_in = False
        st.rerun()
