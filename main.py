import streamlit as st #Importa a biblioteca streamlit. O st é um apelido para streamlit
from controller.controller import ControladorLSB #Importa a classe ControladorLSB que está dentro da pasta controller, que por sua vez está dentro do arquivo controller.py
import os #Importa o módulo OS que serve para interagir com o sistema operacional

#Função principal que inicializa o controlador e renderiza a página do Streamlit
def main(caminho: str) -> None:
    #chama o controlador responsável por lógica e visualização
    controlador = ControladorLSB(caminho)
    #se a coluna 'Ano' não existir mostrará erro
    controlador.modelo.criar_coluna_ano()

    #Barra lateral com filtros e opções. Sidebar
    st.sidebar.markdown("## ⚙️ Filtros e Opções")

    #Seleção de métrica para análise
    metrica = st.sidebar.selectbox(
        "Selecione uma métrica para análise:", controlador.modelo.metricas
    )

    #Título principal do dashboard e logo
    #Divide em duas colunas, uma com o logo e a outra com o título
    col1, col2 = st.columns([1, 3])

    with col1: #coluna 1
        st.image("assets/lsb_logo.png", width=120) #Logo

    with col2: #coluna 2
        st.title("Liga Super Basketball") #Título

    #Mostra os anos disponíveis e adiciona opção 'Todos'
    anos = list(controlador.modelo.df["Ano"].unique()) #acessa o dataframe, pega a coluna ano e escolhe os valores únicos e depois converte para uma lista
    anos_sorted = sorted(anos) #oredena a lista anos em ordem crescente
    anos_opcoes = ["Todos"] + anos_sorted #essa parte cria uma nova lista com a inserção de 'Todos' e depois adiciona os anos
    ano_selecionado = st.sidebar.radio("Selecione o ano:", anos_opcoes) #botão de seleção do tipo button na sidebar e guarda em 'ano_selecionado' o que foi escolhido pelo usuário

    #Filtro para escolher uma liga específica
    ligas = controlador.modelo.df["Liga"].unique().tolist() #acessa a coluna liga do dataframe, extrai os valores únicos e os converte em uma lista
    ligas_opcoes = ["Todas"] + ligas #cria uma lista de opções para exibir no selectbox , sendo a primeira opção 'Todas' e depois as ligas do banco de dados
    liga_selecionada = st.sidebar.selectbox("Filtrar por liga:", ligas_opcoes) #mostra um sidebar com 'Filtrar por liga:' e depois pega a liga selecionada e guarda em 'liga_selecionada'

    #Executa o controlador passando ano, métrica e liga selecionada
    controlador.executar(ano_selecionado, metrica, liga_selecionada)
#define a configuração inicial da página, verifica se o csv existe e então executa a função main()
if __name__ == "__main__":
    st.set_page_config(page_title="Analise LSB", page_icon="📊", layout="wide") #configurações da página do streamlit
    caminho = os.path.join(os.getcwd(), "assets", "lsb.csv")
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado em {caminho}")
    main(caminho)

