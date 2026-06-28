import streamlit as st
import time

# --- CONTROLADORES DE FLUXO INTERNO ---
if "login_step" not in st.session_state:
    st.session_state.login_step = 1

# --- CREDENCIAIS TEMPORÁRIAS PARA VALIDAÇÃO ---
USER_CORRETO = "engenharia@empresa.com"
SENHA_CORRETA = "senha123"
CODIGO_2FA_CORRETO = "123456"

# Centraliza o container do formulário na tela
st.markdown("<br><br>", unsafe_allow_html=True)

with st.container(border=True):
    # --- ETAPA 1: USUÁRIO E SENHA ---
    if st.session_state.login_step == 1:
        st.markdown("<h2 style='text-align: center;'>Portal de Engenharia</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Autenticação Obrigatória</p>", unsafe_allow_html=True)
        
        with st.form("form_etapa_1"):
            email = st.text_input("E-mail corporativo", placeholder="exemplo@empresa.com")
            senha = st.text_input("Senha", type="password", placeholder="••••••••")
            
            if st.form_submit_button("Avançar", use_container_width=True):
                if email == USER_CORRETO and senha == SENHA_CORRETA:
                    st.session_state.login_step = 2
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos.")

    # --- ETAPA 2: CÓDIGO DE VERIFICAÇÃO (2FA) ---
    elif st.session_state.login_step == 2:
        st.markdown("<h3 style='text-align: center;'>Segurança em Duas Etapas</h3>", unsafe_allow_html=True)
        st.info("Digite o código de verificação temporário de 6 dígitos.")
        
        with st.form("form_etapa_2"):
            codigo = st.text_input("Código de 6 dígitos", max_chars=6, placeholder="000000")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Voltar", use_container_width=True):
                    st.session_state.login_step = 1
                    st.rerun()
            with col2:
                if st.form_submit_button("Confirmar Login", use_container_width=True):
                    if codigo == CODIGO_2FA_CORRETO:
                        st.success("Acesso autorizado com sucesso!")
                        time.sleep(0.5)
                        # Libera a chave global que o app.py monitora para abrir o portal
                        st.session_state.logged_in = True
                        st.session_state.login_step = 1  # Reseta para o próximo logout
                        st.rerun()
                    else:
                        st.error("Código incorreto.")
