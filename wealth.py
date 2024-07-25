import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página
st.set_page_config(page_title="Stock Tracker", layout="wide")

# Função para carregar a imagem
def load_image(image_path):
    st.image(image_path, use_column_width=True)
    st.markdown(
        """
        <style>
        .stImage {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Função para configurar estilos
def set_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #000000;
            color: #FFD700;
        }
        .sidebar .sidebar-content {
            background-color: #000000; /* Fundo preto */
            color: #FFFFFF; /* Fonte branca */
        }
        .sidebar .sidebar-content a {
            color: #FFFFFF; /* Links em branco */
        }
        .login-button {
            background-color: #FFD700;
            color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_styles()

# Carregar dados de login
login_df = pd.read_csv("login.csv")

# Verifica o estado do login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Definir a página principal
def main_page():
    # Carregar os dados
    df = pd.read_csv('colaboradores.csv')

    # Função para gerar cores diferentes
    def get_colors(n):
        np.random.seed(0)
        return np.random.rand(n, 3)

    # Função para exibir o gráfico de pizza
    def plot_pie():
        colors = get_colors(len(df))
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(df['Patrim'], labels=df['Nome'], autopct='%1.1f%%', startangle=140, colors=colors)
        ax.set_title('Patrimônio de Cada Colaborador')
        st.pyplot(fig)

    # Função para exibir o gráfico de dispersão
    def plot_scatter():
        fig, ax = plt.subplots(figsize=(8, 6))
        scatter = ax.scatter(df['Patrim'], df['Capt'], c='#FFD700', edgecolors='w', s=100)
        ax.set_xlabel('Patrimônio')
        ax.set_ylabel('Captação')
        ax.set_title('Patrimônio vs Captação')
        
        # Adicionar nomes ao lado de cada ponto
        for i, txt in enumerate(df['Nome']):
            ax.text(df['Patrim'][i], df['Capt'][i], txt, fontsize=9, ha='right', color='#FFD700')
        
        st.pyplot(fig)

    # Função para exibir o gráfico de barras para Capt
    def plot_bars_capt():
        fig, ax = plt.subplots(figsize=(8, 6))
        df.plot(kind='bar', x='Nome', y='Capt', ax=ax, color='#FFD700', legend=False)
        ax.set_title('Captação de Cada Colaborador')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        st.pyplot(fig)

    # Função para exibir o gráfico de barras para ReunMar
    def plot_bars_reunmar():
        fig, ax = plt.subplots(figsize=(8, 6))
        df.plot(kind='bar', x='Nome', y='ReunMar', ax=ax, color='#FFD700', legend=False)
        ax.set_title('Número de Reuniões por Mês de Cada Colaborador')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        st.pyplot(fig)

    # Função para exibir o gráfico de barras para Vendas
    def plot_bars_vendas():
        fig, ax = plt.subplots(figsize=(8, 6))
        df.plot(kind='bar', x='Nome', y='Vendas', ax=ax, color='#FFD700', legend=False)
        ax.set_title('Vendas de Cada Colaborador')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
        st.pyplot(fig)

    # Cabeçalho com imagem
    st.sidebar.image('simpla.png', use_column_width=True)

    # Menu lateral
    st.sidebar.title('Menu')
    options = st.sidebar.multiselect('Escolha até 4 gráficos', 
                                     ['Patrimônio', 'Scatter', 'Captação', 'ReunMar', 'Vendas'])

    # Divisão da tela para múltiplos gráficos
    num_options = len(options)
    
    if num_options == 1:
        plot_container = st.container()
        with plot_container:
            if options[0] == 'Patrimônio':
                plot_pie()
            elif options[0] == 'Scatter':
                plot_scatter()
            elif options[0] == 'Captação':
                plot_bars_capt()
            elif options[0] == 'ReunMar':
                plot_bars_reunmar()
            elif options[0] == 'Vendas':
                plot_bars_vendas()
    elif num_options == 2:
        col1, col2 = st.columns(2)
        with col1:
            if options[0] == 'Patrimônio':
                plot_pie()
            elif options[0] == 'Scatter':
                plot_scatter()
            elif options[0] == 'Captação':
                plot_bars_capt()
            elif options[0] == 'ReunMar':
                plot_bars_reunmar()
            elif options[0] == 'Vendas':
                plot_bars_vendas()
        with col2:
            if options[1] == 'Patrimônio':
                plot_pie()
            elif options[1] == 'Scatter':
                plot_scatter()
            elif options[1] == 'Captação':
                plot_bars_capt()
            elif options[1] == 'ReunMar':
                plot_bars_reunmar()
            elif options[1] == 'Vendas':
                plot_bars_vendas()
    elif num_options == 3:
        col1, col2 = st.columns(2)
        with col1:
            if options[0] == 'Patrimônio':
                plot_pie()
            elif options[0] == 'Scatter':
                plot_scatter()
            elif options[0] == 'Captação':
                plot_bars_capt()
            elif options[0] == 'ReunMar':
                plot_bars_reunmar()
            elif options[0] == 'Vendas':
                plot_bars_vendas()
            if options[1] == 'Patrimônio':
                plot_pie()
            elif options[1] == 'Scatter':
                plot_scatter()
            elif options[1] == 'Captação':
                plot_bars_capt()
            elif options[1] == 'ReunMar':
                plot_bars_reunmar()
            elif options[1] == 'Vendas':
                plot_bars_vendas()
        with col2:
            if options[2] == 'Patrimônio':
                plot_pie()
            elif options[2] == 'Scatter':
                plot_scatter()
            elif options[2] == 'Captação':
                plot_bars_capt()
            elif options[2] == 'ReunMar':
                plot_bars_reunmar()
            elif options[2] == 'Vendas':
                plot_bars_vendas()
    elif num_options == 4:
        col1, col2 = st.columns(2)
        with col1:
            if options[0] == 'Patrimônio':
                plot_pie()
            elif options[0] == 'Scatter':
                plot_scatter()
            elif options[0] == 'Captação':
                plot_bars_capt()
            elif options[0] == 'ReunMar':
                plot_bars_reunmar()
            elif options[0] == 'Vendas':
                plot_bars_vendas()
            if options[1] == 'Patrimônio':
                plot_pie()
            elif options[1] == 'Scatter':
                plot_scatter()
            elif options[1] == 'Captação':
                plot_bars_capt()
            elif options[1] == 'ReunMar':
                plot_bars_reunmar()
            elif options[1] == 'Vendas':
                plot_bars_vendas()
        with col2:
            if options[2] == 'Patrimônio':
                plot_pie()
            elif options[2] == 'Scatter':
                plot_scatter()
            elif options[2] == 'Captação':
                plot_bars_capt()
            elif options[2] == 'ReunMar':
                plot_bars_reunmar()
            elif options[2] == 'Vendas':
                plot_bars_vendas()
            if options[3] == 'Patrimônio':
                plot_pie()
            elif options[3] == 'Scatter':
                plot_scatter()
            elif options[3] == 'Captação':
                plot_bars_capt()
            elif options[3] == 'ReunMar':
                plot_bars_reunmar()
            elif options[3] == 'Vendas':
                plot_bars_vendas()

# Definir a página de login
def login_page():
    load_image("simpla.png")

    # Caixas de texto para login e senha
    login = st.text_input("Login")
    password = st.text_input("Senha", type="password")

    # Botão de login
    if st.button("LOGIN"):
        if (login in login_df['Login'].values) and (password in login_df[login_df['Login'] == login]['Senha'].values):
            st.session_state.logged_in = True
            st.success("Acesso liberado! Bem-vindo à página principal.")
            st.experimental_rerun()  # Recarregar a página para aplicar o login
        else:
            st.error("Dados de login inválidos.")

# Verifica se o usuário está logado
if st.session_state.logged_in:
    main_page()
else:
    login_page()
