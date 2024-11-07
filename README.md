
# Gerador de Indicadores

Este projeto cria uma aplicação interativa utilizando o **Streamlit** para gerar insights sobre datasets fornecidos pelo usuário. A aplicação permite que o usuário faça upload de arquivos CSV, Excel ou JSON e, com base nesses dados, a aplicação gera análises estatísticas, gráficos e visualizações, incluindo:

- Estatísticas descritivas para colunas numéricas
- Correlação entre variáveis numéricas
- Contagem de valores para colunas de texto
- Nuvem de palavras para colunas de texto
- Gráficos de séries temporais para colunas de data
- Dashboard de cruzamento de variáveis numéricas e de texto

A aplicação é capaz de separar as colunas do dataset em três tipos: **numéricas**, **texto** (objetos) e **datas**, gerando gráficos e informações com base nesses tipos.

## Dependências

As seguintes bibliotecas Python são utilizadas:

- **Streamlit**: Interface interativa para visualização de dados
- **Pandas**: Manipulação de dados e leitura de arquivos
- **Seaborn**: Visualização de dados estatísticos
- **Matplotlib**: Geração de gráficos
- **WordCloud**: Geração de nuvem de palavras
- **Plotly**: Visualizações interativas de séries temporais

Instalar as dependências:

```bash
pip install streamlit pandas seaborn matplotlib wordcloud plotly
```

## Funcionalidade

1. **Configuração da Página**
   
   A primeira parte do código define as configurações da página da aplicação Streamlit, incluindo o título da página e o layout.

   ```python
   st.set_page_config(page_title="Gerador de Indicadores", layout="wide")
   st.title("Gerador de Indicadores")
   ```

2. **Upload de Dataset**
   
   O usuário pode fazer upload de um arquivo CSV, Excel ou JSON. O código usa o `file_uploader` da biblioteca Streamlit para isso. Dependendo do tipo de arquivo enviado, o código lê o arquivo e o converte em um DataFrame Pandas.

   ```python
   uploaded_file = st.sidebar.file_uploader("Envie seu arquivo (CSV ou Excel)", type=['csv', 'xlsx', 'json'])
   ```

3. **Função `categorize_columns`**
   
   Essa função é responsável por categorizar as colunas do dataset em três tipos:
   - Colunas numéricas
   - Colunas de texto (objetos)
   - Colunas de data

   ```python
   def categorize_columns(df):
       num_cols = df.select_dtypes(include=['number']).columns.tolist()
       obj_cols = df.select_dtypes(include=['object']).columns.tolist()
       date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
       return num_cols, obj_cols, date_cols
   ```

4. **Geração de Estatísticas e Visualizações**
   
   - **Estatísticas para colunas numéricas**: O código gera estatísticas descritivas (como média, desvio padrão, etc.) e um gráfico de correlação entre variáveis numéricas usando o **Seaborn**.

     ```python
     st.header("Estatísticas para Colunas Numéricas")
     st.write(df[num_cols].describe())
     ```

   - **Contagem de valores e Nuvem de Palavras para colunas de texto**: Para colunas de texto, o código exibe a contagem de valores únicos e gera uma nuvem de palavras utilizando a biblioteca **WordCloud**.

     ```python
     text_data = " ".join(df[col].dropna().astype(str))
     wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
     ```

   - **Séries Temporais para colunas de data**: O código gera gráficos interativos de séries temporais utilizando **Plotly**, exibindo dados agrupados por data.

     ```python
     time_series = df.groupby(df[col].dt.date).size()
     fig = px.line(time_series, x=time_series.index, y=time_series.values, title=f"Série Temporal de {col}")
     st.plotly_chart(fig)
     ```

5. **Dashboard para Cruzamento de Variáveis**
   
   O código também permite ao usuário cruzar variáveis numéricas com variáveis de texto, criando gráficos de barras para visualização desses cruzamentos.

   ```python
   cross_tab = pd.crosstab(df[selected_obj], df[selected_num])
   ```

## Estrutura do Código

1. **Upload do Dataset**:
   - O arquivo é lido e convertido para um DataFrame Pandas com base no tipo de arquivo enviado.

2. **Divisão de Colunas por Tipo**:
   - As colunas são categorizadas em numéricas, de texto ou de data para que análises apropriadas sejam realizadas.

3. **Análises**:
   - Estatísticas descritivas para colunas numéricas.
   - Contagem de valores e geração de nuvem de palavras para colunas de texto.
   - Gráficos de séries temporais para colunas de data.
   - Dashboard interativo para cruzamento de variáveis.

4. **Exibição de Resultados**:
   - Os resultados são exibidos interativamente no frontend do Streamlit.

## Como Usar

1. **Fazer upload do arquivo**: O usuário deve selecionar e carregar um arquivo CSV, Excel ou JSON usando a barra lateral.
2. **Selecionar atributos**: Após o upload, o usuário pode escolher quais atributos do dataset deseja visualizar.
3. **Visualizar resultados**: O código irá gerar automaticamente gráficos e análises com base nas colunas do dataset.

## Exemplo de Uso

1. O usuário faz o upload de um arquivo CSV.
2. O sistema exibe um resumo estatístico das colunas numéricas.
3. Para as colunas de texto, o sistema exibe a contagem de valores e uma nuvem de palavras.
4. Para as colunas de data, o sistema gera gráficos de séries temporais.
5. O usuário pode interagir com o dashboard para analisar as correlações entre variáveis.

## Conclusão

Este código proporciona uma interface simples e eficaz para explorar e analisar datasets de forma visual, tornando mais fácil para os usuários obter insights rapidamente sem precisar de habilidades avançadas de programação.
