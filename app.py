# ===================================================
# DASHBOARD INTERATIVO: AURA_DATA (app.py)
# ===================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------

st.set_page_config(
    page_title="Aura_Data - Cidade Alfa",
    layout="wide"
)

st.title("🌱 Aura_Data: Monitoramento da Qualidade do Ar")
st.subheader("Dashboard de Análise e Correlação entre Temperatura e Poluentes")

# ---------------------------------------------------
# LEITURA DOS DADOS
# ---------------------------------------------------

# Lê a aba 'Dados' do arquivo Excel ajustado
df = pd.read_excel("cidade_alfa_qualidade_ar_ajustado.xlsx", sheet_name='Dados')

# ---------------------------------------------------
# FILTRO DE REGIÃO
# ---------------------------------------------------

regioes = ['Todas'] + sorted(df['regiao'].dropna().unique())

regiao_selecionada = st.sidebar.selectbox(
    "Selecione uma Região",
    regioes
)

if regiao_selecionada != 'Todas':
    df = df[df['regiao'] == regiao_selecionada]

# ---------------------------------------------------
# CÁLCULO DA CORRELAÇÃO
# ---------------------------------------------------

correlacao = df['pm25_ug_m3'].corr(df['temperatura_c'])

# ---------------------------------------------------
# KPI (MÉTRICA)
# ---------------------------------------------------

st.metric(
    label="Coeficiente de Correlação (Temperatura x PM2.5)",
    value=round(correlacao, 4)
)

# ---------------------------------------------------
# SCATTER PLOT
# ---------------------------------------------------

st.subheader("Temperatura (°C) x Concentração de PM2.5 (µg/m³)")

fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(
    df['temperatura_c'],
    df['pm25_ug_m3'],
    color='teal',
    alpha=0.6
)

ax.set_xlabel("Temperatura (°C)")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_title("Correlação entre Temperatura e Material Particulado Fino")

st.pyplot(fig)

# ---------------------------------------------------
# INTERPRETAÇÃO
# ---------------------------------------------------

st.subheader("Análise do Resultado")

if abs(correlacao) < 0.3:
    interpretacao = """
    Correlação fraca. 
    As variáveis apresentam pouca relação linear entre si na região selecionada.
    """
elif abs(correlacao) < 0.7:
    interpretacao = """
    Correlação moderada. 
    Existe uma relação perceptível entre a temperatura e a concentração de poluentes.
    """
else:
    interpretacao = """
    Correlação forte. 
    As variáveis apresentam comportamento fortemente relacionado.
    """

st.write(interpretacao)

# ---------------------------------------------------
# ESTATÍSTICAS BÁSICAS
# ---------------------------------------------------

st.subheader("Estatísticas Descritivas")

st.dataframe(
    df[['pm25_ug_m3', 'temperatura_c']]
    .describe()
)

# ---------------------------------------------------
# TOTAL DE REGISTROS
# ---------------------------------------------------

st.write(f"Total de registros analisados: {len(df)}")

app.py
