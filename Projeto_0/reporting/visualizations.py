import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot_price_and_mavg(prices_df, ticker, output_dir):
    """Gera um gráfico interativo de preços e médias móveis com Plotly."""
    if ticker not in prices_df.columns:
        return go.Figure()

    df = pd.DataFrame(prices_df[ticker])
    df.columns = ['Preço']
    df['MA50'] = df['Preço'].rolling(window=50).mean()
    df['MA200'] = df['Preço'].rolling(window=200).mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Preço'], mode='lines', name='Preço'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], mode='lines', name='Média Móvel 50d'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA200'], mode='lines', name='Média Móvel 200d'))

    fig.update_layout(
        title=f'Preço de Fechamento e Médias Móveis - {ticker}',
        xaxis_title='Data',
        yaxis_title='Preço (R$)',
        template='plotly_white'
    )
    return fig

def plot_historical_fundamentals(historical_df, ticker):
    """
    Gera gráficos de linha para a evolução de múltiplos indicadores fundamentalistas.
    """
    if historical_df.empty:
        return go.Figure().update_layout(title_text=f"Não há dados históricos suficientes para {ticker}")

    # Métricas para plotar
    metrics_to_plot = ['PL', 'PVP', 'Div_Yield', 'ROE']
    
    # Filtra colunas existentes
    available_metrics = [m for m in metrics_to_plot if m in historical_df.columns]
    
    if not available_metrics:
        return go.Figure().update_layout(title_text=f"Nenhuma métrica histórica disponível para {ticker}")

    fig = px.line(
        historical_df, 
        x=historical_df.index, 
        y=available_metrics,
        facet_row="variable",  # Cria um subplot para cada métrica
        title=f'Evolução dos Fundamentos - {ticker}',
        labels={"value": "Valor", "data_coleta": "Data"},
        height=600
    )
    
    fig.update_yaxes(matches=None) # Permite que cada subplot tenha seu próprio eixo Y
    fig.update_layout(template='plotly_white', showlegend=False)
    
    return fig

def plot_backtest_performance(performance_df, output_dir):
    """Gera um gráfico interativo da performance do backtest."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=performance_df.index, y=performance_df['Estratégia'], mode='lines', name='Estratégia'))
    fig.add_trace(go.Scatter(x=performance_df.index, y=performance_df['IBOV'], mode='lines', name='IBOV'))
    
    fig.update_layout(
        title='Performance do Backtest: Estratégia vs. IBOV',
        xaxis_title='Data',
        yaxis_title='Retorno Acumulado',
        template='plotly_white'
    )
    return fig