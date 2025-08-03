import sqlite3
import pandas as pd
import os

DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'database')
DB_PATH = os.path.join(DB_DIR, 'dados.db')

def init_db():
    """Inicializa o banco de dados e cria as tabelas se não existirem."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela para armazenar dados fundamentalistas históricos
    # Adicionando colunas que podem estar faltando, com tipos de dados flexíveis
    base_cols = {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 'Ticker': 'TEXT', 'data_coleta': 'TEXT',
        'PL': 'REAL', 'PVP': 'REAL', 'Div_Yield': 'REAL', 'ROA': 'REAL',
        'ROE': 'REAL', 'ROIC': 'REAL', 'Patrim_Liq': 'REAL', 'FCO': 'REAL',
        'Lucro_Liquido': 'REAL', 'Div_Br_Patrim': 'REAL', 'Liq_Corrente': 'REAL',
        'Nro_Acoes': 'REAL', 'Marg_Bruta': 'REAL', 'Giro_Ativos': 'REAL', 'Setor': 'TEXT'
    }
    
    try:
        # Pega as colunas existentes
        cursor.execute("PRAGMA table_info(fundamentos_historico)")
        existing_cols = {row[1] for row in cursor.fetchall()}
    except sqlite3.OperationalError:
        existing_cols = set()

    if not existing_cols:
        # Cria a tabela se ela não existe
        cols_str = ", ".join([f'"{k}" {v}' for k, v in base_cols.items()])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS fundamentos_historico ({cols_str})")
    else:
        # Adiciona colunas que não existem
        for col, col_type in base_cols.items():
            if col not in existing_cols:
                try:
                    cursor.execute(f'ALTER TABLE fundamentos_historico ADD COLUMN "{col}" {col_type}')
                except sqlite3.OperationalError as e:
                    print(f"Aviso: Não foi possível adicionar a coluna {col}. Erro: {e}")

    conn.commit()
    conn.close()
    print(f"Banco de dados inicializado em: {DB_PATH}")

def save_to_db(df):
    """Salva um DataFrame de fundamentos no banco de dados, evitando duplicatas."""
    if df.empty:
        return
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Pega as colunas existentes no banco de dados
    cursor.execute("PRAGMA table_info(fundamentos_historico)")
    db_cols = {row[1] for row in cursor.fetchall()}
    
    # Filtra o DataFrame para conter apenas colunas que existem no DB
    df_cols = set(df.columns)
    valid_cols = list(db_cols.intersection(df_cols))
    df_to_save = df[valid_cols]

    # Insere os dados
    df_to_save.to_sql('fundamentos_historico', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    print(f"{len(df_to_save)} registros salvos no banco de dados.")

def load_latest_from_db(tickers_list):
    """Carrega os dados fundamentalistas mais recentes para cada ticker."""
    conn = sqlite3.connect(DB_PATH)
    query = f"""
        SELECT t1.*
        FROM fundamentos_historico t1
        INNER JOIN (
            SELECT Ticker, MAX(data_coleta) as MaxDate
            FROM fundamentos_historico
            WHERE Ticker IN ({','.join(['?']*len(tickers_list))})
            GROUP BY Ticker
        ) t2 ON t1.Ticker = t2.Ticker AND t1.data_coleta = t2.MaxDate
    """
    try:
        df = pd.read_sql_query(query, conn, params=tickers_list)
        print(f"{len(df)} registros mais recentes carregados do banco de dados.")
    except Exception as e:
        print(f"Erro ao carregar dados do DB: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
    return df

def get_historical_fundamentals(ticker):
    """Busca todos os dados históricos para um único ticker."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM fundamentos_historico WHERE Ticker = ? ORDER BY data_coleta ASC"
    try:
        df = pd.read_sql_query(query, conn, params=(ticker,))
    except Exception as e:
        print(f"Erro ao buscar histórico para {ticker}: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
    
    df['data_coleta'] = pd.to_datetime(df['data_coleta'])
    df = df.set_index('data_coleta')
    return df