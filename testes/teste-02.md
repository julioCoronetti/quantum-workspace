# Teste 02 - Diagnóstico da Fase 1

Data: 2026-06-11

## Objetivo

Verificar por que a troca inicial para SPSA com `maxiter=100` ainda não estabilizava o VQC acima de 80%.

## Diagnóstico

O script original aplicava PCA antes do split de treino/teste e usava os 60 primeiros registros do dataset `breast cancer`. Isso criava dois problemas para a pesquisa:

- O PCA era ajustado usando dados que depois entravam no teste.
- Os 60 primeiros registros tinham distribuição enviesada: 47 casos da classe 0 e 13 da classe 1.

## Testes exploratórios

Após corrigir o split estratificado e testar escalas de entrada com `COBYLA` e `maxiter=30`, os resultados foram:

| Escala após PCA | Acurácia SVM | Acurácia VQC |
|---|---:|---:|
| PCA padronizado, sem MinMax | 88,89% | 61,11% |
| MinMax `0..1` | 77,78% | 72,22% |
| MinMax `-1..1` | 83,33% | 27,78% |
| MinMax `-pi..pi` | 88,89% | 55,56% |

Com 60 amostras e escala `0..1`, a melhor configuração testada chegou a 77,78%:

| Otimizador | Maxiter | Acurácia VQC | Tempo VQC |
|---|---:|---:|---:|
| COBYLA | 30 | 72,22% | 1,3969 s |
| COBYLA | 100 | 77,78% | 4,4992 s |
| COBYLA | 200 | 77,78% | 4,6191 s |
| SPSA | 100 | 61,11% | 11,7548 s |
| SPSA | 200 | 61,11% | 21,5152 s |

## Conclusão

Com apenas 60 amostras, o conjunto de teste tinha 18 exemplos. O resultado de 77,78% corresponde a 14 acertos em 18; faltava apenas 1 acerto para superar 80%, mas a base era pequena demais para sustentar a conclusão. O próximo teste deve usar uma amostra estratificada maior.
