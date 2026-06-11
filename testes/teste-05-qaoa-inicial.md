# Teste 05 - Execução inicial QAOA/QUBO

Data: 2026-06-11

## Objetivo

Validar se a formulação QUBO da Fase 2 pode ser resolvida com QAOA no ambiente de simulação do Codespace, usando uma configuração pequena.

## Comando registrado

```bash
python3 script_qaoa.py --components 2 --maxiter 20 --output resultados/resultados_qaoa_pca_2.csv
```

## Configuração

| Item | Valor |
|---|---:|
| Dataset | `sklearn.datasets.load_breast_cancer` |
| Amostras | 100 |
| Treino/teste | 70/30 |
| Componentes PCA | 2 |
| Variáveis binárias QUBO | 6 |
| Solver quântico | QAOA |
| Otimizador | COBYLA |
| `maxiter` | 20 |
| `qaoa_reps` | 1 |

## Resultado

| Modelo | Acurácia | Tempo | Status |
|---|---:|---:|---|
| SVM linear | 100,00% | 0,0013 s | SUCCESS |
| QAOA-QUBO linear | 90,00% | 3,6997 s | SUCCESS |

Arquivo gerado:

- `resultados/resultados_qaoa_pca_2.csv`

## Interpretação

O QAOA resolveu a formulação QUBO com sucesso em uma instância pequena, atingindo 90,00% de acurácia no conjunto de teste. O SVM clássico permaneceu superior em acurácia e tempo, mas o resultado confirma que o pipeline experimental da Fase 2 está funcional.

Esse resultado já pode sustentar uma parte da metodologia e dos resultados preliminares do artigo, desde que seja descrito como uma formulação linear discretizada e não como uma implementação completa do SVM dual.
