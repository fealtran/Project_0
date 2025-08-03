import pandas as pd
def run_sector_analysis(df):
    if 'Setor' not in df.columns or df['Setor'].isnull().all(): return df
    metrics = ['PL', 'PVP', 'Div_Yield', 'ROE', 'Sharpe', 'Quality_Score', 'Value_Score', 'Growth_Score']
    available = [m for m in metrics if m in df.columns]
    sector_medians = df.groupby('Setor')[available].median(numeric_only=True)
    sector_medians.rename(columns={m: f"{m}_Setor" for m in available}, inplace=True)
    return pd.merge(df, sector_medians, on='Setor', how='left')