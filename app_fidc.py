# app_fidc.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Painel FIDCs", layout="wide", page_icon="💱")

# ======= SIDEBAR =======
st.sidebar.title("📊 Painel de Análise de FIDCs")
pagina = st.sidebar.radio("Navegação", ["Visão de Mercado e Fundos", "Risco e Carteira", "Motor de Recomendação"])
st.sidebar.markdown("---")
st.sidebar.info("Protótipo BI automatizado — dados simulados para teste.")

# ======= BASES SIMULADAS =======
df_fundos = pd.DataFrame({
    "Fundo": ["FIDC Alpha", "FIDC Beta", "FIDC Gama"],
    "Rentabilidade (%)": [12.3, 9.8, 14.1],
    "Risco (%)": [5.1, 3.9, 7.2],
    "PL (R$ MM)": [120, 85, 95],
    "Setor": ["Financeiro", "Varejo", "Imobiliário"]
})

df_boletos = pd.DataFrame({
    "Setor": ["Financeiro", "Varejo", "Imobiliário", "Agro", "Tecnologia"],
    "% Vencidos >30d": [12.5, 9.8, 11.2, 7.3, 5.6],
    "Qtd_Cedentes": [8, 10, 5, 7, 6],
    "Diversificação": [0.72, 0.64, 0.58, 0.67, 0.61]
})

df_recomend = pd.DataFrame({
    "Fundo": ["FIDC Alpha", "FIDC Beta", "FIDC Gama"],
    "Afinidade": [90, 76, 74],
    "Risco": ["Baixo", "Baixo", "Médio"],
    "Retorno": ["Médio", "Alto", "Alto"]
})

# ======= PÁGINA 1 - VISÃO DE MERCADO =======
if pagina == "Visão de Mercado e Fundos":
    st.title("📈 Painel de Mercado e Fundos - FIDCs")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("FIDCs Monitorados", len(df_fundos))
        st.metric("Patrimônio Líquido Total", f"R$ {df_fundos['PL (R$ MM)'].sum():,.0f} mi")
    with col2:
        rent_med = df_fundos["Rentabilidade (%)"].mean()
        risco_med = df_fundos["Risco (%)"].mean()
        st.metric("Rentabilidade Média (%)", f"{rent_med:.2f}")
        st.metric("Risco Médio (%)", f"{risco_med:.2f}")

    st.markdown("### 💱 Rentabilidade x Risco por Fundo")
    fig1 = px.scatter(df_fundos, x="Risco (%)", y="Rentabilidade (%)", size="PL (R$ MM)",
                      color="Fundo", text="Fundo", color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### 💱 FIDCs por Setor Predominante")
    fig2 = px.bar(df_fundos, x="Setor", y="PL (R$ MM)", color="Setor", text="PL (R$ MM)")
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df_fundos, use_container_width=True)

# ======= PÁGINA 2 - RISCO E CARTEIRA =======
elif pagina == "Risco e Carteira":
    st.title("⚠️ Painel de Risco e Qualidade da Carteira")

    col1, col2, col3 = st.columns(3)
    col1.metric("% Boletos Vencidos >30d (Média)", f"{df_boletos['% Vencidos >30d'].mean():.1f}%")
    col2.metric("Diversificação Média", f"{df_boletos['Diversificação'].mean():.2f}")
    col3.metric("Qtd Média de Cedentes", int(df_boletos['Qtd_Cedentes'].mean()))

    st.markdown("### 🔍 Inadimplência por Setor")
    fig3 = px.bar(df_boletos, x="Setor", y="% Vencidos >30d", color="Setor", text="% Vencidos >30d")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 🔍 Concentração de Cedentes")
    fig4 = px.pie(df_boletos, names="Setor", values="Qtd_Cedentes", color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### 🔍 Diversificação (Índice entre 0 e 1)")
    fig5 = px.line(df_boletos, x="Setor", y="Diversificação", markers=True)
    st.plotly_chart(fig5, use_container_width=True)

    st.dataframe(df_boletos, use_container_width=True)

# ======= PÁGINA 3 - MOTOR DE RECOMENDAÇÃO =======
elif pagina == "Motor de Recomendação":
    st.title("🤖 Motor de Recomendação de Fundos")

    st.markdown("### 🔍 Compatibilidade com Perfil do Investidor")
    afinidade_media = np.mean(df_recomend["Afinidade"])
    st.metric("Compatibilidade Média", f"{afinidade_media:.0f}%")

    st.markdown("### 🔍 Top 3 Fundos Recomendados")
    fig6 = px.bar(df_recomend, x="Fundo", y="Afinidade", color="Fundo", text="Afinidade",
                  color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("### 🔍 Detalhes das Recomendações")
    st.dataframe(df_recomend, use_container_width=True)

    st.markdown("---")
    st.info("💡 Fórmula do Score (Afinidade) usada para teste:\n\n"
            "Afinidade = (Rentabilidade * 0.4) + (Diversificação * 0.3) + (1 - Inadimplência) * 0.3")
