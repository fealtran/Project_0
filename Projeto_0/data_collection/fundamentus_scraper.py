import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def _get_indicator(soup, label):
    """Função auxiliar para buscar um indicador no HTML de forma segura."""
    try:
        # Encontra o <td> com o texto do label e pega o próximo <td> que é o valor
        value_cell = soup.find('td', string=lambda text: text and label in text).find_next_sibling('td')
        return value_cell.get_text(strip=True)
    except AttributeError:
        return None # Retorna None se o label não for encontrado

def coletar_dados_fundamentus(tickers):
    """
    Coleta dados fundamentalistas do site Fundamentus para uma lista de tickers.
    Usa BeautifulSoup para uma extração "cirúrgica", que é mais robusta.
    """
    print("Coletando dados do Fundamentus (Modo Cirúrgico)...")
    all_data = []

    for i, ticker in enumerate(tickers, 1):
        try:
            # O site Fundamentus usa o ticker base (ex: ITUB4), sem o sufixo .SA
            ticker_base = ticker.split('.')[0]
            url = f'https://www.fundamentus.com.br/detalhes.php?papel={ticker_base}'
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Mapeamento dos labels no site para os nomes das colunas que queremos
            indicators_map = {
                'P/L': 'P/L', 'P/VP': 'P/VP', 'Div. Yield': 'Div. Yield',
                'ROE': 'ROE', 'ROIC': 'ROIC', 'ROA': 'ROA',
                'Patrim. Líq': 'Patrim. Líq',
                'Dív. Bruta / Patrim.': 'Div_Br_Patrim', # Label exato do site
                'Liq. Corr.': 'Liq_Corrente',
                'Giro Ativos': 'Giro_Ativos',
                'Nro. Ações': 'Nro_Acoes',
                'Marg. Bruta': 'Marg_Bruta',
                'Cres. Rec (5a)': 'Cres. Rec (5a)',
                'Setor': 'Setor' # O label no site é 'Setor', não 'Setor:'
            }
            
            data = {'Ticker': ticker}
            for label, col_name in indicators_map.items():
                data[col_name] = _get_indicator(soup, label)
            
            # Caso especial para Lucro Líquido (pegar o dos últimos 12 meses)
            # O label de Lucro Líquido aparece duas vezes, precisamos ser mais específicos
            lucro_liquido_label = soup.find_all('td', class_='label', string='Lucro Líquido')
            if len(lucro_liquido_label) > 1:
                # O segundo é geralmente o dos últimos 12 meses
                data['Lucro_Liquido'] = lucro_liquido_label[1].find_next_sibling('td').get_text(strip=True)

            all_data.append(data)
            print(f"({i}/{len(tickers)}) Dados para {ticker_base} ({ticker}) coletados com sucesso.")

        except requests.exceptions.RequestException as e:
            print(f"({i}/{len(tickers)}) Erro de conexão para {ticker}: {e}")
        except Exception as e:
            print(f"({i}/{len(tickers)}) Ocorreu um erro inesperado para o ticker {ticker}: {e}")
        
        time.sleep(0.5) # Pausa para não sobrecarregar o servidor do site

    print("Coleta de dados do Fundamentus concluída.")
    if not all_data:
        return pd.DataFrame()
        
    return pd.DataFrame(all_data)