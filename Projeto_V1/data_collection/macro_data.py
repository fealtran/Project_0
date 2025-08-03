import yfinance as yf
import pandas as pd
def coletar_dados_macro(period="5y"):
    print("Coletando dados macro (IBOV, Dólar)...")
    try:
        data = yf.download(['^BVSP', 'USDBRL=X'], period=period, auto_adjust=True, progress=False)['Close']
        if '^BVSP' in data.columns: data.rename(columns={'^BVSP': 'IBOV'}, inplace=True)
        if 'USDBRL=X' in data.columns: data.rename(columns={'USDBRL=X': 'DOLAR'}, inplace=True)
        return data.dropna(how='all')
    except Exception as e: return pd.DataFrame()