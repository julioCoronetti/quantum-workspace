# Inventario de dados, tabelas e figuras

## Dados ja existentes

| Origem | Conteudo | Uso no artigo |
|---|---|---|
| `testes/teste-inicial.md` | COBYLA/30 inicial | Contexto historico, se necessario |
| `testes/teste-01.md` | SPSA/100 inicial com baixa acuracia | Diagnostico interno, provavelmente nao entra no artigo |
| `testes/teste-02.md` | Diagnostico de preprocessing e escala | Pode embasar metodologia, sem virar resultado principal |
| `testes/teste-03.md` | Fase 1 estabilizada | Resultado de baseline |
| `testes/teste-04-qubo.md` | Formulação QUBO da Fase 2 | Metodologia |
| `testes/teste-05-qaoa-inicial.md` | QAOA inicial com PCA=2 | Resultados preliminares |
| `testes/teste-06-pipeline-estresse.md` | Estresse preliminar PCA/QUBO | Discussão de escalabilidade |
| `resultados/resultados_qubo_exato_pca.csv` | QUBO exato para PCA 2-5 | Tabelas e gráficos |
| `resultados/resultados_qaoa_pca_2.csv` | QAOA PCA=2 | Resultado QAOA principal pequeno |
| `resultados/resultados_qaoa_pca_3.csv` | QAOA PCA=3 | Discussão de custo |
| `resultados/resultados_qaoa_pca_4.csv` | QAOA PCA=4 exploratório | Discussão de limitação computacional |

## Tabelas planejadas

### Tabela 1 - Configuracao experimental

Colunas:

- Item
- Valor

Linhas:

- Dataset
- Numero de amostras
- Split
- PCA
- Escala
- Modelos comparados
- Otimizadores
- Ambiente de simulacao

### Tabela 2 - Resultado da Fase 1

Colunas:

- Modelo
- Acuracia
- Tempo de treino
- Observacoes

### Tabela 3 - Resultados QAOA por PCA

Colunas:

- PCA
- Variaveis binarias
- Acuracia SVM
- Tempo SVM
- Acuracia QAOA
- Tempo QAOA
- Status

## Figuras planejadas

### Figura 1 - Fluxo metodologico

Fluxo:

Dataset -> Split estratificado -> Normalizacao/PCA -> Baseline SVM -> QUBO -> QAOA -> Metricas

Status: desenhar depois que a Fase 2 estiver implementada.

### Figura 2 - Acuracia por PCA

Fonte esperada:

- `resultados/resultados_qaoa_pca.csv`
- `resultados/resultados_qubo_exato_pca.csv`

Status: pendente de geração.

### Figura 3 - Tempo por PCA

Fonte esperada:

- `resultados/resultados_qaoa_pca.csv`
- `resultados/resultados_qubo_exato_pca.csv`

Status: pendente de geração.

## Arquivos a gerar futuramente

- `resultados/resultados_qaoa_pca.csv`
- `resultados/grafico_acuracia_pca.png`
- `resultados/grafico_tempo_pca.png`
- `testes/teste-04-qubo.md`
- `testes/teste-05-qaoa-inicial.md`
- `testes/teste-06-pipeline-estresse.md`
