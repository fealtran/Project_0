
import pandas as pd
import numpy as np

def calculate_momentum_score(prices):
    """
    Calcula um score de momentum para cada ticker baseado nos retornos
    de 1, 3, 6 e 12 meses, ponderados.
    """
    ret_1m = prices.pct_change(periods=21).iloc[-1]
    ret_3m = prices.pct_change(periods=63).iloc[-1]
    ret_6m = prices.pct_change(periods=126).iloc[-1]
    ret_12m = prices.pct_change(periods=252).iloc[-1]
    momentum_df = pd.DataFrame({'Ret_1M': ret_1m, 'Ret_3M': ret_3m,'Ret_6M': ret_6m, 'Ret_12M': ret_12m}).fillna(0)
    weights = {'1M': 0.4, '3M': 0.3, '6M': 0.2, '12M': 0.1}
    momentum_df['Score_Momentum'] = (momentum_df['Ret_1M'].rank(pct=True) * weights['1M'] + momentum_df['Ret_3M'].rank(pct=True) * weights['3M'] + momentum_df['Ret_6M'].rank(pct=True) * weights['6M'] + momentum_df['Ret_12M'].rank(pct=True) * weights['12M'])
    momentum_df.reset_index(inplace=True); momentum_df.rename(columns={'index': 'Ticker'}, inplace=True)
    print("Score de Momentum calculado."); return momentum_df[['Ticker', 'Score_Momentum']]

def calculate_max_drawdown(prices):
    """Calcula o Maximum Drawdown para cada ticker."""
    cumulative_returns = (1 + prices.pct_change()).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()
    max_drawdown_df = max_drawdown.to_frame(name='Max_Drawdown').reset_index()
    max_drawdown_df.rename(columns={'index': 'Ticker'}, inplace=True)
    print("Maximum Drawdown calculado."); return max_drawdown_df

def calculate_rolling_metrics(prices, benchmark_prices, window=252):
    """Calcula as métricas móveis (Beta e Volatilidade)."""
    returns = prices.pct_change()
    benchmark_returns = benchmark_prices.pct_change().iloc[:, 0]
    rolling_vol = returns.rolling(window=window).std() * np.sqrt(252)
    last_rolling_vol = rolling_vol.iloc[-1].to_frame(name=f'Vol_{window}d')
    all_betas = {}
    for ticker in returns.columns:
        stock_returns = returns[ticker]
        df_pair = pd.concat([stock_returns, benchmark_returns], axis=1).dropna(); df_pair.columns = ['Stock', 'Benchmark']
        if len(df_pair) < window:
            all_betas[ticker] = None; continue
        rolling_cov = df_pair['Stock'].rolling(window=window).cov(df_pair['Benchmark'])
        rolling_var = df_pair['Benchmark'].rolling(window=window).var()
        beta_series = rolling_cov / rolling_var
        valid_betas = beta_series.dropna()
        if not valid_betas.empty: all_betas[ticker] = valid_betas.iloc[-1]
        else: all_betas[ticker] = None
    last_rolling_beta = pd.Series(all_betas).to_frame(name=f'Beta_{window}d')
    last_rolling_vol.reset_index(inplace=True); last_rolling_beta.reset_index(inplace=True)
    last_rolling_vol.rename(columns={'index': 'Ticker'}, inplace=True); last_rolling_beta.rename(columns={'index': 'Ticker'}, inplace=True)
    results_df = pd.merge(last_rolling_vol, last_rolling_beta, on='Ticker', how='outer')
    print(f"Métricas Móveis para janela de {window} dias calculadas."); return results_df

def calculate_macro_correlation(prices, macro_data):
    """Calcula a correlação dos retornos dos ativos com variáveis macroeconômicas."""
    if prices.empty or macro_data.empty:
        return pd.DataFrame(columns=['Ticker', 'SELIC', 'IPCA'])

    returns = prices.pct_change().dropna()
    macro_changes = macro_data.diff().dropna()
    
    combined_df = pd.merge(returns, macro_changes, left_index=True, right_index=True, how='inner')
    
    if combined_df.empty or len(combined_df) < 2:
        print("Não há dados suficientes para calcular a correlação macro.")
        return pd.DataFrame(columns=['Ticker', 'SELIC', 'IPCA'])

    correlation_matrix = combined_df.corr()
    
    macro_correlation = correlation_matrix.loc[prices.columns, macro_data.columns]
    
    macro_correlation.reset_index(inplace=True)
    macro_correlation.rename(columns={'index': 'Ticker'}, inplace=True)

    print("Correlação com variáveis macro calculada.")
    return macro_correlation
