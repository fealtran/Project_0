import streamlit as st
import main, screener, sector_dashboard, market_quadrant, my_dashboard
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
st.set_page_config(page_title="Plataforma de Análise de Ativos", page_icon="📈", layout="wide")
PAGES = {
    "Meu Dashboard (Watchlist)": my_dashboard, "Análise de Ativo Individual": main,
    "Stock Screener": screener, "Dashboard Setorial": sector_dashboard,
    "Quadrante de Mercado": market_quadrant
}
def run():
    st.sidebar.title('Ferramentas')
    selection = st.sidebar.radio("Ir para", list(PAGES.keys()))
    page = PAGES[selection]
    page.run_app()
if __name__ == "__main__": run()