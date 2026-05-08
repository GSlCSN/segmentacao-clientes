import pandas as pd

# lê os dois arquivos csv e transforma em DataFrame
clientes_df = pd.read_csv("clientes.csv")
pedidos_df = pd.read_csv("pedidos.csv")

# ======= Parte de Clientes =======

# remove linhas onde o cliente_id aparece mais de uma vez — mantém só a primeira
clientes_df = clientes_df.drop_duplicates(subset=["cliente_id"])

# converte a coluna de texto "2023-06-10" pra um objeto de data real
# sem isso o pandas não consegue comparar datas
clientes_df["data_cadastro"] = pd.to_datetime(clientes_df["data_cadastro"])

# filtra só clientes cadastrados depois de 2023 — remove a Helena (2021)
clientes_df = clientes_df[clientes_df["data_cadastro"] >= "2023-01-10"]

# preenche as células vazias da coluna genero com "F"
clientes_df["genero"] = clientes_df["genero"].fillna("F")

# substitui variações do mesmo valor por um padrão único
# fillna não resolve isso porque não são células vazias, são texto errado
clientes_df["genero"] = clientes_df["genero"].replace(["f","feminino","Feminino"], "F")

# reorganiza os índices pra ficarem 0,1,2... depois das remoções
clientes_df = clientes_df.reset_index(drop=True)

# ======= Parte de Pedidos =======

# mantém só pedidos entregues — cancelado não virou receita real
pedidos_df = pedidos_df[pedidos_df["status"] == "entregue"]

# converte texto pra data real — mesmo conceito dos clientes
pedidos_df["data_pedido"] = pd.to_datetime(pedidos_df["data_pedido"])

# remove pedidos anteriores a 2023 — elimina o outlier de 2022
pedidos_df = pedidos_df[pedidos_df["data_pedido"] >= "2023-01-01"]

# tenta preencher valor nulo com a média das outras compras do mesmo cliente
# transform("mean") calcula a média por grupo e aplica na mesma posição
pedidos_df["valor_total"] = pedidos_df["valor_total"].fillna(
    pedidos_df.groupby("cliente_id")["valor_total"].transform("mean")
)

# plano B — se o cliente tinha só uma compra e era nula, usa a média geral
pedidos_df["valor_total"] = pedidos_df["valor_total"].fillna(pedidos_df["valor_total"].mean())

# ======= Parte Final =======

# junta os dois DataFrames pelo cliente_id
# how="left" garante que todos os clientes aparecem mesmo sem pedido
df_final = pd.merge(clientes_df, pedidos_df, on="cliente_id", how="left")

# pega a data do pedido mais recente de cada cliente
# groupby agrupa por cliente, max() pega a data maior (mais recente)
pedido_recente = df_final.groupby("cliente_id")["data_pedido"].max()

# subtrai a data mais recente de "hoje" (2024-05-01)
# .dt.days extrai só o número inteiro de dias — sem isso ficaria "3 days"
pedido_recente = (pd.Timestamp("2024-05-01") - pedido_recente).dt.days

# soma todo o valor gasto por cliente no período inteiro
valor_monetário = df_final.groupby("cliente_id")["valor_total"].sum()

# conta quantos pedidos cada cliente fez — frequência de compra
frequencia_compra = df_final.groupby("cliente_id")["nome"].count()

# função que recebe os 3 indicadores RFM e retorna o segmento
# os critérios são decisão de negócio — você que definiu os números
def classificador(recencia, frequencia, valor_total):
    if recencia <= 1 and frequencia >= 3 and valor_total >= 1000:
        return "Campeã(o)"   # comprou ontem, compra muito, gasta muito
    elif recencia <= 3 and frequencia <= 3:
        return "Leal"        # comprou recente mas gasta menos
    elif recencia <= 40 and frequencia <= 2:
        return "Em Risco"    # tá sumindo
    else:
        return "Perdida(o)"  # faz muito tempo sem aparecer

# monta o DataFrame RFM com os 3 indicadores
# os três têm cliente_id como índice — o pandas alinha automaticamente
dados_filtrados = pd.DataFrame({
    "recencia_dias": pedido_recente,
    "frequencia": frequencia_compra,
    "valor_total": valor_monetário
})

# apply percorre cada linha (axis=1) e passa os 3 valores pra função classificador
# lambda é um atalho pra chamar a função com os valores da linha atual
dados_filtrados["segmento_rfm"] = dados_filtrados.apply(
    lambda x: classificador(x["recencia_dias"], x["frequencia"], x["valor_total"]),
    axis=1
)

# cliente_id era índice — reset_index transforma em coluna normal pra fazer merge
dados_filtrados = dados_filtrados.reset_index()

# junta com clientes_df pra pegar nome e cidade de cada cliente
dados_filtrados = pd.merge(dados_filtrados, clientes_df, on="cliente_id", how="left")

# seleciona só as colunas que o cliente pediu — descarta o resto
cols = ["cliente_id", "nome", "cidade", "recencia_dias", "frequencia", "valor_total", "segmento_rfm"]
dados_filtrados = dados_filtrados[cols]

# exporta o relatório final pra CSV — index=False remove a numeração do pandas
dados_filtrados.to_csv("relatorio_crm.csv", index=False)

print("Sucesso na exportação")

# monta tabela cruzada Frequência x Recência pra usar no mapa de calor
# values = o que contar, index = linhas, columns = colunas
# fill_value=0 preenche com zero onde não tem cliente
tabela = pd.pivot_table(
    dados_filtrados,
    values="cliente_id",
    index="frequencia",
    columns="recencia_dias",
    aggfunc="count",
    fill_value=0
)

# ======= Parte de Matplotlib =======
import matplotlib.pyplot as plt

# conta quantos clientes tem em cada segmento
contagem_segmentos = dados_filtrados["segmento_rfm"].value_counts()

# cria a tela com tamanho 8x5 polegadas
plt.figure(figsize=(8, 5))

# desenha as barras — cada segmento com sua cor
plt.bar(contagem_segmentos.index, contagem_segmentos.values, color=("red","blue","pink","black"))

# título e labels dos eixos
plt.title("Quantidade de Clientes por Segmento RFM")
plt.ylabel("Quantidade de Clientes")
plt.xlabel("Segmento")

# salva em arquivo antes de mostrar — depois do show o gráfico é limpo da memória
plt.savefig("figura_dados.png")
plt.show()

# ======= Parte de Seaborn =======
import seaborn as sns

# cria nova tela pra não sobrepor o gráfico anterior
plt.figure(figsize=(10, 5))

# heatmap recebe a tabela cruzada
# annot=True mostra o número dentro de cada célula
# cmap="YlOrRd" paleta do amarelo pro vermelho — mais cliente = mais vermelho
sns.heatmap(tabela, annot=True, cmap="YlOrRd")

plt.title("Mapa de Calor: Frequência x Recência")

plt.savefig("figura_dados2.png")
plt.show()