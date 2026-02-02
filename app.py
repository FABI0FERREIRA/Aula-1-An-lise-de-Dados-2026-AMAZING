import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📈",
    layout="wide",
    
)

st.markdown("""
<style>
.stApp {
    background-color: #DCDCDC;
}
</style>
""", unsafe_allow_html=True)


# --- Carregamento dos dados ---
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

st.markdown("""
<style>
/* Multiselect container */
div[data-baseweb="select"] > div {
    background-color: #0E1117;
    border-color: #00E5FF;
}

/* Selected values */
div[data-baseweb="tag"] {
    background-color: #00E5FF;
    color: black;
}

/* Dropdown list */
ul[role="listbox"] {
    background-color: #0E1117;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]




# --- Conteúdo Principal ---
st.markdown(
    "<h1 style='color:	#1C1C1C;'>📊 Dashboard de Análise de Salários na Área de Dados</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='color:gray;'>Explore os dados salariais na área de dados nos últimos anos. "
    "Utilize os filtros à esquerda para refinar sua análise.</p>",
    unsafe_allow_html=True
)


st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: 	#C0C0C0;
}
</style>
""", unsafe_allow_html=True)




# --- Métricas Principais (KPIs) ---
st.markdown(
    "<h3 style='color:#228B22;'>Métricas gerais (Salário anual em USD)</h3>",
    unsafe_allow_html=True
)
if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""


st.markdown("""
<style>
/* Metric label */
[data-testid="stMetricLabel"] {
    color: #9EFF00;
    font-weight: 600;
}

/* Metric value */
[data-testid="stMetricValue"] {
    color: #FFFFFF;
    font-size: 32px;
}

/* Metric container */
[data-testid="stMetric"] {
    background-color: #161B22;
    padding: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

# --- Análises Visuais com Plotly ---
st.markdown(
    "<h3 style='color:#36B902;'>Gráficos</h3>",
    unsafe_allow_html=True
)

col_graf1, col_graf2 = st.columns(2)


with col_graf1:
    if not df_filtrado.empty:
        top_cargos = (
            df_filtrado.groupby('cargo')['usd']
            .mean()
            .nlargest(10)
            .sort_values(ascending=True)
            .reset_index()
        )

        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''},
            color_discrete_sequence=["#36B902"],  # NEON GREEN
        )

        grafico_cargos.update_layout(
            title=dict(
                text="Distribuição de salários anuais",
                x=0.05,
                font=dict(color="white", size=20)
            ),
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="#E6EDF3"),
            xaxis=dict(
                gridcolor="#1F2937",
                zerolinecolor="#1F2937"
            ),
            yaxis=dict(
                gridcolor="#1F2937"
            )
        )

        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")
with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''},
            color_discrete_sequence=["#36B902"]  # NEON CYAN
        )

        grafico_hist.update_layout(
            title=dict(
                text="Distribuição de salários anuais",
                x=0.05,
                font=dict(color="white", size=20)
            ),
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="#E6EDF3"),
            xaxis=dict(
                gridcolor="#4C596B",
                zerolinecolor="#1F2937"
            ),
            yaxis=dict(
                gridcolor="#1F2937"
            )
        )

        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']

        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            hole=0.5,
            color_discrete_sequence=[
                "#00FF9C",  # neon green
                "#00E5FF",  # neon cyan
                "#B983FF",  # neon purple
                "#FF4DFF"   # neon pink
            ]
        )

        grafico_remoto.update_traces(
            textinfo='percent+label',
            textfont=dict(color="white"),
            marker=dict(line=dict(color="#222222", width=2))
        )

        grafico_remoto.update_layout(
            title=dict(
                text="Proporção dos tipos de trabalho",
                x=0.05,
                font=dict(color="white", size=20)
            ),
            paper_bgcolor="#0E1117",
            plot_bgcolor="#ADADAD",
            font=dict(color="#E6EDF3"),
            showlegend=True
        )

        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()

        grafico_paises = px.choropleth(
            media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale=[
                (0.0, "#1E1E2F"),
                (0.5, "#00E5FF"),
                (1.0, "#00FF9C")
            ],
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'}
        )

        grafico_paises.update_layout(
            title=dict(
                text="Salário médio de Cientista de Dados por país",
                x=0.05,
                font=dict(color="white", size=20)
            ),
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="#E6EDF3"),
            geo=dict(
                bgcolor="#0E1117"
            )
        )

        grafico_paises.update_geos(
            showcountries=True,
            countrycolor="#2A2A2A",
            showcoastlines=False
        )

        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

# --- Tabela de Dados Detalhados ---
st.markdown("""
<style>
[data-testid="stDataFrame"] {
    background-color: #0E1117;
}

[data-testid="stDataFrame"] th {
    background-color: #161B22;
    color: black;
}

[data-testid="stDataFrame"] td {
    color: #E6EDF3;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h3 style='color:#36B902;'>Dados Detalhados</h3>",
    unsafe_allow_html=True
)
st.dataframe(df_filtrado)