
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from core import strategies

def optimize_weights(prices, max_weight=0.40):
    # ... (código existente sem alterações) ...
    returns = prices.pct_change().dropna(); n_assets = returns.shape[1]
    expected_returns = returns.mean() * 252; cov_matrix = returns.cov() * 252
    def negative_sharpe(weights):
        p_return = np.sum(expected_returns * weights)
        p_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return - (p_return / p_vol) if p_vol > 0 else 0
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = tuple((0, max_weight) for _ in range(n_assets))
    initial_weights = np.array(n_assets * [1. / n_assets])
    result = minimize(negative_sharpe, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x / np.sum(result.x)

def calculate_performance_metrics(strategy_returns, benchmark_returns, risk_free_rate=0.0):
    # ... (código existente sem alterações) ...
    benchmark_returns = benchmark_returns.reindex(strategy_returns.index).ffill()
    annual_return = strategy_returns.mean() * 252
    annual_volatility = strategy_returns.std() * np.sqrt(252)
    sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility if annual_volatility > 0 else 0
    negative_returns = strategy_returns[strategy_returns < 0]; downside_deviation = negative_returns.std() * np.sqrt(252)
    sortino_ratio = (annual_return - risk_free_rate) / downside_deviation if downside_deviation > 0 else 0
    equity_curve = (1 + strategy_returns).cumprod()
    peak = equity_curve.cummax(); drawdown = (equity_curve - peak) / peak; max_drawdown = drawdown.min()
    cov_matrix = np.cov(strategy_returns.dropna(), benchmark_returns.dropna()); beta = cov_matrix[0, 1] / cov_matrix[1, 1]
    benchmark_annual_return = benchmark_returns.mean() * 252
    alpha = annual_return - (risk_free_rate + beta * (benchmark_annual_return - risk_free_rate))
    total_return_strategy = equity_curve.iloc[-1] - 1 if not equity_curve.empty else 0
    total_return_benchmark = (1 + benchmark_returns).cumprod().iloc[-1] - 1 if not benchmark_returns.empty else 0
    return {'Retorno Total (Estratégia)': total_return_strategy, 'Retorno Total (IBOV)': total_return_benchmark, 'Retorno Anualizado (Estratégia)': annual_return, 'Volatilidade Anual (Estratégia)': annual_volatility, 'Sharpe Ratio': sharpe_ratio, 'Sortino Ratio': sortino_ratio, 'Max Drawdown': max_drawdown, 'Beta (vs IBOV)': beta, 'Alpha (vs IBOV)': alpha}

# **CORREÇÃO**: Renomeando a função para 'run_backtest'
def run_backtest(prices, benchmark_prices, fundamental_df, score_weights, n_top_stocks=3):
    print(f"\n--- Iniciando Backtest (Top {n_top_stocks} Ações) ---")
    
    final_score = strategies.quantamental_strategy_score(prices, fundamental_df, score_weights)
    
    portfolio_returns = []
    dates = final_score.resample('ME').last().index
    for i in range(len(dates) - 1):
        start_date, end_date = dates[i], dates[i+1]
        current_score = final_score.asof(start_date)
        top_stocks = current_score.nlargest(n_top_stocks).index
        
        optimization_prices = prices.loc[:start_date].tail(126)
        valid_top_stocks = [s for s in top_stocks if s in optimization_prices.columns and not optimization_prices[s].isnull().all()]
        if len(valid_top_stocks) < 1: continue

        try:
            optimal_weights = optimize_weights(optimization_prices[valid_top_stocks], max_weight=0.40)
        except:
            optimal_weights = [1./len(valid_top_stocks)] * len(valid_top_stocks)
        
        period_returns = prices.pct_change().loc[start_date:end_date]
        portfolio_daily_returns = (period_returns[valid_top_stocks] * optimal_weights).sum(axis=1)
        portfolio_returns.append(portfolio_daily_returns)

    if not portfolio_returns:
        print("Não foi possível gerar retornos para o portfólio no backtest.")
        return None, pd.DataFrame()

    strategy_returns = pd.concat(portfolio_returns)
    benchmark_returns = benchmark_prices.pct_change().iloc[:,0]
    performance_summary = calculate_performance_metrics(strategy_returns, benchmark_returns)
    
    equity_curve = (1 + strategy_returns).cumprod()
    benchmark_equity = (1 + benchmark_returns).cumprod().reindex(equity_curve.index).ffill()
    plot_df = pd.DataFrame({'Estratégia Otimizada': equity_curve, 'Ibovespa': benchmark_equity}).dropna()
    
    print("Backtest concluído.")
    return performance_summary, plot_df
