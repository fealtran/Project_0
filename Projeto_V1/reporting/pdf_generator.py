import pandas as pd
from fpdf import FPDF
import plotly.graph_objects as go
import os

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Relatório de Análise de Ativo', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(ticker_data, charts, output_dir="output"):
    print(f"Gerando relatório PDF para {ticker_data['Ticker'].iloc[0]}...")
    os.makedirs(output_dir, exist_ok=True)
    pdf = PDF()
    pdf.add_page()
    ticker = ticker_data['Ticker'].iloc[0]
    
    pdf.set_font('Arial', 'B', 18); pdf.cell(0, 10, f"Análise Completa - {ticker}", 0, 1, 'L')
    pdf.set_font('Arial', 'B', 12); pdf.cell(0, 10, "Veredito do Analista (IA):", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, ticker_data['Veredito_IA'].iloc[0].encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)

    pdf.set_font('Arial', 'B', 12); pdf.cell(0, 10, "Principais Indicadores:", 0, 1)
    pdf.set_font('Arial', '', 9); col_width = pdf.w / 4.4; line_height = pdf.font_size * 1.8
    
    key_metrics = {
        "Preço Atual": "R$ {:.2f}", "P/L": "{:.2f}", "P/VP": "{:.2f}", "Div. Yield": "{:.2%}",
        "ROE": "{:.2%}", "Upside (Gordon)": "{:.2%}", "Quality Score": "{:.2%}",
        "Value Score": "{:.2%}", "Growth Score": "{:.2%}", "Sortino Ratio": "{:.2f}"
    }
    
    i = 0
    for label, fmt in key_metrics.items():
        col_name = label.replace(" (Gordon)", "_Gordon").replace(" ", "_")
        if col_name in ticker_data.columns:
            value = ticker_data[col_name].iloc[0]
            if pd.notna(value):
                pdf.cell(col_width, line_height, label, border=1)
                pdf.cell(col_width, line_height, fmt.format(value), border=1, ln=i % 2 != 0)
                i += 1
    pdf.ln(10)
    
    chart_paths = []
    for chart_name, chart_fig in charts.items():
        if chart_fig and isinstance(chart_fig, go.Figure):
            path = os.path.join(output_dir, f"temp_{ticker}_{chart_name}.png")
            chart_fig.write_image(path, width=800, height=450, scale=2); chart_paths.append((chart_name.replace('_', ' ').title(), path))

    for title, path in chart_paths:
        if pdf.get_y() > 180: pdf.add_page() # Adiciona nova página se não houver espaço
        pdf.set_font('Arial', 'B', 12); pdf.cell(0, 10, f"Gráfico: {title}", 0, 1)
        pdf.image(path, x=None, y=None, w=180); pdf.ln(5)

    pdf_output_path = os.path.join(output_dir, f"Relatorio_{ticker}.pdf")
    pdf.output(pdf_output_path)
    print(f"Relatório salvo em: {pdf_output_path}")
    return pdf_output_path