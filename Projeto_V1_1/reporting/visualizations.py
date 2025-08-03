import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_price_and_mavg(prices_df, ticker):
    if ticker not in prices_df.columns: return go.Figure()
    df = pd.DataFrame(prices_df[ticker])
    df.columns = ['Preço']
    df['MA50'] = df['Preço'].rolling(window=50).mean()
    df['MA200'] = df['Preço'].rolling(window=200).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Preço'], mode='lines', name='Preço'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], mode='lines', name='MME 50d'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA200'], mode='lines', name='MME 200d'))
    fig.update_layout(title=f'Preço de Fechamento - {ticker}', template='plotly_white')
    return fig

# --- FUNÇÃO RESTAURADA ---
def plot_historical_fundamentals(historical_df, ticker):
    """Plota a evolução histórica dos principais indicadores fundamentalistas."""
    if historical_df.empty or len(historical_df) < 2:
        return go.Figure().update_layout(title_text=f"Dados históricos insuficientes para gerar gráfico para {ticker}.")
    
    metrics_to_plot = ['PL', 'PVP', 'Div_Yield', 'ROE']
    available_metrics = [m for m in metrics_to_plot if m in historical_df.columns]
    
    if not available_metrics:
        return go.Figure().update_layout(title_text=f"Nenhuma métrica histórica disponível para {ticker}")

    fig = px.line(historical_df, x=historical_df.index, y=available_metrics,
                  title=f'Evolução dos Fundamentos - {ticker}', markers=True)
    fig.update_layout(template='plotly_white', legend_title_text='Indicadores')
    return fig

def plot_rolling_volatility(precos, ticker): return go.Figure() # Simplificado
def plot_radar_chart(ticker_data, sector_avg_data, ticker): return go.Figure() # Simplificado