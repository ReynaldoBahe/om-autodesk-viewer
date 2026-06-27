import streamlit as st
import pandas as pd

# Configuração padrão da página para manter a identidade visual da RB Consultoria
st.set_page_config(layout="wide", page_title="CMMS Nativo - RB Consultoria")

st.markdown('### 🛠️ CMMS Proprietário — Gestão de Ordens de Serviço')
st.write("Abra e controle ordens de serviço de forma nativa e integrada ao ecossistema.")

# 🔗 CONEXÃO COM O BANCO DE DADOS EM MEMÓRIA OU ARQUIVO LOCAL
df_base = pd.DataFrame()

# 1. Tenta buscar das variáveis de sessão conhecidas
for chave in ['dados_os', 'df_filtrado', 'df', 'df_os']:
    if chave in st.session_state and isinstance(st.session_state[chave], pd.DataFrame):
        if not st.session_state[chave].empty:
            df_base = st.session_state[chave]
            break

# 2. SE CONTINUAR VAZIO: Lê direto o arquivo físico do seu repositório para nunca quebrar
if df_base.empty:
    for nome_arq in ["CMMS_Export_RB - CMMS_RB.csv", "CMMS_Export_RB.csv"]:
        try:
            df_base = pd.read_csv(nome_arq)
            st.session_state['dados_os'] = df_base
            break
        except Exception:
            continue

# 3. VERIFICAÇÃO FINAL DE SEGURANÇA
if df_base.empty:
    st.warning("⚠️ Certifique-se de que o arquivo de dados está na raiz do seu repositório GitHub para liberar o CMMS Nativo.")
else:
    df = df_base.copy()

    # 🛠️ FUNÇÕES DE CALLBACK (RODAM ANTES DA TELA LIMPAR)
    def salvar_nova_os():
        # Captura os dados diretamente usando as chaves dos widgets
        novo_registro = {
            'OS': st.session_state.get('k_os', f"OS-2026-{len(df) + 1:03d}"),
            'ID': st.session_state.get('k_id', '29e456...'),
            'Data_Abertura': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S'),
            'Data_Fechamento': '',
            'Descrição': f"Atendimento nativo criado via portal para setor de {st.session_state.get('k_setor', 'Climatização')}.",
            'Status': 'Aberta',
            'Setor': st.session_state.get('k_setor', 'Climatização'),
            'Tipo_manutencao': st.session_state.get('k_tipo', 'Corretiva'),
            'Responsavel': st.session_state.get('k_resp', 'Pedro'),
            'Criticidade': st.session_state.get('k_crit', 'Alta'),
            'Sintoma_detalhado': st.session_state.get('k_sintoma', ''),
            'Pecas_substituidas': '',
            'link_manual_tecnico': st.session_state.get('k_manual', ''),
            'Custo_Material': 0.0,
            'Custo_Mao_Obra': 0.0,
            'ID_Sonoff': st.session_state.get('k_sonoff', 'Não Vinculado'),
            'Tempo_Parado_Horas': 0,
            'Causa_Raiz': 'Pendente de Análise'
        }
        
        # Concatena e atualiza a memória mestre global
        df_novo = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
        st.session_state['dados_os'] = df_novo
        st.toast(f"✅ {st.session_state.get('k_os')} registrada com sucesso!")

    def atualizar_status_os():
        os_sel = st.session_state.get('k_os_sel')
        if 'dados_os' in st.session_state:
            df_mestre = st.session_state['dados_os']
            idx = df_mestre[df_mestre['OS'] == os_sel].index
            
            df_mestre.at[idx, 'Status'] = st.session_state.get('k_novo_status')
            df_mestre.at[idx, 'Pecas_substituidas'] = st.session_state.get('k_pecas')
            df_mestre.at[idx, 'Causa_Raiz'] = st.session_state.get('k_causa')
            
            if st.session_state.get('k_novo_status') == "Fechado":
                df_mestre.at[idx, 'Data_Fechamento'] = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')
                
            st.session_state['dados_os'] = df_mestre
            st.toast(f"📊 Status da {os_sel} atualizado!")

    # --------------------------------------------------------
    # FORMULÁRIO DE ABERTURA DE NOVA OS
    # --------------------------------------------------------
    with st.form("formulario_nova_os", clear_on_submit=True):
        st.subheader("➕ Registrar Nova Ordem de Serviço")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Código da OS", value=f"OS-2026-{len(df) + 1:03d}", key='k_os')
            st.text_input("ID BIM do Ativo (Speckle)", value="29e456...", key='k_id')
            st.selectbox("Setor Responsável", ["Climatização", "Elétrica", "Hidráulica", "Mecânica", "Civil"], key='k_setor')
            st.selectbox("Tipo de Manutenção", ["Corretiva", "Preventiva", "Preditiva"], key='k_tipo')
            st.selectbox("Profissional Técnico", ["Pedro", "Marcos", "Tiago", "Francisco", "Joaquim"], key='k_resp')
            
        with col2:
            st.selectbox("Grau de Criticidade", ["Alta", "Média", "Baixa"], key='k_crit')
            st.text_area("Sintoma Detalhado / Descrição do Problema", placeholder="Descreva o comportamento...", key='k_sintoma')
            st.text_input("Link do Manual Técnico (URL)", value="", key='k_manual')
            st.text_input("ID do Sensor Sonoff Vinculado", value="Não Vinculado", key='k_sonoff')
            
        # Conecta a função de callback diretamente ao botão de envio
        st.form_submit_button("💾 Registrar OS no Sistema", on_click=salvar_nova_os)

    # --------------------------------------------------------
    # PAINEL DE ATUALIZAÇÃO RÁPIDA (BAIXA EM OS)
    # --------------------------------------------------------
    st.markdown("---")
    st.subheader("⚡ Atualização Rápida de Status (Operador)")
    
    os_selecionada = st.selectbox("Selecione uma OS para dar baixa ou alterar status:", df['OS'].unique(), key='k_os_sel')
    linha_os = df[df['OS'] == os_selecionada]
    
    if not linha_os.empty:
        dados_os_sel = linha_os.iloc[0]
        
        col_edit1, col_edit2, col_edit3 = st.columns(3)
        with col_edit1:
            status_padrao = ["Aberta", "Em Andamento", "Pausada", "Fechado"]
            status_atual = dados_os_sel.get('Status', 'Aberta')
            idx_status = status_padrao.index(status_atual) if status_atual in status_padrao else 0
            st.selectbox("Novo Status", status_padrao, index=idx_status, key='k_novo_status')
        with col_edit2:
            pecas_atuais = dados_os_sel.get('Pecas_substituidas', '')
            st.text_input("Peças Substituídas", value="" if pd.isna(pecas_atuais) else str(pecas_atuais), key='k_pecas')
        with col_edit3:
            st.selectbox("Causa Raiz", ["Desgaste Natural", "Falha Elétrica", "Erro Operacional", "Falha Mecânica"], index=0, key='k_causa')
            
        st.button("🔄 Atualizar Registro", on_click=atualizar_status_os)

    # --------------------------------------------------------
    # RECURSO ADICIONAL: EXPORTAÇÃO DOS DADOS ATUALIZADOS
    # --------------------------------------------------------
    st.markdown("---")
    st.subheader("💾 Exportar Banco de Dados Atualizado")
    
    if 'dados_os' in st.session_state:
        csv_data = st.session_state['dados_os'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Planilha CMMS Atualizada (.CSV)",
            data=csv_data,
            file_name="CMMS_Export_RB_Atualizado.csv",
            mime="text/csv"
        )
