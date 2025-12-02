import pandas as pd

class ModeloLSB:
    """Classe responsável por carregar os dados e fornecer métodos de agregação"""

    def __init__(self, caminho_dados: str):
        # Tratamento de erro. Tenta carregar o CSV, caso não exista lança FileNotFoundError com mensagem amigável
        try:
            self.df = pd.read_csv(caminho_dados)
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo não encontrado em {caminho_dados}")

        # Mapeamento de colunas, aplica apenas se os códigos existirem no csv
        mapa = {
            'J': 'Jogos','PTS': 'Pontos','PTSC': 'Pontos Contra',
            '2PTST': '2 Pontos Tentados','2PTSC': '2 Pontos Convertidos',
            'P2PTS': 'Percentual de 2 Pontos','3PTST': '3 Pontos Tentados',
            '3PTSC': '3 Pontos Convertidos','P3PTS': 'Percentual de 3 Pontos',
            'LLT': 'Lances Livres Tentados','LLC': 'Lances Livres Convertidos',
            'PLL': 'Percentual de Lances Livres','TREB': 'Total de Rebotes',
            'REBD': 'Rebotes Defensivos','REBO': 'Rebotes Ofensivos',
            'ASS': 'Assistências','RB': 'Roubos de Bolas','T': 'Tocos',
            'TF': 'Total de Faltas','ERR': 'Erros','EFF': 'Eficiência'
        }
        presentes = {k:v for k,v in mapa.items() if k in self.df.columns}
        self.df.rename(columns=presentes, inplace=True)

        # Se não existir a coluna Liga, cria uma coluna padrão para que possam serem feitos filtros
        if 'Liga' not in self.df.columns:
            self.df['Liga'] = 'Geral'

        # Lista de métricas possíveis
        possiveis_metricas = [
            "Jogos","Pontos","Pontos Contra","2 Pontos Tentados","2 Pontos Convertidos","Percentual de 2 Pontos","3 Pontos Tentados","3 Pontos Convertidos",
            "Percentual de 3 Pontos","Lances Livres Tentados","Lances Livres Convertidos","Percentual de Lances Livres","Total de Rebotes","Rebotes Defensivos","Rebotes Ofensivos","Assistências",
            "Roubos de Bolas","Tocos","Total de Faltas","Erros","Eficiência"
        ]
        self.metricas = [m for m in possiveis_metricas if m in self.df.columns]

    def criar_coluna_ano(self):
        """Valida se o banco de dados possui a coluna Ano. Se não tiver, mostra ValueError"""
        if "Ano" not in self.df.columns:
            raise ValueError("O dataset não possui coluna 'Ano'")

    def obter_dados_por_ano(self, ano):
        """Retorna os dados filtrados pelo ano. Se ano for Todos ou None retorna todo o banco de dados"""
        if ano == "Todos" or ano is None:
            return self.df.copy()
        # Permite ano como string ou int
        return self.df[self.df["Ano"] == ano].copy()

    def calcular_media_por_equipe(self, ano, coluna: str):
        """Calcula a média da coluna por equipe no ano informado"""
        df = self.obter_dados_por_ano(ano)
        return df.groupby("Equipe")[[coluna]].mean().reset_index()

    def calcular_top_equipes(self, ano, coluna: str, top_n: int = 10):
        """Retorna o top N equipes ordenadas pela coluna"""
        df = self.obter_dados_por_ano(ano)
        df_ordenado = df.sort_values(by=coluna, ascending=False)
        return df_ordenado[["Equipe", coluna]].head(top_n)

    def serie_temporal_ligas(self):
        """Mostra a quuantidade de equipes por ano"""
        return self.df.groupby("Ano")["Equipe"].count().reset_index(name="Quantidade")
