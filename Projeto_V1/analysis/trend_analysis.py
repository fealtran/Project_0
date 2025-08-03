import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_fundamental_trends(historical_df, years=3):
    """
    Calcula tendências em dados fundamentalistas históricos.
    - CAGR do ROE
    - Slope (inclinação) da regressão linear do P/L
    """
    print("Calculando tendências de fundamentos...")
    if historical_df.empty:
        return pd.DataFrame()

    # Garante que o índice seja datetime
    historical_df.index = pd.to_datetime(historical_df.index)
    
    results = []
    for ticker in historical_df['Ticker'].unique():
        ticker_df = historical_df[historical_df['Ticker'] == ticker].copy()
        
        # Filtra os dados para o período desejado
        ticker_df = ticker_df.last(f'{years}Y')
        if len(ticker_df) < 2:
            continue

        ticker_data = {'Ticker': ticker}

        # 1. CAGR do ROE
        roe = ticker_df['ROE'].dropna()
        if len(roe) >= 2:
            start_value = roe.iloc[0]
            end_value = roe.iloc[-1]
            if start_value > 0: # CAGR só é significativo para valores positivos
                num_periods = len(roe) - 1
                ticker_data[f'ROE_CAGR_{years}A'] = (end_value / start_value)**(1 / num_periods) - 1
        
        # 2. Tendência (Slope) do P/L
        pl = ticker_df['PL'].dropna().reset_index()
        if len(pl) >= 2:
            pl['time'] = np.arange(len(pl))
            X = pl[['time']]
            y = pl['PL']
            model = LinearRegression()
            model.fit(X, y)
            ticker_data['PL_Tendencia'] = model.coef_[0]
            
        results.append(ticker_data)
        
    return pd.DataFrame(results)