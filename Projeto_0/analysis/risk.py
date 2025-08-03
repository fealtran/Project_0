
import pandas as pd

def calculate_historical_var(prices, confidence_level=0.95):
    """
    Calcula o Value at Risk (VaR) Histórico para cada ativo.
    
    O VaR Histórico simplesmente encontra o n-ésimo pior retorno diário no histórico,
    onde n é o nível de confiança.
    """
    if prices.empty:
        return pd.DataFrame()

    # Calcula os retornos diários
    returns = prices.pct_change().dropna()
    
    # Calcula o VaR para cada ticker. O quantile é 1 - o nível de confiança.
    # Ex: Para 95% de confiança, queremos o 5º percentil (o corte dos 5% piores dias).
    var_quantile = 1 - confidence_level
    var = returns.quantile(var_quantile)
    
    var_df = var.to_frame(name=f'VaR_{confidence_level:.0%}').reset_index()
    var_df.rename(columns={'index': 'Ticker'}, inplace=True)
    
    print(f"VaR Histórico ({confidence_level:.0%}) calculado.")
    return var_df
