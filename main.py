import streamlit as st
from controller.controller import ControladorLSB
import os

# Função principal que inicializa o controlador e renderiza a página Streamlit
def main(caminho: str) -> None:
    # Instancia o controlador responsável por lógica e visualização
    controlador = ControladorLSB(caminho)
    # Valida a presença da coluna 'Ano', caso não exista, mostrará erro
    controlador.modelo.criar_coluna_ano()

    # Barra lateral com filtros e opções
    st.sidebar.markdown("## ⚙️ Filtros e Opções")

    # Seleção de métrica para análise
    metrica = st.sidebar.selectbox(
        "Selecione uma métrica para análise:", controlador.modelo.metricas
    )

    # Título principal do dashboard e logo
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("assets/lsb_logo.png", width=120)

    with col2:
        st.title("Liga Super Basketball")

    # Obtem anos disponíveis e adiciona opção 'Todos'
    anos = list(controlador.modelo.df["Ano"].unique())
    anos_sorted = sorted(anos)
    anos_opcoes = ["Todos"] + anos_sorted
    ano_selecionado = st.sidebar.radio("Selecione o ano:", anos_opcoes)

    # Filtro para escolher uma liga específica
    ligas = controlador.modelo.df["Liga"].unique().tolist()
    ligas_opcoes = ["Todas"] + ligas
    liga_selecionada = st.sidebar.selectbox("Filtrar por liga:", ligas_opcoes)

    # Executa o controlador passando ano, métrica e liga selecionada
    controlador.executar(ano_selecionado, metrica, liga_selecionada)

if __name__ == "__main__":
    st.set_page_config(page_title="Analise LSB", page_icon="📊", layout="wide")
    caminho = os.path.join(os.getcwd(), "assets", "lsb.csv")
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado em {caminho}")
    main(caminho)
