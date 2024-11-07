import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px

# Configuração inicial da página
st.set_page_config(page_title="Gerador de Indicadores", layout="wide")

# Título do projeto
st.title("Gerador de Indicadores")

# Sidebar para o upload do dataset
st.sidebar.header("Upload do Dataset")
uploaded_file = st.sidebar.file_uploader("Envie seu arquivo (CSV ou Excel)", type=['csv', 'xlsx', 'json'])

# Função para separar as colunas por tipo
def categorize_columns(df):
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    obj_cols = df.select_dtypes(include=['object']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    return num_cols, obj_cols, date_cols

# Se o usuário fizer upload do dataset
if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    if file_type == 'csv':
        # Perguntar qual o separador do CSV
        separator = st.sidebar.selectbox(
            "Selecione o separador do arquivo CSV",
            options=[',', ';', '|', '\t'],
            index=0  # Default é o ','
        )
        try:
            df = pd.read_csv(uploaded_file, sep=separator)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo CSV. Erro: {e}")
    
    elif file_type == 'xlsx':
        try:
            df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo Excel. Erro: {e}")
    
    elif file_type == 'json':
        try:
            df = pd.read_json(uploaded_file)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo JSON. Erro: {e}")
    
    else:
        st.warning("Formato de arquivo não suportado. Por favor, envie um arquivo CSV, Excel ou JSON.")
    
    # Exibir uma lista de atributos disponíveis
    if 'df' in locals():
        st.sidebar.header("Atributos do Dataset")
        selected_attributes = st.sidebar.multiselect(
            "Selecione os atributos que deseja visualizar",
            options=list(df.columns),  # Converte para lista
            default=list(df.columns)   # Define o padrão explicitamente como lista
        )

        # Exibir o dataset
        st.write("**Prévia do Dataset:**")
        st.write(df.head())

        # Separando as colunas por tipo
        num_cols, obj_cols, date_cols = categorize_columns(df)

        # Gerar estatísticas para colunas numéricas
        if num_cols:
            st.header("Estatísticas para Colunas Numéricas")
            st.write(df[num_cols].describe())
            
            # Correlação entre as variáveis numéricas
            st.header("Correlação entre Variáveis Numéricas")
            correlation_matrix = df[num_cols].corr()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

        # Gerar contagem para colunas de objeto (string) e nuvem de palavras
        if obj_cols:
            st.header("Informações para Colunas de Texto")
            for col in obj_cols:
                st.subheader(f"Contagem de valores para {col}")
                st.write(df[col].value_counts())
                
                # Gerar nuvem de palavras para a coluna de texto
                st.subheader(f"Nuvem de Palavras para {col}")
                
                # Verificar se há palavras válidas para gerar a nuvem
                text_data = " ".join(df[col].dropna().astype(str))
                if text_data.strip():  # Verifica se há texto não vazio
                    try:
                        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
                        
                        # Exibe a nuvem de palavras
                        plt.figure(figsize=(10, 5))
                        plt.imshow(wordcloud, interpolation='bilinear')
                        plt.axis("off")
                        st.pyplot(plt)
                    except ValueError:
                        st.warning(f"A coluna {col} não contém palavras suficientes para gerar a nuvem.")
                else:
                    st.warning(f"A coluna {col} não possui dados válidos para gerar a nuvem de palavras.")

        # Gerar gráfico de séries temporais para colunas de data
        if date_cols:
            st.header("Séries Temporais para Colunas de Data")
            for col in date_cols:
                st.subheader(f"Série Temporal para {col}")
                # Garantir que a coluna de data seja de tipo datetime
                df[col] = pd.to_datetime(df[col], errors='coerce')
                
                # Agrupar por data e calcular a soma, média ou contagem
                time_series = df.groupby(df[col].dt.date).size()
                
                # Exibe a série temporal com Plotly
                fig = px.line(time_series, x=time_series.index, y=time_series.values, title=f"Série Temporal de {col}")
                st.plotly_chart(fig)

        # Dashboard para cruzamento de variáveis numéricas e de objeto
       # Dashboard para cruzamento de variáveis numéricas e de objeto
        if num_cols and obj_cols:
            st.header("Dashboard de Cruzamento de Variáveis")
            
            # Selecionar a variável numérica
            selected_num = st.selectbox("Selecione a variável numérica", options=num_cols)
            
            # Selecionar a variável de texto
            selected_obj = st.selectbox("Selecione a variável de texto", options=obj_cols)
            
            # Limitar os valores da coluna de objeto para os Top 10 mais frequentes
            top_values = df[selected_obj].value_counts().head(10).index.tolist()
            filtered_df = df[df[selected_obj].isin(top_values)]
            
            # Gerar gráfico de barras com base no cruzamento selecionado
            st.subheader(f"Cruzamento entre {selected_num} e {selected_obj}")
            cross_tab = pd.crosstab(filtered_df[selected_obj], filtered_df[selected_num])
            
            fig, ax = plt.subplots(figsize=(10, 6))
            cross_tab.plot(kind='bar', stacked=False, ax=ax)
            st.pyplot(fig)


else:
    st.write("Por favor, faça o upload de um arquivo para gerar insights.")
