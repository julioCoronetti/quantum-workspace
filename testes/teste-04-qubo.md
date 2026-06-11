# Teste 04 - Formulação QUBO da Fase 2

Data: 2026-06-11

## Objetivo

Registrar a formulação usada para transformar a tarefa de classificação binária em um problema QUBO pequeno o suficiente para execução no Codespace.

## Arquivo-base

- `script_qaoa.py`

## Ideia da formulação

A classificação foi modelada como um classificador linear discretizado. Cada coeficiente do modelo, incluindo o viés, é representado por variáveis binárias que indicam contribuição positiva ou negativa.

Para `d` componentes PCA, o modelo possui:

- 1 coeficiente de viés.
- `d` coeficientes de pesos.
- 2 variáveis binárias por coeficiente quando `bits_per_sign=1`.

Assim, o número de variáveis binárias é:

```text
n_binary_variables = 2 * (d + 1)
```

Exemplos:

| Componentes PCA | Variáveis binárias |
|---:|---:|
| 2 | 6 |
| 3 | 8 |
| 4 | 10 |
| 5 | 12 |

## Função objetivo

A função objetivo minimiza uma perda quadrática de margem:

```text
mean((bias + X @ weights - y_signed)^2)
```

onde:

- `y_signed = -1` para a classe 0.
- `y_signed = +1` para a classe 1.
- `bias` e `weights` são reconstruídos a partir das variáveis binárias.

Além da perda principal, foram adicionados:

- Regularização quadrática dos coeficientes.
- Penalização para evitar ativar simultaneamente o bit positivo e negativo do mesmo coeficiente.

## Parâmetros usados

| Parâmetro | Valor |
|---|---:|
| `n_samples` | 100 |
| `bits_per_sign` | 1 |
| `coefficient_scale` | 2.0 |
| `regularization` | 0.05 |
| `mutual_exclusion` | 0.25 |
| `random_state` | 42 |

## Predição

Após resolver o QUBO, os bits retornados são convertidos novamente para `bias` e `weights`. A classe prevista é definida pelo sinal do score linear:

```text
score = bias + X @ weights
classe = 1 se score >= 0, caso contrário 0
```

## Observação metodológica

Esta formulação não é uma implementação completa do SVM dual. Ela é uma formulação QUBO simplificada de classificador linear discretizado, usada para viabilizar a ponte experimental:

```text
classificação supervisionada -> otimização discreta -> QUBO -> QAOA
```

Essa limitação deve ser declarada no artigo para evitar afirmar mais do que o experimento realmente executou.
