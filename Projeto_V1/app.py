import streamlit as st
# ... (demais imports) ...

def render_stock_screener_page(full_df):
    st.header("Stock Screener Avançado")
    # ... (código dos filtros existentes) ...
    
    with st.sidebar:
        # --- NOVOS FILTROS DE TENDÊNCIA ---
        st.subheader("Filtros de Tendência")
        
        # Verifica se as colunas de tendência existem antes de criar os sliders
        if 'ROE_CAGR_3A' in full_df.columns:
            min_roe_cagr = st.slider("Cresc. Anual Mín. do ROE (%)", -50.0, 100.0, -50.0, 1.0)
        else:
            min_roe_cagr = -50.0 # Valor padrão se a coluna não existir
        
        if 'PL_Tendencia' in full_df.columns:
            tendencia_pl = st.selectbox("Tendência do P/L", ["Qualquer", "Positiva (ficando mais caro)", "Negativa (ficando mais barato)"])
        else:
            tendencia_pl = "Qualquer" # Valor padrão

    # ... (lógica de filtragem, agora incluindo os novos filtros) ...
    
    if 'ROE_CAGR_3A' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['ROE_CAGR_3A'].fillna(-1) >= (min_roe_cagr / 100)]
    
    if 'PL_Tendencia' in filtered_df.columns:
        if tendencia_pl == "Positiva (ficando mais caro)":
            filtered_df = filtered_df[filtered_df['PL_Tendencia'] > 0]
        elif tendencia_pl == "Negativa (ficando mais barato)":
            filtered_df = filtered_df[filtered_df['PL_Tendencia'] < 0]
            
    # ... (o resto da exibição do dataframe) ...