
import pandas as pd

def calculate_sector_metrics(df):
    # ... (código existente sem alterações) ...
    if 'Setor' not in df.columns or df['Setor'].isnull().all(): return df
    metrics_to_analyze = ['PL', 'ROE', 'Div. Yield', 'Mrg. Líq.', 'PVP']
    existing_metrics = [metric for metric in metrics_to_analyze if metric in df.columns]
    for metric in existing_metrics: df[metric] = pd.to_numeric(df[metric], errors='coerce')
    sector_medians = df.groupby('Setor')[existing_metrics].median()
    sector_medians.rename(columns={metric: f'{metric}_Setor' for metric in existing_metrics}, inplace=True)
    df_with_sector = pd.merge(df, sector_medians, on='Setor', how='left')
    print("Análise setorial concluída."); return df_with_sector

def calculate_sector_momentum(prices, fundamentals):
    """Calcula o momentum de cada setor."""
    if prices.empty or fundamentals.empty or 'Setor' not in fundamentals.columns:
        return pd.DataFrame()
    
    ticker_sector_map = fundamentals.set_index('Ticker')['Setor']
    sector_prices = prices.T.join(ticker_sector_map).groupby('Setor').mean().T
    
    # Calcula retornos e score de momentum para os setores
    ret_1m = sector_prices.pct_change(periods=21).iloc[-1]
    ret_3m = sector_prices.pct_change(periods=63).iloc[-1]
    ret_6m = sector_prices.pct_change(periods=126).iloc[-1]
    
    momentum_df = pd.DataFrame({'Ret_1M': ret_1m, 'Ret_3M': ret_3m, 'Ret_6M': ret_6m}).fillna(0)
    momentum_df['Momentum_Score'] = momentum_df.rank(ascending=False, pct=True).mean(axis=1)
    
    print("Momentum setorial calculado.")
    return momentum_df.sort_values('Momentum_Score', ascending=False)
