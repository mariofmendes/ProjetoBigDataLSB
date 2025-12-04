import streamlit as st #Importa a biblioteca streamlit. O st é um apelido para streamlit
import plotly.express as px #Importa do plotly express e cria uma apelido 'px'
import pandas as pd #importa a biblioteca pandas e cria um apelido 'pd'

class VisualizacaoLSB:
    #Monta a parte dos gráficos e tabelas no Streamlit e plotly

    def exibir_dashboard(self, df_filtrado, top_df, media_df, serie_df, metrica, ano_selecionado):
        
        st.markdown(f"# Liga Super Basketball - Métrica: **{metrica}**") #título com markdown

        col1, col2 = st.columns(2) #cria duas colunas 

        #Cria o gráfico das top 10 equipes
        fig_top = px.bar(top_df, x="Equipe", y=metrica, title=f"Top 10 equipes em {metrica}")
        col1.plotly_chart(fig_top, use_container_width=True)

        #Gráfico de barras da média por equipe
        fig_media = px.bar(media_df, x="Equipe", y=metrica, title=f"Média por equipe ({metrica})")
        col2.plotly_chart(fig_media, use_container_width=True)

        #Mostra contagem de quantas ligas existem no ano selecionado
        #Se o usuário escolher Todos, a contagem será feita sobre todo o banco de dados
        if ano_selecionado == "Todos" or ano_selecionado is None: #verifica o ano selecionado
            ligas_no_ano = df_filtrado["Liga"].nunique() #verifica quantas ligas diferentes existem e guarda em 'ligas_no_ano'
            st.markdown(f"## 🔢 Contagem de ligas (Todos os anos): **{ligas_no_ano}**") #mostra a quantidade de ligas
        else: #condição para um ano específico for selecionado
            ligas_no_ano = df_filtrado["Liga"].nunique()
            st.markdown(f"## 🔢 Contagem de ligas em {ano_selecionado}: **{ligas_no_ano}**") #mostra a quantidade de ligas para o ano escolhido

        #Filtro de visualização: Dispersão por liga, dispersão por equipe, gráficos de pizza
        st.markdown("## 🔵 Dispersão por Liga (todas as ligas do ano selecionado)")
        if df_filtrado.empty:
            st.write("Nenhum dado disponível para o filtro selecionado.")
        else:
            #Gráfico de dispersão com cada ponto representando uma equipe; x = Liga, y = métrica
            fig_disp_liga = px.strip(df_filtrado, x="Liga", y=metrica, hover_data=["Equipe"], title="Dispersão por Liga")
            st.plotly_chart(fig_disp_liga, use_container_width=True)

            #Gráfico de dispersão com todas as equipes do ano selecionado (x = Equipe, y = métrica)
            st.markdown("## 🔵 Dispersão por Equipe (todas as equipes do ano selecionado)")
            fig_disp_equipe = px.scatter(df_filtrado, x="Equipe", y=metrica, hover_name="Equipe", title="Dispersão por Equipe")
            st.plotly_chart(fig_disp_equipe, use_container_width=True)

            #Gráfico de pizza: Total da métrica por Liga
            st.markdown("## 🥧 Distribuição da métrica por Liga (pizza)")
            soma_por_liga = df_filtrado.groupby("Liga")[metrica].sum().reset_index(name="Total")
            if not soma_por_liga.empty:
                fig_pizza_pontos = px.pie(soma_por_liga, names="Liga", values="Total", title=f"Total de {metrica} por Liga")
                st.plotly_chart(fig_pizza_pontos, use_container_width=True)
            else:
                st.write("Nenhum dado para construir o gráfico de pizza de pontos.")

            #Gráfico de pizza: Quantidade de equipes por Liga
            st.markdown("## 🥧 Quantidade de Equipes por Liga (pizza)")
            contagem_por_liga = df_filtrado.groupby("Liga")["Equipe"].nunique().reset_index(name="QuantidadeEquipes")
            if not contagem_por_liga.empty:
                fig_pizza_qtd = px.pie(contagem_por_liga, names="Liga", values="QuantidadeEquipes", title="Quantidade de equipes por Liga")
                st.plotly_chart(fig_pizza_qtd, use_container_width=True)
            else:
                st.write("Nenhum dado para construir o gráfico de pizza de quantidades.")

        #Seção final: Exibe todos os dados do banco de dados filtrados
        st.markdown("## 🗃️ Banco de Dados (registros filtrados)")
        st.dataframe(df_filtrado.reset_index(drop=True))

