import requests
from bs4 import BeautifulSoup

def _to_float(value_str):
    if value_str is None: return None
    try: return float(str(value_str).replace('.', '').replace(',', '.'))
    except (ValueError, TypeError): return None

def _calculate_derived_metrics(data):
    if 'Dív.Líq/EBITDA' not in data:
        div_liq = _to_float(data.get('Dív. Líquida'))
        valor_firma = _to_float(data.get('Valor da firma'))
        ev_ebitda = _to_float(data.get('EV / EBITDA'))
        if valor_firma and ev_ebitda and ev_ebitda != 0:
            ebitda = valor_firma / ev_ebitda
            if div_liq and ebitda != 0:
                data['Dív.Líq/EBITDA'] = f"{(div_liq / ebitda):.2f}".replace('.', ',')
    # --- GARANTIA DE EXISTÊNCIA ---
    # Garante que a chave sempre exista, mesmo que o cálculo falhe
    if 'Dív.Líq/EBITDA' not in data:
        data['Dív.Líq/EBITDA'] = 'N/A'
    return data

def get_fundamentus_data(ticker):
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={ticker}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        dados_empresa = {}
        for table in soup.find_all('table'):
            for row in table.find_all('tr'):
                cells = [cell.text.strip() for cell in row.find_all('td')]
                for i in range(0, len(cells), 2):
                    if i + 1 < len(cells):
                        key = cells[i].replace('?', '')
                        value = cells[i+1]
                        if key: dados_empresa[key] = value
        if 'Papel' not in dados_empresa: return None
        dados_empresa = _calculate_derived_metrics(dados_empresa)
        if 'Empresa' in dados_empresa: dados_empresa['Nome'] = dados_empresa['Empresa']
        return dados_empresa
    except Exception as e:
        print(f"[Scraper] Falha ao processar {ticker}. Erro: {e}")
        return None