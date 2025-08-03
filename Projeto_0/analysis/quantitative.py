
import pandas as pd
import numpy as np

def calculate_basic_metrics(precos, ibov):
    """Calcula métricas quantitativas básicas (beta, volatilidade, retorno anual e sharpe)"""
    if precos.empty:
        return pd.DataFrame()
    retornos = precos.pct_change().dropna()
    retorno_ibov = ibov.pct_change().dropna()

    resultados = []
    for col in retornos.columns:
        ret = retornos[col].dropna()
        df = pd.concat([ret, retorno_ibov], axis=1, join='inner').dropna()
        df.columns = ['Ret', 'Ibov']

        if len(df) < 2:
            beta, vol, ret_ano, sharpe = [np.nan] * 4
        else:
            var_ibov = np.var(df['Ibov'])
            beta = np.cov(df['Ret'], df['Ibov'])[0, 1] / var_ibov if var_ibov != 0 else np.nan
            vol = df['Ret'].std() * np.sqrt(252)
            ret_ano = (1 + df['Ret'].mean())**252 - 1
            sharpe = (ret_ano / vol) if vol > 0 else np.nan

        resultados.append({
            'Ticker': col, 'Volatilidade': vol, 'Retorno Anual': ret_ano,
            'Beta': beta, 'Sharpe': sharpe
        })
    return pd.DataFrame(resultados)
