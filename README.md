# Segmentação de Clientes por Comportamento de Compra

## Sobre o projeto
Análise RFM (Recência, Frequência e Valor Monetário) de clientes 
de um e-commerce de moda feminina. O objetivo é segmentar clientes 
para orientar ações de CRM — quem recebe cupom, quem recebe e-mail 
de reativação e quem não precisa de ação.

## Upgrades realizados
- Adicionado gráfico de barras com distribuição dos segmentos RFM
- Adicionado mapa de calor Frequência x Recência com seaborn
- Gráficos exportados automaticamente em PNG

## O que o projeto faz
- Limpa e padroniza dados de clientes e pedidos
- Calcula os 3 indicadores RFM de cada cliente
- Classifica cada cliente em: Campeã, Leal, Em Risco ou Perdida
- Gera 2 gráficos profissionais automaticamente
- Exporta relatório CSV pronto para o time de CRM usar

## Tecnologias
- Python 3.12
- pandas
- numpy
- matplotlib
- seaborn

## Como rodar
pip install pandas numpy matplotlib seaborn
python segmentacao-clientes.py

## Resultado
| Segmento | Descrição |
|---|---|
| Campeã | Comprou recente, frequente e gasta muito |
| Leal | Compra com frequência |
| Em Risco | Tá sumindo |
| Perdida | Faz muito tempo sem comprar |