# Atlas do mercado escolar - Academe Educação

Painel estático, sem backend, login, analytics ou serviços pagos. Mapa vetorial, filtros por UF, porte total, categoria privada e etapa; comparação nacional; exportação CSV; simulador comercial de cinco anos com premissas mantidas somente na memória da aba. Não há dados de carteira de clientes, pessoas, escolas identificadas ou credenciais.

## Executar
`python3 -m http.server 8080` e abrir localhost:8080. Publicar o diretório raiz na Vercel como projeto **Other**, sem comando de build. Arquivo de runtime: index.html (HTML, CSS, JavaScript e base agregada no mesmo arquivo).

## Fontes e atualização
- Microdados: https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2025_.zip
- Sinopses: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/sinopses-estatisticas/educacao-basica
- Malha de origem IBGE, distribuição CC0: https://github.com/henriquemalvar/br-geojson e https://cdn.jsdelivr.net/gh/henriquemalvar/br-geojson@main/dist/estados.geojson

Fonte verificada em 30/10/2026: edição mais recente 2025, Sinopse atualizada em julho/2026. Não é tempo real, não há tarefa automática ou atualização indefinida.

A constante DATA.groups no HTML agrega por CO_UF, categoria privada e faixa de porte [0,100,300,500,1000]. Cada grupo contém [UF, categoria, limite inferior de porte, soma BAS, soma INF, soma FUND, soma MED, número de unidades]. DATA.paths contém a malha vetorial. DATA.meta contém proveniência e hash do CSV de origem. O CSV de entrada foi extraído dos microdados oficiais, limitado à rede privada, com matrícula BAS > 0 e com o recorte conferido contra a Sinopse. Sem matrícula: excluídas. Categoria: 1 particular, 2 comunitária, 3 confessional, 4 filantrópica.

Para reproduzir: preparar CSV com os campos CO_UF, CO_MUNICIPIO, TP_CATEGORIA_ESCOLA_PRIVADA, QT_MAT_BAS, QT_MAT_INF, QT_MAT_FUND, QT_MAT_MED, QT_MAT_EJA, QT_MAT_PROF, QT_MAT_ESP; baixar estados.geojson do link acima; executar `python3 prepare.py escolas.csv estados.geojson 2025 > data-block.js` e substituir o bloco const DATA no HTML pelo resultado.

Para nova edição: confirmar sua publicação no Inep, extrair o mesmo esquema, conferir totais com a Sinopse, atualizar ano e verificações em prepare.py, fontes e notas de atualidade em index.html/app.js. Regenerar a constante DATA dentro de index.html, testar filtros, comparar BR/CE e só então publicar. As assertions de 2025 devem ser substituídas pelos totais auditados da nova edição, não removidas sem substituição.

## Verificações de referência 2025
- Brasil: 41.746 unidades / 9.245.384 matrículas BAS.
- Ceará: 1.686 / 399.969 BAS.
- Porte total >= 300 Brasil: 8.873 / 5.609.618 BAS / 4.114.450 FUND+MED.
- Porte total >= 300 Ceará: 402 / 245.040 BAS / 175.593 FUND+MED.

Matrículas não são pessoas únicas. Porte é BAS da unidade, independente da etapa selecionada. Contagem de unidades usa porte/categoria/UF, não presença da etapa. BAS não é soma de etapas. Sem dados de mensalidade, sem filtro de R$600 e sem extrapolação de amostras. Receita é simulação à tabela, não faturamento, SAM ou previsão. Denominador do simulador permanece em 2025. Simulações não são salvas nem enviadas.
