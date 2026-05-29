## COBYLA vs. SPSA no Qiskit

Ambos são otimizadores **sem gradiente** (*gradient-free*) disponíveis no `qiskit.algorithms.optimizers`, mas operam de formas fundamentalmente distintas. [quantum.cloud.ibm](https://quantum.cloud.ibm.com/docs/en/api/qiskit/0.45/qiskit.algorithms.optimizers)

## Como o COBYLA funciona

COBYLA (*Constrained Optimization By Linear Approximation*) constrói um **modelo linear local** do espaço de parâmetros a cada iteração. Ele avalia a função de custo em pontos vizinhos para montar uma aproximação da superfície e decide para onde mover os parâmetros. O problema: cada avaliação assume que o valor retornado é *determinístico*. Em hardware quântico real, o mesmo conjunto de parâmetros medido duas vezes retorna valores ligeiramente diferentes (shot noise), o que **corrompe o modelo linear** e faz o COBYLA tomar decisões baseadas em informação ruidosa. [syskool](https://syskool.com/optimization-techniques-in-quantum-machine-learning-spsa-cobyla-and-beyond/)

## Por que o SPSA é mais robusto

SPSA (*Simultaneous Perturbation Stochastic Approximation*) **estima o gradiente perturbando todos os parâmetros simultaneamente** com vetores aleatórios \(\Delta_k\), usando apenas **duas avaliações da função de custo** por iteração: [syskool](https://syskool.com/optimization-techniques-in-quantum-machine-learning-spsa-cobyla-and-beyond/)

A chave para a robustez ao ruído está em dois aspectos do SPSA:

- **Natureza estocástica intrínseca**: o algoritmo *espera* e *incorpora* variabilidade nas medições. O ruído de shot noise é tratado como parte da aproximação estocástica, não como um erro que distorce o modelo. [syskool](https://syskool.com/optimization-techniques-in-quantum-machine-learning-spsa-cobyla-and-beyond/)
- **Custo fixo de avaliações**: com apenas 2 avaliações por passo, o SPSA não acumula erros de modelagem ao tentar reconstruir uma superfície completa como o COBYLA faz. [syskool](https://syskool.com/optimization-techniques-in-quantum-machine-learning-spsa-cobyla-and-beyond/)

## Quando usar cada um

| Critério | SPSA | COBYLA |
|---|---|---|
| Hardware quântico ruidoso (NISQ) | ✅ Ideal | ⚠️ Frágil |
| Simulador sem ruído | ⚠️ Pode oscilar | ✅ Converge bem |
| Alta dimensionalidade (muitos parâmetros) | ✅ Escalável | ❌ Lento |
| Restrições de parâmetros | ❌ Não suporta | ✅ Suporta nativo |
| QAOA / VQE em hardware real | ✅ Recomendado | ⚠️ Possível, mas instável |

Para aplicações como QAOA em dispositivos IBM reais, o SPSA é o otimizador padrão recomendado justamente porque a variância das medições quânticas não interfere na sua lógica de convergência. [quantum.cloud.ibm](https://quantum.cloud.ibm.com/docs/en/api/qiskit/0.45/qiskit.algorithms.optimizers)