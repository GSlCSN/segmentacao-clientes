## 🎯 Nome do projeto
**Segmentação de Clientes por Comportamento de Compra em E-commerce de Moda**

---

## 📊 Nível de dificuldade
**3 — Intermediário**
Exige raciocínio analítico além do código: você vai construir um pipeline de limpeza, cruzar duas fontes de dados e segmentar clientes com análise RFM (Recência, Frequência e Valor Monetário).

---

## 🧩 Tema
E-commerce

---

## 📝 Descrição do desafio
Uma loja virtual de moda feminina quer entender quais clientes merecem ações de retenção e quais estão sumindo silenciosamente. Você vai cruzar dados de pedidos e cadastro de clientes, limpar inconsistências reais do banco, calcular os três indicadores RFM e classificar cada cliente em um segmento acionável (ex: Campeã, Em Risco, Perdida). O resultado final deve orientar a equipe de CRM sobre para quem mandar cupom, reativação ou nada.

---

## 📦 Dataset fictício

**Arquivo 1 — `pedidos.csv`** -- feito --
```csv
pedido_id,cliente_id,data_pedido,valor_total,status
1001,C01,2024-01-15,189.90,entregue
1002,C02,2024-02-03,450.00,entregue
1003,C01,2024-03-22,97.50,entregue
1004,C03,2024-01-08,312.00,cancelado
1005,C04,2023-11-30,88.00,entregue
1006,C02,2024-04-10,210.00,entregue
1007,C05,2024-03-05,560.00,entregue
1008,C01,2024-04-28,134.00,entregue
1009,C06,2024-02-14,,entregue
1010,C03,2024-03-19,275.00,entregue
1011,C07,2023-12-01,99.90,entregue
1012,C04,2024-01-20,145.00,entregue
1013,C05,2024-04-15,430.00,entregue
1014,C08,2022-07-10,310.00,entregue
1015,C06,2024-03-30,180.00,entregue
1016,C07,2024-04-20,220.00,entregue
1017,C09,2024-04-25,95.00,entregue
1018,C02,2024-04-30,375.00,entregue
```

**Arquivo 2 — `clientes.csv`** -- feito -- 
```csv
cliente_id,nome,cidade,estado,genero,data_cadastro
C01,Ana Lima,São Paulo,SP,F,2023-06-10
C02,Beatriz Souza,Campinas,SP,feminino,2023-08-22
C03,Carla Mendes,Rio de Janeiro,RJ,F,2023-05-15
C04,Débora Ramos,Belo Horizonte,MG,,2023-09-01
C05,Eliana Costa,Curitiba,PR,F,2023-07-19
C06,Fernanda Nunes,Porto Alegre,RS,F,2023-10-05
C07,Giovana Pereira,Recife,PE,F,2023-11-12
C08,Helena Martins,Salvador,BA,F,2021-03-30
C09,Isabela Teixeira,Fortaleza,CE,F,2024-04-01
C02,Beatriz Souza,Campinas,SP,feminino,2023-08-22
```

> 🧹 **O que está sujo (documenado):**
> - `pedidos.csv`: valor_total nulo no pedido 1009; pedido 1014 com data de 2022 (outlier temporal);
pedido 1004 cancelado que deve ser excluído da análise RFM

> - `clientes.csv`: coluna `genero` com encoding inconsistente (F / feminino / vazio); linha C02 duplicada;
 C08 com cadastro muito antigo e apenas 1 compra antiga -- feito -- 

---

## 🛠 Bibliotecas necessárias
```
pandas
numpy
matplotlib
seaborn
datetime (built-in)
```

---

## ⏱ Tempo estimado
**4 a 6 horas** estudando 2h/dia → 2 a 3 sessões de estudo

---

## ✅ Entregável esperado

1. **Pipeline de limpeza documentado** — cada decisão explicada em comentário no código (por que removeu, imputou ou ignorou cada problema)
2. **DataFrame final** com as colunas: `cliente_id`, `nome`, `cidade`, `recencia_dias`, `frequencia`, `valor_total`, `segmento_rfm`
3. **Segmentação RFM** com pelo menos 4 categorias: `Campeã`, `Leal`, `Em Risco`, `Perdida` — critérios definidos por você e justificados
4. **2 gráficos**: distribuição dos segmentos (barras) + mapa de calor Frequência × Recência
5. **Arquivo `relatorio_crm.csv`** exportado com nome, cidade e segmento — pronto para a equipe usar

---

## 🎯 Desafio bônus — 7/10

A loja agora quer rodar essa mesma análise todo mês automaticamente, para diferentes arquivos que chegam numa pasta `/dados/YYYY-MM/`. Transforme seu pipeline em uma **função `analisar_rfm(pasta)`** que recebe o caminho da pasta, lê os dois CSVs de lá dentro e devolve o DataFrame segmentado — lembre que o Python tem um módulo nativo que sabe montar caminhos de forma segura em qualquer sistema operacional, sem precisar concatenar strings manualmente.

---

Quer que eu gere o próximo projeto, ou prefere uma **trilha completa** a partir desse nível 3? 🚀