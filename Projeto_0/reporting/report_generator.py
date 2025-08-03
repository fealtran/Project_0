
import pandas as pd
from datetime import datetime

# A função agora aceita 'backtest_summary' como o terceiro argumento
def generate_html_report(df_ranking, backtest_summary, output_dir):
    """
    Gera um relatório HTML completo, incluindo o resumo do backtest.
    """
    try:
        report_path = f'{output_dir}/Relatorio_Analise.html'
        
        # Converte a tabela de ranking para HTML
        html_table = df_ranking.to_html(classes='styled-table', index=False, justify='center', float_format='{:.2f}'.format)
        
        # Converte a tabela de resumo do backtest para HTML
        html_backtest_table = "<h3>Backtest não executado ou sem resultados.</h3>"
        if backtest_summary:
            summary_df = pd.DataFrame.from_dict(backtest_summary, orient='index', columns=['Valor'])
            # Formatação condicional para percentuais e números
            summary_df['Valor'] = summary_df['Valor'].apply(lambda x: f"{x:.2%}" if abs(x) < 5 else f"{x:.2f}")
            html_backtest_table = summary_df.to_html(classes='styled-table', justify='center', header=False)

        # Template HTML final
        html_template = f"""
        <html>
        <head>
            <title>Relatório de Análise Quantamental</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f0f2f6; color: #333; margin: 20px; }}
                h1, h2, h3 {{ color: #0e1117; text-align: center; }}
                .styled-table {{ border-collapse: collapse; margin: 25px auto; font-size: 0.9em; min-width: 700px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.1); border-radius: 8px; overflow: hidden; }}
                .styled-table thead tr {{ background-color: #0068c9; color: #ffffff; text-align: center; }}
                .styled-table th, .styled-table td {{ padding: 12px 15px; text-align: center; }}
                .styled-table tbody tr {{ border-bottom: 1px solid #dddddd; }}
                .styled-table tbody tr:nth-of-type(even) {{ background-color: #f3f3f3; }}
                .styled-table tbody tr:last-of-type {{ border-bottom: 2px solid #0068c9; }}
                .chart-container {{ text-align: center; margin-top: 40px; }}
                img {{ max-width: 90%; height: auto; margin: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                .footer {{ text-align: center; margin-top: 30px; font-size: 0.8em; color: #888; }}
            </style>
        </head>
        <body>
            <h1>Relatório de Análise Quantamental</h1>
            <p class="footer">Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            
            <h2>Ranking Final</h2>
            {html_table}
            
            <h2>Relatório de Performance do Backtest</h2>
            {html_backtest_table}

            <div class="chart-container">
                <h3>Performance da Estratégia vs. Ibovespa</h3>
                <img src="backtest_performance.png" alt="Gráfico de Backtest">
                
                <h3>Performance Comparativa dos Ativos</h3>
                <img src="comparative_performance.png" alt="Gráfico de Performance Comparativa">
            </div>
            
            <p class="footer">Fim do Relatório</p>
        </body>
        </html>
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        print(f"Relatório HTML completo salvo em: {report_path}")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o relatório HTML: {e}")
