import pandas as pd
import numpy as np
def calculate_gordon_growth_model(df, risk_free_rate=0.105, market_return=0.15, cap=0.04):
    print("Calculando Preço Justo (Modelo de Gordon)...")
    results = []
    for _, row in df.iterrows():
        data = {'Ticker': row['Ticker'], 'Preco_Justo_Gordon': np.nan, 'Upside_Gordon': np.nan}
        try:
            preco, dy, cres, beta = row.get('Preco_Atual'), row.get('Div_Yield'), row.get('Cres_Rec_5a'), row.get('Beta')
            if all(pd.notna([preco, dy, cres, beta])) and preco > 0 and dy > 0:
                k = risk_free_rate + beta * (market_return - risk_free_rate)
                g = min(cres, cap) if cres > 0 else 0
                if k > g:
                    preco_justo = (dy * preco * (1 + g)) / (k - g)
                    if 0 < preco_justo < (preco * 5):
                        data['Preco_Justo_Gordon'] = preco_justo
                        data['Upside_Gordon'] = (preco_justo / preco) - 1
        except: pass
        results.append(data)
    return pd.DataFrame(results)