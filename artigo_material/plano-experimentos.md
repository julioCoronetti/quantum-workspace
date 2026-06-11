# Plano de experimentos

Este plano separa o que ja esta medido do que ainda precisa ser executado para sustentar o artigo.

## Fase 1 - Baseline VQC/SVM

Status: concluida.

Arquivo-base:

- `script.py`

Registro:

- `testes/teste-03.md`

Configuracao validada:

- Dataset: `sklearn.datasets.load_breast_cancer`
- Amostras: 100, estratificadas
- PCA: 2 componentes
- Escala: `0..1`
- Classico: SVM linear
- Quantico baseline: VQC simulado
- Otimizador: SPSA
- `maxiter`: 100

Resultado registrado:

| Modelo | Acuracia | Tempo |
|---|---:|---:|
| SVM classico | 100,00% | 0,0009 s |
| VQC simulado | 83,33% | 12,8098 s |

## Fase 2 - QUBO/QAOA

Objetivo: transformar o problema de classificacao em uma formulacao QUBO e resolver por QAOA simulado.

Entregaveis sugeridos:

- `script_qaoa.py`: implementacao separada para nao quebrar o baseline da Fase 1.
- `testes/teste-04-qubo.md`: registro da formulacao QUBO escolhida.
- `testes/teste-05-qaoa-inicial.md`: primeira execucao QAOA.

Decisoes tecnicas a registrar:

- Como os pesos/variaveis do SVM serao discretizados.
- Qual funcao objetivo sera convertida para QUBO.
- Quantos bits serao usados por variavel.
- Como a predicao sera feita a partir da solucao binaria.
- Qual otimizador classico sera usado dentro do QAOA.
- Qual simulador/primitives do Qiskit sera usado.

Criterios minimos:

- O script precisa salvar acuracia, tempo, numero de features, numero de variaveis binarias e parametros do QAOA.
- O resultado precisa comparar com SVM classico no mesmo split.
- Se o QAOA nao superar o baseline, isso ainda pode ser resultado valido: a discussao deve focar viabilidade, custo e limitacoes.

## Fase 3 - Estresse por dimensionalidade

Objetivo: medir efeito de aumentar features via PCA.

Execucoes:

| Execucao | PCA | Dataset | Medidas |
|---|---:|---|---|
| E1 | 2 componentes | breast cancer | acuracia e tempo |
| E2 | 3 componentes | breast cancer | acuracia e tempo |
| E3 | 4 componentes | breast cancer | acuracia e tempo |
| E4 | 5 componentes | breast cancer | acuracia e tempo |

CSV esperado:

`resultados/resultados_qaoa_pca.csv`

Colunas sugeridas:

- `fase`
- `data_execucao`
- `n_samples`
- `n_components`
- `n_train`
- `n_test`
- `modelo`
- `otimizador`
- `maxiter`
- `qaoa_reps`
- `n_binary_variables`
- `accuracy`
- `train_time_seconds`
- `status`
- `observacoes`

## Fase 4 - Graficos

Graficos minimos para o artigo:

- Acuracia por numero de componentes PCA.
- Tempo de execucao por numero de componentes PCA.
- Comparacao SVM classico vs. modelo quantico/QAOA.

Arquivos sugeridos:

- `resultados/grafico_acuracia_pca.png`
- `resultados/grafico_tempo_pca.png`
- `resultados/tabela_resultados_finais.csv`
