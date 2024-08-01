import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Função para processar novos dados
def process_new_data(new_data):
    df_col = new_data[['From', 'To', 'Connect time', 'Charged time, hour:min:sec']]
    
    valores_para_filtrar = ['3231420315', '3231420314', '3231420319', '1006 (3231420314 - Camila)',  
                            '1008 (3231420315 - Victoria)', '3231420316', '1010 (3231420316 - Aide)', '3231420312', 
                            '3231420310', '3231420313', '1002 (3231420312 - Vanessa)', 
                            '1012 (3231420310 - Leo)', '3231420317', 
                            '1015 (3231420319 - Gabriel)', '1004 (3231420313 - Joao Pedro)',
                            '1014 (3231420317 - Joao Vitor)'
                            ]

    df_col = df_col.loc[df_col['From'].isin(valores_para_filtrar)]

    substituicoes = {
        3231420314: '1006 (3231420314 - Camila)',
        3231420315: '1008 (3231420315 - Victoria)',
        3231420316 : '1010 (3231420316 - Aide)',
        3231420312: '1002 (3231420312 - Vanessa)',
        3231420313: '1004 (3231420313 - Joao Pedro)',
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
    
    # Dicionário de DDDs para estados
    ddd_to_state = {
        '61': 'Distrito Federal',
        '62': 'Goiás', '64': 'Goiás',
        '65': 'Mato Grosso', '66': 'Mato Grosso',
        '67': 'Mato Grosso do Sul',
        '82': 'Alagoas',
        '71': 'Bahia', '73': 'Bahia', '74': 'Bahia', '75': 'Bahia', '77': 'Bahia',
        '85': 'Ceará', '88': 'Ceará',
        '98': 'Maranhão', '99': 'Maranhão',
        '83': 'Paraíba',
        '81': 'Pernambuco', '87': 'Pernambuco',
        '86': 'Piauí', '89': 'Piauí',
        '84': 'Rio Grande do Norte',
        '79': 'Sergipe',
        '68': 'Acre',
        '96': 'Amapá',
        '92': 'Amazonas', '97': 'Amazonas',
        '91': 'Pará', '93': 'Pará', '94': 'Pará',
        '69': 'Rondônia',
        '95': 'Roraima',
        '63': 'Tocantins',
        '27': 'Espírito Santo', '28': 'Espírito Santo',
        '31': 'Minas Gerais', '32': 'Minas Gerais', '33': 'Minas Gerais', '34': 'Minas Gerais', '35': 'Minas Gerais', '37': 'Minas Gerais', 
        '38': 'Minas Gerais',
        '21': 'Rio de Janeiro', '22': 'Rio de Janeiro', '24': 'Rio de Janeiro',
        '11': 'São Paulo', '12': 'São Paulo', '13': 'São Paulo', '14': 'São Paulo', '15': 'São Paulo', '16': 'São Paulo', '17': 'São Paulo', 
        '18': 'São Paulo', '19': 'São Paulo',
        '41': 'Paraná', '42': 'Paraná', '43': 'Paraná', '44': 'Paraná', '45': 'Paraná', '46': 'Paraná',
        '51': 'Rio Grande do Sul', '53': 'Rio Grande do Sul', '54': 'Rio Grande do Sul', '55': 'Rio Grande do Sul',
        '47': 'Santa Catarina', '48': 'Santa Catarina', '49': 'Santa Catarina'
    }

    # Extraindo DDD e mapeando para o estado correspondente
    df_col['DDD'] = df_col['To'].str[2:4].map(ddd_to_state)

    return df_col

# Inicializando o Streamlit
st.set_page_config(page_title='Central Wealth', layout="wide")
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
        '1004 (3231420313 - Joao Pedro)', '1010 (3231420316 - Aide)'
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
            duration_filters.append((filtered_data['Charged time, hour:min:sec'] > timedelta(seconds=0)) & 
                                    (filtered_data['Charged time, hour:min:sec'] < timedelta(minutes=1)))
        if "Mais de 1 min" in selected_durations:
            duration_filters.append(filtered_data['Charged time, hour:min:sec'] >= timedelta(minutes=1))
        if "Mais de 2 min" in selected_durations:
            duration_filters.append(filtered_data['Charged time, hour:min:sec'] >= timedelta(minutes=2))
        filtered_data = filtered_data[pd.concat(duration_filters, axis=1).any(axis=1)]

    # Layout do Dashboard
    col1, col2, col3 = st.columns(3)

    # Histograma de horário das ligações
    with col1.expander("Densidade horário de ligações"):
        filtered_data['Hora'] = filtered_data['Connect time'].dt.hour + filtered_data['Connect time'].dt.minute / 60
        hist_fig = px.histogram(filtered_data, x='Hora', nbins=14, title='Distribuição de Ligações por Hora do Dia',
                                labels={'Hora':'Hora do Dia'}, range_x=[7, 20])
        hist_fig.update_traces(marker_line_width=2, marker_line_color='black')
        hist_fig.update_layout(xaxis=dict(tickmode='linear', dtick=1))
        st.plotly_chart(hist_fig, use_container_width=True)

    # Gráfico de barras de ligações por estado (antigo mapa de calor)
    with col1.expander("Número de Ligações por Estado"):
        # Contagem de ligações por estado
        state_counts = filtered_data['DDD'].value_counts().reset_index()
        state_counts.columns = ['Estado', 'Número de Ligações']
        # Criando o gráfico de barras
        bar_fig = px.bar(state_counts, x='Número de Ligações', y='Estado', orientation='h',
                         title='Número de Ligações por Estado',
                         labels={'Número de Ligações': 'Número de Ligações', 'Estado': 'Estado'})
        bar_fig.update_layout(xaxis_title='Número de Ligações', yaxis_title='Estado')
        st.plotly_chart(bar_fig, use_container_width=True)

    # Gráfico de barras de ligações por SDR
    with col2.expander("Ligações por SDR"):
        sdr_counts = filtered_data['From'].value_counts()
        bar_fig = px.bar(sdr_counts, orientation='h', title='Número de Ligações por SDR', labels={'index':'SDR', 'value':'Número de Ligações'})

        # Calcular a média das ligações por SDR
        avg_calls = sdr_counts.mean()

        # Adicionar linha vertical pontilhada vermelha para a média
        bar_fig.add_shape(
            type='line',
            x0=avg_calls, y0=-0.5, x1=avg_calls, y1=len(sdr_counts)-0.5,
            line=dict(color='red', width=2, dash='dot')
        )
        
        # Adicionar anotação para o valor da média no eixo x
        bar_fig.add_annotation(
            x=avg_calls, y=len(sdr_counts)-0.5, text=f"Média: {avg_calls:.2f}",
            showarrow=True, arrowhead=2, ax=0, ay=-40,
            bgcolor="red"
        )

        st.plotly_chart(bar_fig, use_container_width=True)


    # Gráfico de linha de ligações ao longo do tempo
    with col3.expander("Ligações por dia"):
        filtered_data['Data'] = filtered_data['Connect time'].dt.date
        line_data = filtered_data.groupby('Data').size().reset_index(name='counts')
        line_fig = px.line(line_data, x='Data', y='counts', markers=True, title='Número de Ligações ao Longo do Tempo')
        if selected_sdr == "Visão Geral":
            for sdr in sdrs:
                sdr_data = filtered_data[filtered_data['From'] == sdr]
                sdr_line_data = sdr_data.groupby('Data').size().reset_index(name=sdr)
                line_fig.add_scatter(x=sdr_line_data['Data'], y=sdr_line_data[sdr], mode='lines+markers', name=sdr)
    
        st.plotly_chart(line_fig, use_container_width=True)
else:
    st.write("Por favor, faça o upload de um arquivo CSV para começar.")
