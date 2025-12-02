from model.model import ModeloLSB
from view.view import VisualizacaoLSB

class ControladorLSB:
    """Controlador que faz a ponte entre o modelo de dados e a visualização"""

    def __init__(self, caminho_dados: str):
        # Inicializa modelo e view
        self.modelo = ModeloLSB(caminho_dados)
        self.visualizacao = VisualizacaoLSB()

    def executar(self, ano, metrica: str, liga_selecionada: str = "Todas") -> None:
        """Executa as consultas necessárias e delega a renderização à view.
        Recebe:
            - ano: valor selecionado pelo usuário
            - metrica: string com o nome da coluna métrica
            - liga_selecionada: filtro adicional por Liga"""
        # Dados filtrados por ano
        df_ano = self.modelo.obter_dados_por_ano(ano)

        # Se houver filtro por liga executa o código abauixo
        if liga_selecionada != "Todas" and liga_selecionada is not None:
            df_ano = df_ano[df_ano["Liga"] == liga_selecionada]

        # Top 10 equipes pela métrica
        top_df = df_ano.sort_values(metrica, ascending=False)[["Equipe", metrica]].head(10)

        # Média por equipe
        media_df = df_ano.groupby("Equipe")[[metrica]].mean().reset_index()

        # Série temporal de quantidade de equipes por ano
        serie_df = self.modelo.serie_temporal_ligas()

        # Chama a view para exibir tudo
        self.visualizacao.exibir_dashboard(df_ano, top_df, media_df, serie_df, metrica, ano)
