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

# 2. SE CONTINUAR VAZIO: Lê direto o arquivo físico do seu repositório
if df_base.empty:
    for nome_arq in ["CMMS_Export_RB - CMMS_RB.csv", "CMMS_Export_RB.csv"]:
        try:
            df_base = pd.read_csv(nome_arq)
            st.session_state['dados_os'] = df_base
            break
        except Exception:
            continue

# 3. VERIFICAÇÃO DE CONTINGÊNCIA (Garante que nunca quebra)
if df_base.empty:
    dados_padrao = [{
        'OS': 'OS-2026-001', 'ID': '29e456...', 'Data_Abertura': '26/06/2026 08:00:00',
        'Data_Fechamento': '', 'Descrição': 'Inicialização padrão.',
        'Status': 'Aberta', 'Setor': 'Climatização', 'Tipo_manutencao': 'Preventiva',
        'Responsavel': 'Pedro', 'Criticidade': 'Alta', 'Sintoma_detalhado': 'Sistema ativo.',
        'Pecas_substituidas': '', 'link_manual_tecnico': '', 'Custo_Material': 0.0,
        'Custo_Mao_Obra': 0.0, 'ID_Sonoff': 'Não Vinculado', 'Tempo_Parado_Horas': 0, 'Causa_Raiz': 'Pendente'
    }]
    df_base = pd.DataFrame(dados_padrao)

if 'dados_os' not in st.session_state or st.session_state['dados_os'].empty:
    st.session_state['dados_os'] = df_base

# Força todas as colunas a aceitarem qualquer tipo de texto para evitar o TypeError
df = st.session_state['dados_os'].astype(object)

for col in ['Pecas_substituidas', 'Causa_Raiz', 'Data_Fechamento']:
    if col not in df.columns:
        df[col] = ""
    df[col] = df[col].fillna("").astype(str)

# --------------------------------------------------------
# CAIXA 1: FORMULÁRIO DE ABERTURA DE NOVA OS
# --------------------------------------------------------
with st.form("formulario_nova_os", clear_on_submit=False):
    st.subheader("➕ Registrar Nova Ordem de Serviço")
    
    col1, col2 = st.columns(2)
    with col1:
        nova_os = st.text_input("Código da OS", value=f"OS-2026-{len(df) + 1:03d}")
        id_bim = st.text_input("ID BIM do Ativo (Speckle)", value="29e456...")
        setor = st.selectbox("Setor Responsável", ["Climatização", "Elétrica", "Hidráulica", "Mecânica", "Civil"])
        tipo_manutencao = st.selectbox("Tipo de Manutenção", ["Corretiva", "Preventiva", "Preditiva"])
        responsavel = st.selectbox("Profissional Técnico", ["Pedro", "Marcos", "Tiago", "Francisco", "Joaquim"])
        
    with col2:
        criticidade = st.selectbox("Grau de Criticidade", ["Alta", "Média", "Baixa"])
        sintoma = st.text_area("Sintoma Detalhado / Descrição do Problema", placeholder="Descreva o comportamento anômalo encontrado...")
        link_manual = st.text_input("Link do Manual Técnico (URL)", value="")
        id_sonoff = st.text_input("ID do Sensor Sonoff Vinculado", value="Não Vinculado")
        
    btn_registrar = st.form_submit_button("💾 Registrar OS no Sistema")
    
    if btn_registrar:
        novo_registro = {
            'OS': nova_os, 'ID': id_bim,
            'Data_Abertura': pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S'),
            'Data_Fechamento': '',
            'Descrição': f"Atendimento nativo criado via portal para setor de {setor}.",
            'Status': 'Aberta', 'Setor': setor, 'Tipo_manutencao': tipo_manutencao,
            'Responsavel': responsavel, 'Criticidade': criticidade,
            'Sintoma_detalhado': sintoma, 'Pecas_substituidas': '',
            'link_manual_tecnico': link_manual, 'Custo_Material': 0.0,
            'Custo_Mao_Obra': 0.0, 'ID_Sonoff': id_sonoff,
            'Tempo_Parado_Horas': 0, 'Causa_Raiz': 'Pendente de Análise'
        }
        
        df_atualizado = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
        st.session_state['dados_os'] = df_atualizado
        st.success(f"✅ {nova_os} registrada com sucesso!")
        st.experimental_rerun()

# --------------------------------------------------------
# CAIXA 2: PAINEL DE ATUALIZAÇÃO RÁPIDA (BAIXA EM OS)
# --------------------------------------------------------
st.markdown("---")
st.subheader("⚡ Atualização Rápida de Status (Operador)")

lista_os = df['OS'].unique()
os_selecionada = st.selectbox("Selecione uma OS para dar baixa ou alterar status:", lista_os)

# 🛠️ SISTEMA DE BUSCA ULTRA SEGURO POR MÁSCARA BOOLEANA
condicao = df['OS'] == os_selecionada

if condicao.any():
    # Extrai os dados atuais como string para evitar falhas de visualização
    status_atual = str(df.loc[condicao, 'Status'].values[0])
    pecas_atuais = df.loc[condicao, 'Pecas_substituidas'].values[0]
    pecas_texto = "" if pd.isna(pecas_atuais) or pecas_atuais == "nan" else str(pecas_atuais)
    
    col_edit1, col_edit2, col_edit3 = st.columns(3)
    with col_edit1:
        status_padrao = ["Aberta", "Em Andamento", "Pausada", "Fechado"]
        idx_status = status_padrao.index(status_atual) if status_atual in status_padrao else 0
        novo_status = st.selectbox("Novo Status", status_padrao, index=idx_status)
    with col_edit2:
        pecas = st.text_input("Peças Substituídas", value=pecas_texto)
    with col_edit3:
        causa = st.selectbox("Causa Raiz", ["Desgaste Natural", "Falha Elétrica", "Erro Operacional", "Falha Mecânica"], index=0)
        
    if st.button("🔄 Atualizar Registro"):
        # 🔥 A CARTADA FINAL: .loc garante a alteração direta e segura sem erros de tipo
        df.loc[condicao, 'Status'] = str(novo_status)
        df.loc[condicao, 'Pecas_substituidas'] = str(pecas)
        df.loc[condicao, 'Causa_Raiz'] = str(causa)
        
        if novo_status == "Fechado":
            df.loc[condicao, 'Data_Fechamento'] = pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')
            
        st.session_state['dados_os'] = df
        st.success(f"📊 Status da {os_selecionada} modificado para '{novo_status}' com sucesso!")
        st.experimental_rerun()

# --------------------------------------------------------
# CAIXA 3: EXPORTAÇÃO DOS DADOS ATUALIZADOS
# --------------------------------------------------------
st.markdown("---")
st.subheader("💾 Exportar Banco de Dados Atualizado")

csv_data = st.session_state['dados_os'].to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar Planilha CMMS Atualizada (.CSV)",
    data=csv_data,
    file_name="CMMS_Export_RB_Atualizado.csv",
    mime="text/csv"
)
