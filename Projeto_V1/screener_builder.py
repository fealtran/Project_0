import pandas as pd
import main
from utils import b3_tickers
import time
import os

def build_screener_database(batch_size=20):
    start_time = time.time()
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    screener_file_path = os.path.join(output_dir, "screener_database.parquet")

    all_tickers = b3_tickers.get_b3_tickers()
    if not all_tickers:
        print("Não foi possível obter a lista de tickers. Abortando."); return

    all_results = []
    failed_batches = []
    
    print(f"Iniciando análise para {len(all_tickers)} tickers em lotes de {batch_size}...")
    
    for i in range(0, len(all_tickers), batch_size):
        batch = all_tickers[i:i + batch_size]
        current_batch_num = i//batch_size + 1
        total_batches = (len(all_tickers)//batch_size)+1
        
        print(f"\n--- Processando Lote {current_batch_num}/{total_batches} ({len(batch)} tickers) ---")
        
        try:
            results = main.run_analysis(batch)
            if results and "ranking" in results and not results["ranking"].empty:
                all_results.append(results["ranking"])
                print(f"Lote {current_batch_num} concluído com sucesso.")
        except Exception as e:
            print(f"ERRO CRÍTICO ao processar o lote {current_batch_num}: {e}")
            failed_batches.append(batch)

    if all_results:
        final_df = pd.concat(all_results, ignore_index=True).dropna(subset=['Ticker']).drop_duplicates(subset=['Ticker'], keep='last')
        print(f"\nAnálise concluída. Salvando {len(final_df)} resultados em {screener_file_path}...")
        final_df.to_parquet(screener_file_path, index=False)
        print("Base de dados do screener construída com sucesso!")
        if failed_batches:
            print(f"Houve falha no processamento de {len(failed_batches)} lotes.")
    else:
        print("Nenhum resultado foi gerado. A base de dados não foi criada.")

    end_time = time.time()
    print(f"Tempo total de execução: {((end_time - start_time) / 60):.2f} minutos.")

if __name__ == "__main__":
    build_screener_database()