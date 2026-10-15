# Mapa das secoes do artigo

## Titulo

Titulo atual em `contexto-ic.md`:

> Exploracao do Algoritmo QAOA para Otimizacao em Modelos de Classificacao Supervisionada utilizando Simuladores Quanticos

Sugestao de titulo em ingles:

> Exploration of the QAOA Algorithm for Optimization in Supervised Classification Models Using Quantum Simulators

Pendencias:

- Confirmar se o titulo deve mencionar SVM/QUBO explicitamente.

## Resumo

Escrever por ultimo.

Conteudo obrigatorio:

- Problema: classificacao supervisionada convertida em otimizacao.
- Objetivo: avaliar viabilidade de QAOA/QUBO em simulador.
- Metodo: dataset breast cancer, PCA, SVM classico, VQC baseline, QAOA/QUBO.
- Resultados: usar somente metricas finais medidas.
- Conclusao: destacar desempenho, custo computacional e limitacoes.

## Introducao

Funcao:

- Apresentar computacao quantica NISQ, QAOA e classificacao supervisionada.
- Justificar por que SVM/classificacao pode ser analisado como problema de otimizacao.
- Fechar com objetivo geral e objetivos especificos.

Referencias provaveis:

- Preskill (2018)
- Farhi, Goldstone e Gutmann (2014)
- Havlicek et al. (2019)
- Cerezo et al. (2021)

## Revisao de Literatura

Subsecoes sugeridas:

1. Computacao quantica na era NISQ
2. Algoritmos variacionais e QAOA
3. Quantum machine learning e classificacao supervisionada
4. SVM, QUBO e formulacoes discretas de otimizacao
5. Otimizadores classicos em circuitos variacionais

Referencias provaveis:

- Preskill (2018)
- Bharti et al. (2022)
- Cerezo et al. (2021)
- Farhi, Goldstone e Gutmann (2014)
- Schuld e Killoran (2019)
- Havlicek et al. (2019)
- Bifulco e Roversi (2025), se aceitarmos preprint recente
- Spall (1992), para SPSA

## Metodologia

Conteudo baseado em execucao, nao em promessa.

Itens:

- Ambiente Python/Qiskit/scikit-learn.
- Dataset `breast cancer`.
- Pre-processamento sem vazamento: split estratificado, `StandardScaler`, PCA, `MinMaxScaler`.
- Baseline classico: SVM linear.
- Baseline quantico: VQC simulado.
- Experimento principal: QUBO/QAOA, quando implementado.
- Protocolo de comparacao: acuracia e tempo de execucao.
- Variacao de dimensionalidade por PCA.

Arquivos de origem:

- `script.py`
- futuro `script_qaoa.py`
- `testes/teste-03.md`
- futuros logs da Fase 2 e Fase 3

## Resultados e Discussoes

Conteudo ja disponivel:

- Fase 1: SVM classico 100,00%; VQC simulado 83,33%; VQC mais lento.

Conteudo pendente:

- QAOA/QUBO inicial.
- Tabela final por numero de componentes PCA.
- Graficos de acuracia e tempo.

Discussao esperada:

- Acuracia nao e o unico criterio; custo de simulacao e escalabilidade sao centrais.
- SPSA tem justificativa em cenarios ruidosos, mas pode ser mais lento em simulador ideal.
- QAOA exige que o problema seja formulado como otimizacao discreta; isso adiciona complexidade ao pipeline.

## Conclusao

Escrever apos resultados finais.

Pontos provaveis:

- A abordagem e viavel como estudo experimental em simulador.
- O baseline quantico atingiu acuracia acima de 80%, mas com custo temporal superior ao SVM.
- A formulacao QUBO/QAOA deve ser avaliada pela relacao entre acuracia, tempo e crescimento de variaveis.
- Trabalhos futuros: aumentar datasets, testar ruido/hardware real, variar ansatz/reps, comparar otimizadores.
