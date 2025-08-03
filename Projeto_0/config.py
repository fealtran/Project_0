# Listas de tickers para análise
TICKER_LISTS = {
    "Bancos": ['ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA', 'SANB11.SA', 'BPAC11.SA'],
    "Varejo": ['MGLU3.SA', 'BHIA3.SA', 'LREN3.SA', 'CEAB3.SA', 'ARZZ3.SA'],
    "Elétricas": ['ELET3.SA', 'CMIG4.SA', 'CPLE6.SA', 'TAEE11.SA', 'AURE3.SA'],
    "Siderurgia": ['GGBR4.SA', 'USIM5.SA', 'CSNA3.SA', 'GOAU4.SA'],
}

# Pesos padrão para o Score Flexível
# 'ascending': True significa "quanto maior, melhor". False significa "quanto menor, melhor".
SCORE_WEIGHTS = {
    # --- Valuation (Peso Total: 0.25) ---
    "PL":               {"weight": 0.15, "ascending": False}, # Menor é melhor
    "PVP":              {"weight": 0.10, "ascending": False}, # Menor é melhor

    # --- Rentabilidade (Peso Total: 0.35) ---
    "ROE":              {"weight": 0.20, "ascending": True},  # Maior é melhor
    "F_Score":          {"weight": 0.15, "ascending": True},  # Maior é melhor (Piotroski F-Score)

    # --- Dividendos (Peso Total: 0.10) ---
    "Div_Yield":        {"weight": 0.10, "ascending": True},  # Maior é melhor

    # --- Risco/Retorno Quant (Peso Total: 0.20) ---
    "Sharpe":           {"weight": 0.15, "ascending": True},  # Maior é melhor
    "Volatilidade":     {"weight": 0.05, "ascending": False}, # Menor é melhor

    # --- Momentum (Peso Total: 0.10) ---
    "Momentum_Score":   {"weight": 0.10, "ascending": True},  # Maior é melhor
}

# Diretório de output para relatórios e gráficos
OUTPUT_DIR = "/content/drive/MyDrive/Projeto_0/output"