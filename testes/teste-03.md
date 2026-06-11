# Teste 03 - Configuração estabilizada da Fase 1

Data: 2026-06-11

## Configuração

- Dataset: `sklearn.datasets.load_breast_cancer`
- Amostras: 100, selecionadas de forma estratificada
- Split: 70% treino e 30% teste, também estratificado
- Pré-processamento: `StandardScaler` ajustado no treino, PCA com 2 componentes ajustado no treino, `MinMaxScaler` para escala `0..1`
- Otimizador principal: SPSA
- `maxiter`: 100
- `random_state`: 42

## Resultado do script principal

```text
## PARAMETROS
 - Amostras: 100
 - Componentes PCA: 2
 - Maxiter: 100
 - Otimizador: SPSA

## RESULTADOS DA FASE 1
Modelo Clássico (SVM):
 - Acurácia: 100.00%
 - Tempo de treino: 0.0009 segundos

Modelo Quântico (VQC Simulado):
 - Acurácia: 83.33%
 - Tempo de treino: 12.8098 segundos
```

## Comparação complementar

Na mesma configuração de dados, os otimizadores testados tiveram o seguinte comportamento:

| Otimizador | Maxiter | Acurácia VQC | Tempo VQC |
|---|---:|---:|---:|
| SPSA | 100 | 83,33% | 12,8605 s |
| SPSA | 200 | 83,33% | 24,1435 s |
| COBYLA | 100 | 83,33% | 4,0098 s |

## Conclusão

A Fase 1 atingiu o critério prático de acurácia quântica acima de 80%. O SPSA manteve a acurácia em 83,33%, mas foi mais lento que COBYLA no simulador sem ruído. Esse resultado deve ser usado na discussão: SPSA é teoricamente interessante para cenários ruidosos/NISQ, enquanto COBYLA pode ser mais eficiente no simulador ideal usado nesta etapa.
