import sqlite3
import pandas as pd
import os

DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'database')
DB_PATH = os.path.join(DB_DIR, 'dados.db')

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS fundamentos_historico (Ticker TEXT, data_coleta TEXT, PL REAL, PVP REAL, Div_Yield REAL, ROE REAL, Cres_Rec_5a REAL, Setor TEXT, ROIC REAL)")
    conn.close()

def save_to_db(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('fundamentos_historico', conn, if_exists='append', index=False)
    conn.close()

def load_latest_from_db(tickers_list):
    conn = sqlite3.connect(DB_PATH)
    try:
        query = f"SELECT * FROM fundamentos_historico WHERE Ticker IN ({','.join(['?']*len(tickers_list))})"
        df = pd.read_sql_query(query, conn, params=tickers_list)
        if df.empty: return pd.DataFrame()
        df['data_coleta'] = pd.to_datetime(df['data_coleta'])
        df = df.sort_values('data_coleta').drop_duplicates(subset=['Ticker'], keep='last')
    finally:
        conn.close()
    return df

# --- FUNÇÃO RESTAURADA ---
def get_historical_fundamentals(ticker):
    """Busca o histórico de fundamentos para um único ticker."""
    conn = sqlite3.connect(DB_PATH)
    try:
        query = "SELECT * FROM fundamentos_historico WHERE Ticker = ? ORDER BY data_coleta ASC"
        df = pd.read_sql_query(query, conn, params=(ticker,))
        if df.empty: return pd.DataFrame()
        df['data_coleta'] = pd.to_datetime(df['data_coleta'])
        df = df.set_index('data_coleta')
        return df
    finally:
        conn.close()

def get_historical_data_counts(tickers_list):
    return pd.DataFrame() # Simplificado por enquanto