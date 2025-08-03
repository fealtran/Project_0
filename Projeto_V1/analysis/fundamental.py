import pandas as pd
import numpy as np
def clean_and_convert_data(df):
    df_clean = df.copy()
    percent_columns = ['Div_Yield', 'ROE', 'ROIC', 'Cres_Rec_5a']
    for col in df_clean.columns:
        if col not in ['Ticker', 'Setor']:
            series = df_clean[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.rstrip('%').str.strip()
            df_clean[col] = pd.to_numeric(series, errors='coerce')
            if col in percent_columns: df_clean[col] /= 100
    return df_clean
def calculate_flexible_score(df, weights):
    df_score = df.copy()
    for metric, weight_info in weights.items():
        if metric in df_score.columns:
            df_score[f"Score_{metric}"] = df_score[metric].rank(ascending=weight_info['ascending'], pct=True).fillna(0.5)
    df_score['Score'] = 0
    for metric, weight_info in weights.items():
        if f"Score_{metric}" in df_score.columns: df_score['Score'] += df_score[f"Score_{metric}"] * weight_info['weight']
    return df_score
def calculate_qvg_scores(df, qvg_map):
    df_qvg = df.copy(); results = {'Ticker': df_qvg['Ticker']}
    for category, metrics in qvg_map.items():
        category_score_col = f"{category}_Score"; df_qvg[category_score_col] = 0
        valid_metrics = [m for m in metrics.keys() if m in df_qvg.columns]
        if not valid_metrics: results[category_score_col] = 0.0; continue
        for metric in valid_metrics:
            params = metrics[metric]
            df_qvg[category_score_col] += df_qvg[metric].rank(ascending=params['ascending'], pct=True).fillna(0.5)
        results[category_score_col] = df_qvg[category_score_col] / len(valid_metrics)
    return pd.DataFrame(results)
def calculate_piotroski_f_score(df): return pd.DataFrame() # Dummy