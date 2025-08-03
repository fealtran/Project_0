import streamlit as st
import pandas as pd
import main
import config
from core import database_manager as dbm
from reporting import visualizations as viz

# --- Configuração da Página ---
st.set_page_config(layout="wide", page_title="Análise de Ações BR")
st.title("Dashboard de Análise de Ações Brasileiras")

# --- Funções de Cache ---
@st.cache_data(ttl=3600) # Cache por 1 hora
def run_full_analysis(tickers_list, score_weights):
    print("--- Executando Análise Completa (Cache Miss) ---")
    return main.run_analysis(tickers_list=tickers_list, score_weights=score_weights, run_backtest_flag=True)

# --- Barra Lateral (Inputs) ---
with st.sidebar:
    st.header("Configurações da Análise")
    
    lista_selecionada = st.selectbox(
        "Selecione uma lista de ativos:", 
        list(config.TICKER_LISTS.keys()),
        key='ticker_list_selector'
    )
    tickers_list = config.TICKER_LISTS[lista_selecionada]

    st.subheader("Pesos do Score Flexível")
    weights = {}
    for metric, params in config.SCORE_WEIGHTS.items():
        weights[metric] = {
            "weight": st.slider(f"Peso para {metric}", 0.0, 1.0, params['weight'], 0.05),
            "ascending": params['ascending']
        }
    
    if st.button("Executar Análise"):
        st.cache_data.clear() # Limpa o cache para forçar a re-execução

# --- Lógica Principal ---
if tickers_list:
    results = run_full_analysis(tickers_list, weights)
    ranking_df = results["ranking"]
    alerts_df = results["alerts"]
    backtest_results = results["backtest"]
    prices_df = results["prices"]
    
    # Inicializa o session_state para o ticker selecionado se não existir
    if 'selected_ticker' not in st.session_state:
        st.session_state.selected_ticker = tickers_list[0]

    # --- Visão Geral e Ranking ---
    st.subheader("Ranking de Ativos e Alertas")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.dataframe(ranking_df)
    with col2:
        st.write("Alertas:")
        st.dataframe(alerts_df)

    # --- Análise Individual ---
    st.subheader("Análise Individual Detalhada")
    
    # Seletor de ativos que atualiza o session_state
    st.session_state.selected_ticker = st.selectbox(
        "Selecione um ativo para ver os detalhes:", 
        tickers_list, 
        index=tickers_list.index(st.session_state.selected_ticker) # Mantém a seleção
    )
    
    if st.session_state.selected_ticker:
        # Busca dados históricos para o ticker selecionado
        historical_df = dbm.get_historical_fundamentals(st.session_state.selected_ticker)
        
        # Abas para organizar a análise
        tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Gráfico de Preços", "Fundamentos Históricos", "Análise de Risco"])

        with tab1:
            st.write(f"**Dados para {st.session_state.selected_ticker}**")
            st.dataframe(ranking_df[ranking_df['Ticker'] == st.session_state.selected_ticker].T)
        
        with tab2:
            price_chart = viz.plot_price_and_mavg(prices_df, st.session_state.selected_ticker, config.OUTPUT_DIR)
            st.plotly_chart(price_chart, use_container_width=True)
            
        with tab3:
            funda_chart = viz.plot_historical_fundamentals(historical_df, st.session_state.selected_ticker)
            st.plotly_chart(funda_chart, use_container_width=True)
            
        with tab4:
            st.write("Métricas de Risco:")
            risk_metrics = ['Volatilidade', 'Beta', 'Max_Drawdown', 'VaR_95']
            risk_data = ranking_df[ranking_df['Ticker'] == st.session_state.selected_ticker][risk_metrics]
            st.dataframe(risk_data)

    # --- Backtest ---
    if backtest_results:
        st.subheader("Resultado do Backtest da Estratégia")
        performance_summary = backtest_results["summary"]
        backtest_chart_df = backtest_results["performance_df"]
        
        st.dataframe(pd.DataFrame([performance_summary]))
        
        backtest_chart = viz.plot_backtest_performance(backtest_chart_df, config.OUTPUT_DIR)
        st.plotly_chart(backtest_chart, use_container_width=True)
else:
    st.warning("Por favor, selecione uma lista de ativos na barra lateral.")