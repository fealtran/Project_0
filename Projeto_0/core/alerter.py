
import pandas as pd

def generate_alerts(df_ranking):
    """
    Gera uma lista de alertas e insights baseados no DataFrame de ranking final.
    """
    alerts = []
    
    if df_ranking.empty:
        return alerts

    # Ordena pelo Score para facilitar alertas de ranking
    df_sorted = df_ranking.sort_values(by='Score', ascending=False).reset_index(drop=True)

    # Itera sobre cada ação no ranking
    for index, row in df_sorted.iterrows():
        ticker = row['Ticker']
        
        # --- Regras de Alerta ---

        # Alerta de Ranking
        if index == 0: # A primeira da lista
            alerts.append(f"🏆 **Oportunidade Topo:** {ticker} é a ação com o maior Score no ranking atual.")

        # Alerta de Value (P/L)
        if pd.notna(row.get('PL')) and pd.notna(row.get('PL_Setor')):
            if row['PL'] > 0 and row['PL'] < row['PL_Setor'] * 0.8: # 20% abaixo da mediana
                alerts.append(f"💰 **Alerta de Value:** {ticker} tem um P/L ({row['PL']:.2f}) significativamente abaixo da mediana do setor ({row['PL_Setor']:.2f}).")
        
        # Alerta de Quality (ROE)
        if pd.notna(row.get('ROE')) and row['ROE'] > 0.20:
             alerts.append(f"⭐ **Alerta de Qualidade:** {ticker} apresenta um ROE elevado de {row['ROE']:.2%}.")
        
        # Alerta de Risco (VaR)
        if pd.notna(row.get('VaR_95%')) and row['VaR_95%'] < -0.035: # Perda potencial diária > 3.5%
            alerts.append(f"⚠️ **Alerta de Risco:** {ticker} mostra um VaR_95% de {row['VaR_95%']:.2%}, indicando alta volatilidade de curto prazo.")
            
    if not alerts:
        alerts.append("ℹ️ Nenhum alerta notável gerado para o universo de ações analisado.")
        
    print(f"{len(alerts)} alertas gerados.")
    return alerts
