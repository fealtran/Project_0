TICKER_LISTS = {
    "Bancos": ['ITUB4.SA', 'BBDC4.SA', 'BBAS3.SA', 'SANB11.SA', 'BPAC11.SA'],
    "Elétricas": ['ELET3.SA', 'CMIG4.SA', 'CPLE6.SA', 'TAEE11.SA', 'AURE3.SA'],
}
QVG_METRICS = {
    'Value': {'PL': {'ascending': False}, 'PVP': {'ascending': False}},
    'Quality': {'ROE': {'ascending': True}, 'Div_Yield': {'ascending': True}},
    'Growth': {'Cres_Rec_5a': {'ascending': True}}
}
DEFAULT_SCORE_WEIGHTS = {
    "PL": {"weight": 0.20, "ascending": False}, "PVP": {"weight": 0.20, "ascending": False},
    "ROE": {"weight": 0.30, "ascending": True}, "Div_Yield": {"weight": 0.20, "ascending": True},
    "Cres_Rec_5a": {"weight": 0.10, "ascending": True},
}
SECTOR_SPECIFIC_WEIGHTS = {
    "Intermediários Financeiros": {
        "PVP": {"weight": 0.40, "ascending": False}, "ROE": {"weight": 0.40, "ascending": True},
        "PL": {"weight": 0.10, "ascending": False}, "Div_Yield": {"weight": 0.10, "ascending": True},
    }
}