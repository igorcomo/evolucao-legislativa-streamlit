import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Produção Legislativa - Câmara dos Deputados", layout="wide")

st.title("📜 Análise da Produção Legislativa da Câmara dos Deputados")

st.write("""
Aplicação desenvolvida por **Igor Costa**.

Esta aplicação consulta dados reais da **API de Dados Abertos da Câmara dos Deputados**, permitindo analisar a produção legislativa brasileira por ano e tipo de proposição.
""")

anos = list(range(2000, 2025))
ano_escolhido = st.selectbox("Selecione o ano:", anos[::-1])
tipo = st.selectbox("Tipo de proposição:", ["PL", "PEC", "PDL", "MPV"])

url = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes?ano={ano_escolhido}&siglaTipo={tipo}&itens=200"
st.info("Buscando dados em API oficial...")

response = requests.get(url)
data = response.json()

if "dados" not in data or len(data["dados"]) == 0:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
else:
    df = pd.DataFrame(data["dados"])
    df["dataApresentacao"] = pd.to_datetime(df["dataApresentacao"])

    st.subheader(f"📊 Projetos encontrados em {ano_escolhido}: {len(df)} registros")
    st.dataframe(df[["id", "siglaTipo", "numero", "ano", "ementa", "dataApresentacao"]])

    df["mes"] = df["dataApresentacao"].dt.month
    mensal = df.groupby("mes").size().reset_index(name="quantidade")

    fig1 = px.bar(mensal, x="mes", y="quantidade", title="Quantidade de projetos por mês", color="quantidade")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(mensal, x="mes", y="quantidade", title="Evolução mensal")
    st.plotly_chart(fig2, use_container_width=True)

    st.download_button(
        "📥 Baixar base de dados (CSV)",
        df.to_csv(index=False),
        file_name=f"proposicoes_{ano_escolhido}_{tipo}.csv",
        mime="text/csv"
    )
