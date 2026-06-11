# Teste 06 - Estresse preliminar por número de componentes PCA

Data: 2026-06-11

## Objetivo

Avaliar, de forma preliminar, o impacto do aumento de componentes PCA no número de variáveis binárias e no tempo de solução da formulação QUBO.

## Arquivos gerados

- `resultados/resultados_qubo_exato_pca.csv`
- `resultados/resultados_qaoa_pca_2.csv`
- `resultados/resultados_qaoa_pca_3.csv`
- `resultados/resultados_qaoa_pca_4.csv`

## Resultado QUBO exato

O solver exato por força bruta foi usado como caminho leve para medir a formulação QUBO em PCA 2 a 5 sem acionar QAOA pesado.

| PCA | Variáveis binárias | Acurácia SVM | Acurácia QUBO exato | Tempo QUBO exato |
|---:|---:|---:|---:|---:|
| 2 | 6 | 100,00% | 90,00% | 0,0824 s |
| 3 | 8 | 100,00% | 90,00% | 0,4580 s |
| 4 | 10 | 100,00% | 90,00% | 1,2578 s |
| 5 | 12 | 100,00% | 90,00% | 7,1497 s |

## Resultado QAOA

| PCA | Variáveis binárias | Otimizador | Maxiter | Acurácia QAOA | Tempo QAOA |
|---:|---:|---|---:|---:|---:|
| 2 | 6 | COBYLA | 20 | 90,00% | 3,6997 s |
| 3 | 8 | COBYLA | 20 | 90,00% | 41,7146 s |
| 4 | 10 | COBYLA | 5 | 96,67% | 863,4231 s |

## Interpretação

O crescimento do número de variáveis binárias torna o QAOA rapidamente caro para o Codespace. Mesmo reduzindo `maxiter` para 5 na instância com 4 componentes PCA, a execução levou mais de 14 minutos.

Para o artigo, a leitura mais honesta é:

- O pipeline QUBO/QAOA funciona em instâncias pequenas.
- A acurácia preliminar foi competitiva no conjunto de teste.
- O tempo cresce rapidamente quando o número de variáveis binárias aumenta.
- A limitação computacional observada reforça a discussão sobre custo de simulação clássica e restrições da era NISQ.

## Decisão prática

Não executar `--stress` com QAOA completo no Codespace sem necessidade. Para novas coletas, rodar uma configuração por vez e commitar cada etapa.
