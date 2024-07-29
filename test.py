import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Função para processar novos dados
def process_new_data(new_data):
    df_col = new_data[['From', 'Connect time', 'Charged time, hour:min:sec']]
    
    valores_para_filtrar = ['3231420315', '3231420314', '3231420319', '1006 (3231420314 - Camila)',  
                            '1008 (3231420315 - Victoria)', '3231420316', '3231420312', 
                            '3231420310', '3231420313', '1002 (3231420312 - Vanessa)', 
                            '1012 (3231420310 - Leo)', '3231420317', 
                            '1015 (3231420319 - Gabriel)', '1004 (3231420313 - Joao Pedro)', 
                            '1010 (3231420316 - Mateus)', '1014 (3231420317 - Joao Vitor)']

    df_col = df_col.loc[df_col['From'].isin(valores_para_filtrar)]

    substituicoes = {
        3231420314: '1006 (3231420314 - Camila)',
        3231420315: '1008 (3231420315 - Victoria)',
        3231420312: '1002 (3231420312 - Vanessa)',
        3231420313: '1004 (3231420313 - Joao Pedro)',
        3231420316: '1010 (3231420316 - Mateus)',
        3231420317: '1014 (3231420317 - Joao Vitor)',
        3231420319: '1015 (3231420319 - Gabriel)',
        3231420310: '1012 (3231420310 - Leo)'
    }

    df_col['From'] = df_col['From'].astype(str)
    df_col['From'] = df_col['From'].replace(substituicoes)

    def substituir_valores(val):
        if val.isdigit():
            return substituicoes.get(int(val), val)
        return val

    df_col['From'] = df_col['From'].apply(substituir_valores)

    df_col['Connect time'] = pd.to_datetime(df_col['Connect time'], format='%d-%m-%y %H:%M:%S')
    df_col['Charged time, hour:min:sec'] = pd.to_timedelta(df_col['Charged time, hour:min:sec'])

    return df_col

# Inicializando o Streamlit
st.set_page_config(page_title='Central Wealth', layout="centered")
st.title('Visão SDRs')

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data = process_new_data(data)

    # Opções de filtros
    sdrs = [
        '1008 (3231420315 - Victoria)', '1014 (3231420317 - Joao Vitor)',
        '1012 (3231420310 - Leo)', '1002 (3231420312 - Vanessa)',
        '1006 (3231420314 - Camila)', '1015 (3231420319 - Gabriel)',
        '1004 (3231420313 - Joao Pedro)', '1010 (3231420316 - Mateus)'
    ]
    selected_sdr = st.selectbox("Escolha um SDR", ["Visão Geral"] + sdrs)
    
    # Seletor de intervalo de datas
    start_date, end_date = st.date_input("Escolha o período de tempo", [datetime.now() - timedelta(days=7), datetime.now()])
    
    # Filtro de duração da chamada
    duration_options = ["Zero", "Menos de 1 min", "Mais de 1 min", "Mais de 2 min"]
    selected_durations = st.multiselect("Escolha a duração das chamadas", duration_options)

    # Filtragem de dados por SDR e datas
    filtered_data = data[(data['Connect time'] >= pd.Timestamp(start_date)) & (data['Connect time'] <= pd.Timestamp(end_date))]
    if selected_sdr != "Visão Geral":
        filtered_data = filtered_data[filtered_data['From'] == selected_sdr]

    # Filtragem de dados por duração das chamadas
    if selected_durations:
        duration_filters = []
        if "Zero" in selected_durations:
            duration_filters.append(filtered_data['Charged time, hour:min:sec'] == timedelta(seconds=0))
        if "Menos de 1 min" in selected_durations:
            duration_filters.append(filtered_data['Charged time, hour:min:sec'] <= timedelta(minutes=1))
        if "Mais de 1 min" in selected_durations:
            duration_filters.append(filtered_data['Charged time, hour:min:sec'] >= timedelta(minutes=1))
        if "Mais de 2 min" in selected_durations:
            duration_filters.append(filtered_data['Charged time, hour:min:sec'] >= timedelta(minutes=2))
        filtered_data = filtered_data[pd.concat(duration_filters, axis=1).any(axis=1)]

    # Visualização dos dados
    with st.expander("Tabela de Ligações"):
        st.write(filtered_data)

    # Histograma de horário das ligações
    with st.expander("Densidade horário de ligações"):
        filtered_data['Hora'] = filtered_data['Connect time'].dt.hour + filtered_data['Connect time'].dt.minute / 60
        fig = px.histogram(filtered_data, x='Hora', nbins=14, range_x=[7, 21], title='Distribuição de Ligações por Hora do Dia')
        fig.update_layout(xaxis_title='Hora do Dia', yaxis_title='Número de Ligações', bargap=0.2)
        st.plotly_chart(fig)

    # Gráfico de barras de ligações por SDR
    with st.expander("Ligações por SDR"):
        sdr_counts = filtered_data['From'].value_counts().reset_index()
        sdr_counts.columns = ['From', 'Count']
        fig = px.bar(sdr_counts, x='Count', y='From', orientation='h', title='Número de Ligações por SDR')
        st.plotly_chart(fig)

    # Gráfico de linha de ligações ao longo do tempo
    with st.expander("Ligações por dia"):
        filtered_data['Data'] = filtered_data['Connect time'].dt.date
        line_data = filtered_data.groupby('Data').size().reset_index(name='Count')
        fig = px.line(line_data, x='Data', y='Count', title='Número de Ligações ao Longo do Tempo', markers=True)
        
        # Gráficos de linha por SDR na visão geral
        if selected_sdr == "Visão Geral":
            for sdr in sdrs:
                sdr_data = filtered_data[filtered_data['From'] == sdr]
                sdr_line_data = sdr_data.groupby('Data').size().reset_index(name='Count')
                fig.add_scatter(x=sdr_line_data['Data'], y=sdr_line_data['Count'], mode='lines+markers', name=sdr)
        
        st.plotly_chart(fig)
else:
    st.write("Por favor, faça o upload de um arquivo CSV para começar.")
