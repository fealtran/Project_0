import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
HEADERS = {'User-Agent': 'Mozilla/5.0'}
def find_indicator_value(soup, label_text):
    try:
        tag = soup.find(lambda t: t.name == 'td' and label_text in t.get_text(strip=True))
        return tag.find_next_sibling('td').get_text(strip=True) if tag else None
    except: return None
def coletar_dados_fundamentus(tickers):
    print("Coletando dados do Fundamentus...")
    all_data = []
    indicators_map = {
        'PL': 'P/L', 'PVP': 'P/VP', 'Div_Yield': 'Div. Yield', 'ROE': 'ROE',
        'Cres_Rec_5a': 'Cres. Rec (5a)', 'Setor': 'Setor', 'ROIC': 'ROIC'
    }
    for ticker in tickers:
        data = {'Ticker': ticker}
        try:
            url = f'https://www.fundamentus.com.br/detalhes.php?papel={ticker.split(".")[0]}'
            response = requests.get(url, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(response.text, 'lxml')
            for col_name, label_text in indicators_map.items():
                data[col_name] = find_indicator_value(soup, label_text)
            all_data.append(data)
        except Exception as e:
            print(f"Falha ao processar {ticker}: {e}")
            all_data.append(data)
    return pd.DataFrame(all_data)