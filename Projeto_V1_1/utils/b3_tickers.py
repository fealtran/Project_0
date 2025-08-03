import pandas as pd
import os

def get_b3_tickers():
    """
    Lê a lista de tickers da B3 de um arquivo CSV local no projeto.
    """
    print("Buscando lista de tickers do arquivo local...")
    try:
        # Constrói o caminho para o arquivo de dados de forma segura
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, '..', 'data', 'b3_tickers.csv')
        
        if not os.path.exists(file_path):
            print(f"Aviso: Arquivo de tickers não encontrado em {file_path}")
            return ['PETR4.SA', 'VALE3.SA'] # Fallback

        df = pd.read_csv(file_path)
        tickers_list = df['ticker'].dropna().unique().tolist()
        tickers_sa = [f"{ticker}.SA" for ticker in tickers_list]
        
        print(f"{len(tickers_sa)} tickers carregados do arquivo local.")
        return tickers_sa
    except Exception as e:
        print(f"Erro ao ler tickers do arquivo local: {e}")
        return ['PETR4.SA', 'VALE3.SA']