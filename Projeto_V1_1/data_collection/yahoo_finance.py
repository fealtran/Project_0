import yfinance as yf
import pandas as pd

def coletar_dados_yahoo(tickers, period="5y"):
    print("Coletando dados de preços do Yahoo Finance...")
    try:
        data = yf.download(tickers, period=period, auto_adjust=True, progress=False)
        
        # Identifica os tickers que falharam (colunas são todas NaN)
        failed_tickers = data['Close'].columns[data['Close'].isnull().all()].tolist()
        if failed_tickers:
            print(f"Aviso: Falha no download para os tickers: {failed_tickers}")
            # Remove os tickers que falharam de todas as colunas (Open, High, Low, Close, Volume)
            data.drop(columns=failed_tickers, level=1, inplace=True)
            
        return data.dropna(how='all')
    except Exception as e:
        print(f"Erro crítico ao coletar dados do Yahoo Finance: {e}")
        return pd.DataFrame()