import pandas as pd
from datetime import datetime

# Importação dos módulos do projeto
from data_collection import fundamentus_scraper as funda_scrap, yahoo_finance as yf
from core import database_manager as dbm, backtester, alerter
from analysis import fundamental as funda, quantitative as quant, advanced_quantitative as quant_adv, sector
from reporting import visualizations as viz, report_generator

def run_analysis(tickers_list, score_weights, run_backtest_flag=False):
    """
    Orquestra a execução completa da análise.
    """
    print("--- Iniciando Análise ---")
    
    # --- 1/4 - Coletando Dados ---
    print("1/4 - Coletando Dados...")
    precos = yf.coletar_dados_yahoo(tickers_list + ['^BVSP'], period="5y")
    ibov_data = precos[['^BVSP']].copy()
    precos = precos.drop(columns=['^BVSP'])

    fundamentos_hoje = funda_scrap.coletar_dados_fundamentus(tickers_list)
    fundamentos_hoje['data_coleta'] = datetime.now().strftime('%Y-%m-%d')
    
    dbm.init_db()
    dbm.save_to_db(fundamentos_hoje)
    fundamentos_db = dbm.load_latest_from_db(tickers_list)
    
    if fundamentos_db.empty:
        print("Aviso: Não foi possível carregar dados do banco de dados. Usando dados da coleta de hoje.")
        df_fundos = funda.clean_and_convert_data(fundamentos_hoje.copy())
    else:
        df_fundos = funda.clean_and_convert_data(fundamentos_db.copy())

    # --- 2/4 - Análise e Scores ---
    print("2/4 - Análise e Scores...")
    metricas_quant = quant.calculate_basic_metrics(precos, ibov_data)
    df_merged = pd.merge(metricas_quant, df_fundos, on='Ticker', how='left')

    # Cálculos avançados
    momentum = quant_adv.calculate_momentum_score(precos); df_merged = pd.merge(df_merged, momentum, on='Ticker', how='left')
    drawdown = quant_adv.calculate_max_drawdown(precos); df_merged = pd.merge(df_merged, drawdown, on='Ticker', how='left')
    var = quant_adv.calculate_historical_var(precos); df_merged = pd.merge(df_merged, var, on='Ticker', how='left')
    
    # F-Score
    historico_completo = pd.concat([dbm.get_historical_fundamentals(t) for t in tickers_list])
    f_score = funda.calculate_piotroski_f_score(historico_completo)
    if not f_score.empty:
        df_merged = pd.merge(df_merged, f_score, on='Ticker', how='left')

    # Score Flexível
    ranking = funda.calculate_flexible_score(df_merged, score_weights)
    
    # Análise setorial
    ranking_setorial = sector.run_sector_analysis(ranking)
    
    # --- 3/4 - Backtest e Alertas ---
    print("3/4 - Backtest e Alertas...")
    backtest_results = None
    if run_backtest_flag:
        backtest_results = backtester.run_backtest(precos, ranking, ibov_data)

    alertas = alerter.check_alerts(ranking_setorial)
    
    # --- 4/4 - Finalizando ---
    print("4/4 - Finalizando...")
    
    results = {
        "ranking": ranking_setorial,
        "alerts": alertas,
        "backtest": backtest_results,
        "prices": precos
    }
    
    return results