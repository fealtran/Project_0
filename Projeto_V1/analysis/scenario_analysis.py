import pandas as pd

def run_scenario_analysis(precos, macro_data, ranking_df):
    """
    Calcula o beta em relação ao dólar e estima o impacto de cenários de estresse.
    """
    print("Executando análise de cenários...")
    if precos.empty or macro_data.empty or 'DOLAR' not in macro_data.columns:
        return pd.DataFrame()

    retornos_ativos = precos.pct_change()
    retornos_macro = macro_data.pct_change()

    # Calcula o 'Beta do Dólar'
    df_merged = pd.merge(retornos_ativos, retornos_macro['DOLAR'], left_index=True, right_index=True, how='inner')
    
    cov_matrix = df_merged.cov()
    var_dolar = df_merged['DOLAR'].var()
    
    beta_dolar = cov_matrix['DOLAR'] / var_dolar if var_dolar != 0 else 0
    beta_dolar = beta_dolar.drop('DOLAR').rename('Beta_DOLAR')
    
    # Junta os betas ao ranking
    df_cenarios = pd.merge(ranking_df, beta_dolar, left_on='Ticker', right_index=True, how='left')
    
    return df_cenarios