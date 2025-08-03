import pandas as pd
import numpy as np

def calculate_basic_metrics(precos, ibov_data):
    retornos = precos.pct_change(fill_method=None)
    retorno_ibov = ibov_data.pct_change(fill_method=None).rename(columns={'IBOV':'IBOV_ret'})
    resultados = []
    for col in retornos.columns:
        df_sync = pd.concat([retornos[col], retorno_ibov], axis=1, join='inner').dropna()
        if len(df_sync) > 1:
            cov = df_sync.cov().iloc[0,1]
            var_ibov = df_sync['IBOV_ret'].var()
            beta = cov / var_ibov if var_ibov != 0 else np.nan
        else:
            beta = np.nan
        resultados.append({'Ticker': col, 'Beta': beta})
    return pd.DataFrame(resultados)