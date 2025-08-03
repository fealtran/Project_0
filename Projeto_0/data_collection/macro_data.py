
import pandas as pd
import requests
from datetime import datetime, timedelta

def get_bcb_series(code, start_date, end_date):
    """
    Busca uma série temporal da API do Banco Central do Brasil (BCB).
    Documentação: https://dadosabertos.bcb.gov.br/dataset/11-taxa-de-juros---selic/resource/11a5b2b2-652a-43f9-b472-518a2e1055c6
    """
    # Formata as datas para a API
    start_date_str = start_date.strftime('%d/%m/%Y')
    end_date_str = end_date.strftime('%d/%m/%Y')
    
    # Monta a URL da API
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?formato=json&dataInicial={start_date_str}&dataFinal={end_date_str}'
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data)
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        df = df.set_index('data')
        df['valor'] = df['valor'].astype(float)
        # O BCB retorna a SELIC anual em %, então dividimos por 100 para obter a taxa e depois por 252 para a taxa diária aproximada
        if code == 11: # Código da SELIC
            df['valor'] = (df['valor'] / 100) / 252

        return df
    except Exception as e:
        print(f"Erro ao buscar a série {code} do BCB: {e}")
        return pd.DataFrame()

def get_macro_data(period_in_years=2):
    """
    Busca os principais dados macroeconômicos (SELIC, IPCA) para o período especificado.
    """
    print("Coletando dados macroeconômicos do Banco Central...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=int(period_in_years * 365.25))
    
    # Códigos das séries no SGS do BCB
    # 11: SELIC
    # 433: IPCA
    selic_df = get_bcb_series(11, start_date, end_date)
    ipca_df = get_bcb_series(433, start_date, end_date)
    
    # Renomeia as colunas para clareza
    selic_df.rename(columns={'valor': 'SELIC'}, inplace=True)
    ipca_df.rename(columns={'valor': 'IPCA'}, inplace=True)
    
    # Junta os DataFrames
    macro_df = pd.merge(selic_df, ipca_df, left_index=True, right_index=True, how='outer').ffill()
    
    print("Dados macroeconômicos coletados com sucesso.")
    return macro_df
