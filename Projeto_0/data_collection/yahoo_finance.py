import yfinance as yf
import pandas as pd

def coletar_dados_yahoo(tickers, period="5y", interval="1d"):
    """
    Coleta dados históricos de preços de fechamento do Yahoo Finance.
    A função lida tanto com um único ticker quanto com uma lista de tickers.
    """
    print(f"Coletando dados de preços para {len(tickers)} tickers do Yahoo Finance...")
    try:
        # Baixa os dados. 'Close' seleciona apenas o preço de fechamento.
        # 'auto_adjust=True' ajusta para dividendos e splits.
        data = yf.download(
            tickers,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False
        )['Close']

        # Se apenas um ticker for solicitado, yf.download retorna uma Series. Convertemos para DataFrame.
        if isinstance(data, pd.Series):
            data = data.to_frame(name=tickers[0])

        # Remove linhas que contenham apenas NaNs (feriados, etc.)
        data.dropna(how='all', inplace=True)

        print("Coleta de dados de preços concluída.")
        return data

    except Exception as e:
        print(f"Ocorreu um erro ao coletar dados do Yahoo Finance: {e}")
        # Retorna um DataFrame vazio em caso de erro.
        return pd.DataFrame()