import pandas as pd
import numpy as np

def clean_and_convert_data(df):
    """Limpa e converte os dados fundamentalistas para formatos numéricos."""
    for col in df.columns:
        if col != 'Ticker' and col != 'Setor':
            # Remove o prefixo '?' se existir
            if df[col].astype(str).str.startswith('?').any():
                df[col] = df[col].astype(str).str.lstrip('?')

            # Converte para numérico, tratando erros e formatos
            df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.rstrip('%').str.strip()
            df[col] = pd.to_numeric(df[col], errors='coerce')

            # Ajusta a escala de porcentagens
            if '%' in str(df[col].name) or col in ['Div. Yield', 'ROE', 'ROIC', 'Cres. Rec (5a)']:
                 df[col] = df[col] / 100

    # Renomeia colunas para remover caracteres especiais
    df = df.rename(columns={
        'P/L': 'PL',
        'P/VP': 'PVP',
        'Div. Yield': 'Div_Yield',
        'Patrim. Líq': 'Patrim_Liq',
        'Cres. Rec (5a)': 'Cres_Rec_5a'
    })
    return df

def calculate_piotroski_f_score(df_historico):
    """
    Calcula o Piotroski F-Score para cada ticker com base em seu histórico.
    O F-Score é a soma de 9 critérios binários (0 ou 1).
    """
    if df_historico.empty:
        return pd.DataFrame(columns=['Ticker', 'F_Score'])

    df_historico['data_coleta'] = pd.to_datetime(df_historico['data_coleta'])
    df_historico = df_historico.sort_values(by=['Ticker', 'data_coleta'])

    scores = {}
    for ticker, group in df_historico.groupby('Ticker'):
        if len(group) < 2:
            scores[ticker] = np.nan
            continue

        # Pega os dois balanços mais recentes
        latest = group.iloc[-1]
        previous = group.iloc[-2]
        score = 0

        # --- Rentabilidade ---
        # 1. ROA (Return on Assets) positivo
        if latest.get('ROA', 0) > 0: score += 1
        # 2. FCO (Fluxo de Caixa Operacional) positivo
        if latest.get('FCO', 0) > 0: score += 1 # Assumindo que temos FCO
        # 3. ROA crescente
        if latest.get('ROA', 0) > previous.get('ROA', 0): score += 1
        # 4. FCO > Lucro Líquido (Accruals)
        if latest.get('FCO', 0) > latest.get('Lucro_Liquido', 0): score += 1

        # --- Alavancagem, Liquidez e Fonte de Capital ---
        # 5. Dívida Bruta/Patrimônio decrescente (menor alavancagem)
        if latest.get('Div_Br_Patrim', 1) < previous.get('Div_Br_Patrim', 1): score += 1
        # 6. Liquidez Corrente crescente
        if latest.get('Liq_Corrente', 0) > previous.get('Liq_Corrente', 0): score += 1
        # 7. Não houve emissão de novas ações
        if latest.get('Nro_Acoes', 0) <= previous.get('Nro_Acoes', 0): score += 1

        # --- Eficiência Operacional ---
        # 8. Margem Bruta crescente
        if latest.get('Marg_Bruta', 0) > previous.get('Marg_Bruta', 0): score += 1
        # 9. Giro do Ativo crescente
        if latest.get('Giro_Ativos', 0) > previous.get('Giro_Ativos', 0): score += 1

        scores[ticker] = score

    f_score_df = pd.DataFrame(list(scores.items()), columns=['Ticker', 'F_Score'])
    return f_score_df


def calculate_flexible_score(df, weights):
    """Calcula um score flexível com base em pesos customizáveis."""
    df_score = df.copy()
    
    # Normalização por Rank Percentil (maior = melhor)
    for metric, weight_info in weights.items():
        if metric in df_score.columns:
            ascending = weight_info['ascending']
            # Cria um nome de score único para cada métrica
            score_col_name = f"Score_{metric}"
            df_score[score_col_name] = df_score[metric].rank(ascending=ascending, pct=True).fillna(0.5)

    # Cálculo do Score Final Ponderado
    df_score['Score'] = 0
    for metric, weight_info in weights.items():
        score_col_name = f"Score_{metric}"
        if score_col_name in df_score.columns:
            df_score['Score'] += df_score[score_col_name] * weight_info['weight']
            
    return df_score