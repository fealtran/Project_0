
import pandas as pd

def quantamental_strategy_score(prices, fundamental_df, score_weights):
    """
    Calcula o score para uma estratégia quantamental, combinando fatores quantitativos
    históricos com os dados fundamentalistas mais recentes.
    Retorna um DataFrame de scores ao longo do tempo.
    """
    # Sinais Quantitativos Históricos
    returns_6m = prices.pct_change(periods=126)
    volatility_3m = prices.pct_change().rolling(window=63).std()
    
    score_momentum = returns_6m.rank(axis=1, ascending=True, pct=True)
    score_low_vol = (-volatility_3m).rank(axis=1, ascending=True, pct=True)

    # Sinais Fundamentalistas (Estáticos)
    fund_scores = fundamental_df.set_index('Ticker')
    # Usamos .get() com um default para evitar erros se a coluna não existir
    score_pl = fund_scores.get('Score_PL', pd.Series(0.5, index=fund_scores.index)).rank(ascending=False, pct=True)
    score_roe = fund_scores.get('Score_ROE', pd.Series(0.5, index=fund_scores.index)).rank(ascending=True, pct=True)
    score_dy = fund_scores.get('Score_DY', pd.Series(0.5, index=fund_scores.index)).rank(ascending=True, pct=True)
    score_pvp = fund_scores.get('Score_PVP', pd.Series(0.5, index=fund_scores.index)).rank(ascending=False, pct=True)

    # Combinação ponderada dos scores
    final_score = (
        score_momentum * score_weights.get('Score_Momentum', 0) +
        score_low_vol * score_weights.get('Score_Sharpe', 0) + 
        score_pl * score_weights.get('Score_PL', 0) +
        score_roe * score_weights.get('Score_ROE', 0) +
        score_dy * score_weights.get('Score_DY', 0) +
        score_pvp * score_weights.get('Score_PVP', 0)
    )
    
    return final_score
