import pandas as pd
import numpy as np
# ... (outras funções do advanced_quantitative)
def calculate_correlations(precos, macro_data):
    if precos.empty or macro_data.empty: return pd.DataFrame()
    retornos_ativos = precos.pct_change(fill_method=None)
    retornos_macro = macro_data.pct_change(fill_method=None)
    df_merged = pd.merge(retornos_ativos, retornos_macro, left_index=True, right_index=True, how='inner')
    correlations = df_merged.corr()
    corr_ibov = correlations['IBOV'].drop(['IBOV', 'DOLAR'])
    corr_dolar = correlations['DOLAR'].drop(['IBOV', 'DOLAR'])
    return pd.DataFrame({'Corr_IBOV': corr_ibov, 'Corr_DOLAR': corr_dolar}).reset_index().rename(columns={'index': 'Ticker'})
def calculate_advanced_risk_metrics(precos):
    if precos.empty: return pd.DataFrame()
    retornos = precos.pct_change(fill_method=None)
    retorno_anualizado = (1 + retornos.mean())**252 - 1
    downside_deviation = retornos[retornos < 0].std() * np.sqrt(252)
    sortino_ratio = retorno_anualizado / downside_deviation
    return pd.DataFrame({'Sortino_Ratio': sortino_ratio}).reset_index().rename(columns={'index': 'Ticker'})
# ... (demais funções)