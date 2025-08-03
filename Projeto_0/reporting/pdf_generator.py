
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Análise Quantamental', 0, 1, 'C')
        self.set_font('Arial', '', 8)
        self.cell(0, 5, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
        
    def dataframe_to_table(self, df, col_widths=None):
        self.set_font('Arial', 'B', 8)
        # Header
        for i, col in enumerate(df.columns):
            width = col_widths[i] if col_widths else 180 / len(df.columns)
            self.cell(width, 7, str(col), 1, 0, 'C')
        self.ln()
        # Data
        self.set_font('Arial', '', 8)
        for index, row in df.iterrows():
            for i, item in enumerate(row):
                width = col_widths[i] if col_widths else 180 / len(df.columns)
                if isinstance(item, float): item = f"{item:.2f}"
                self.cell(width, 6, str(item), 1, 0, 'C')
            self.ln()
        self.ln(5)

def create_pdf_report(results, output_dir):
    """Gera um relatório PDF completo com todos os resultados da análise."""
    pdf = PDF()
    
    # Extrai os dados do dicionário de resultados
    ranking_df = results["ranking_final"]
    alerts = results["alerts"]
    backtest_summary = results["backtest_summary"]
    
    # --- PÁGINA 1: CAPA E RANKING ---
    pdf.add_page()
    pdf.chapter_title('Ranking Final')
    pdf.dataframe_to_table(ranking_df[['Ticker', 'Score', 'PL', 'ROE', 'Div. Yield']].head(10))
    
    pdf.chapter_title('Alertas e Insights Principais')
    pdf.set_font('Arial', '', 10)
    for alert in alerts:
        pdf.multi_cell(0, 5, alert.encode('latin-1', 'replace').decode('latin-1'))
    
    # --- PÁGINA 2: BACKTEST ---
    pdf.add_page()
    pdf.chapter_title('Relatório de Performance do Backtest')
    if backtest_summary:
        summary_df = pd.DataFrame.from_dict(backtest_summary, orient='index', columns=['Valor'])
        summary_df.index.name = "Métrica"
        summary_df.reset_index(inplace=True)
        pdf.dataframe_to_table(summary_df, col_widths=[120, 60])
    
    chart_path = os.path.join(output_dir, 'backtest_performance.png')
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=15, w=180)
    
    # --- PÁGINAS 3+: TEARSHEETS INDIVIDUAIS ---
    from reporting import visualizations as viz
    from core import database_manager as dbm
    from analysis import fundamental as funda_analysis
    
    for ticker in ranking_df['Ticker']:
        pdf.add_page()
        pdf.chapter_title(f"Análise Individual: {ticker}")
        
        # Gera e insere gráficos
        price_chart = viz.plot_price_and_indicators(results['prices'], ticker, output_dir, f"{ticker}_price.png")
        if price_chart: pdf.image(os.path.join(output_dir, f"{ticker}_price.png"), x=15, w=180)
        
        history_df = dbm.load_full_history_for_ticker(ticker)
        if not history_df.empty and len(history_df) > 1:
            roe_chart = viz.plot_historical_fundamental(history_df, 'ROE', ticker)
            pl_chart = viz.plot_historical_fundamental(history_df, 'PL', ticker)
            
            if roe_chart:
                roe_chart.savefig(os.path.join(output_dir, f"{ticker}_roe.png"))
                pdf.image(os.path.join(output_dir, f"{ticker}_roe.png"), x=15, y=pdf.get_y()+5, w=90)
            if pl_chart:
                pl_chart.savefig(os.path.join(output_dir, f"{ticker}_pl.png"))
                pdf.image(os.path.join(output_dir, f"{ticker}_pl.png"), x=105, y=pdf.get_y()+5, w=90)

    # Salva o PDF
    pdf_path = os.path.join(output_dir, "Relatorio_Completo.pdf")
    pdf.output(pdf_path)
    print(f"Relatório PDF completo salvo em: {pdf_path}")
