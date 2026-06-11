# Iniciação Cientifica

## Título:

Exploração do Algoritmo QAOA para Otimização em Modelos de Classificação Supervisionada utilizando Simuladores Quânticos

---

## Texto base do tema:

### Algoritmo QAOA

O QAOA (Quantum Approximate Optimization Algorithm) é um algoritmo quântico que tem ganhado destaque para resolver problemas de otimização combinatória. Ele é considerado um dos algoritmos mais promissores para rodar em computadores quânticos de médio porte (near-term quantum devices). Por ser um algoritmo que já possui formulação matemática e implementações em simuladores, torna o estudo mais focado e concreto.

### Otimização em Modelos de Classificação Supervisionada

Aqui você direciona o uso do QAOA para melhorar um problema específico da inteligência artificial, que são os modelos de classificação com supervisão, por exemplo, classificar imagens, textos ou dados numéricos em categorias. Essa abordagem delimita um escopo prático e claro para a pesquisa, em vez de buscar avanços amplos e genéricos em IA.

---

## Objetivos

Investigar a viabilidade e o desempenho do algoritmo quântico QAOA na otimização de modelos de classificação supervisionada, utilizando simuladores quânticos para comparar sua eficiência e precisão em relação aos métodos clássicos tradicionais.

### Objetivos Específicos

- **Mapear** o problema de classificação binária (Support Vector Machine) para uma formulação matemática de otimização discreta (QUBO).
- **Implementar e testar** o algoritmo QAOA em um ambiente de simulação quântica (Qiskit), avaliando o impacto de diferentes otimizadores (como COBYLA e SPSA) na convergência do modelo.
- **Medir e comparar** as métricas de acurácia e tempo de execução entre o modelo híbrido simulado e o classificador clássico (SVM).
- **Analisar** o impacto da dimensionalidade dos dados (número de *features* reduzidas via PCA) no custo computacional e na memória do simulador.

---

## Metodologia

Implementar o algoritmo QAOA em simuladores quânticos (ex.: Qiskit), aplicar em conjuntos de dados para tarefas de classificação, comparar resultados com métodos clássicos e analisar desempenho, eficiência e limitações técnicas do processo.

### Hipótese Norteadora

A conversão de problemas de classificação supervisionada para formulações QUBO permite que o algoritmo QAOA alcance uma acurácia convergente e viável. No entanto, postula-se que, no ambiente de simuladores quânticos, o modelo híbrido apresentará um tempo de execução significativamente superior ao clássico devido ao alto custo computacional exigido para emular estados quânticos em processadores tradicionais, refletindo as atuais restrições de infraestrutura da era NISQ.

---

### Siglas

**QAOA (Quantum Approximate Optimization Algorithm):** Algoritmo quântico focado em resolver problemas complexos de otimização de forma aproximada.

**NISQ (Noisy Intermediate-Scale Quantum):** A atual geração de computadores quânticos. Eles ainda possuem poucos qubits e sofrem com ruídos (erros de processamento).

**QUBO (Quadratic Unconstrained Binary Optimization):** Modelo matemático usado para traduzir problemas clássicos para uma estrutura que o algoritmo quântico consiga processar.

**SVM (Support Vector Machine):** Algoritmo clássico de Machine Learning amplamente utilizado para separar e classificar dados em categorias.

---

### Fases

#### Fase 1: Estabilizando o Modelo Base

**Status:** Concluída em 2026-06-11 para o baseline VQC simulado. A configuração estabilizada usa 100 amostras estratificadas, PCA com 2 componentes, escala `0..1`, otimizador SPSA e `maxiter=100`.

**Objetivo Prático:** Fazer a acurácia quântica subir de 44% para mais de 80%, estabilizando o aprendizado do modelo.

- **Pesquisa:** Entender a diferença entre os otimizadores clássicos do Qiskit, focando no motivo pelo qual o SPSA lida melhor com ruídos do que o COBYLA.
- **Experimento:** No script inicial, aumentar o `maxiter` de 30 para 100 ou 200 e trocar o otimizador para SPSA.
- **Resultado validado:** O script principal atingiu 83,33% de acurácia no VQC simulado e 100,00% no SVM clássico. O registro completo está em `testes/teste-03.md`.
- **Buscas no EBSCO (Justificativa Teórica):** Encontrar artigos que justifiquem a troca para um otimizador mais robusto no ambiente quântico.
    - `"Quantum Machine Learning" AND ("SPSA" OR "COBYLA") AND "optimizer"`
    - `"Variational Quantum Classifier" AND "noise" AND "SPSA"`

#### Fase 2: O Coração da IC (Implementando o QAOA)

**Status:** Próxima fase.

**Objetivo Prático:** Traduzir a classificação em otimização. O QAOA não roda classificação nativamente; ele precisa ler o problema matematicamente de outra forma.

- **Pesquisa:** Estudar o conceito de QUBO (Quadratic Unconstrained Binary Optimization). Pesquisar especificamente pelo termo *"How to map SVM to QUBO Qiskit"*.
- **Experimento:** Usar a biblioteca `qiskit-optimization` para formular a classificação do dataset como um QUBO. Depois, substituir o `VQC` e o `RealAmplitudes` pelo `QAOAAnsatz`.
- **Buscas no EBSCO (A Pesquisa Principal):** Artigos que mostrem como transformar um problema clássico de IA (SVM) em uma matriz matemática (QUBO) que o QAOA consiga ler.
    - `"QAOA" AND ("Support Vector Machine" OR "SVM" OR "Classification")`
    - `"QUBO" AND "Support Vector Machine" AND "Quantum"`
    - `"Quantum Approximate Optimization Algorithm" AND "QUBO" AND "Machine Learning"`

#### Fase 3: Pipeline de Estresse e Coleta de Dados

**Objetivo Prático:** Gerar os dados finais e as métricas para a criação dos gráficos que irão compor o artigo.

- **Pesquisa:** Entender a relação exponencial entre o número de features (colunas do dataset) e a exigência de memória RAM/processamento do simulador quântico.
- **Experimento:** Criar um script com um loop que roda o QAOA variando as features do PCA (2, 3, 4 e 5). Salvar automaticamente os resultados (Tempo Clássico, Tempo Quântico, Acurácia Clássica, Acurácia Quântica) em um arquivo `.csv`.
- **Buscas no EBSCO (Munição para Discussão):** Provar cientificamente que a lentidão no processamento (ex: o tempo de 1.64s do primeiro teste) é uma limitação arquitetural de simuladores e hardwares atuais, e não um erro do código.
    - `"Quantum Simulator" AND "performance" AND ("scaling" OR "qubits")`
    - `("PCA" OR "feature reduction") AND "Quantum Machine Learning" AND "limitations"`

#### Fase 4: Redação no Template

**Objetivo Prático:** Transformar os logs de dados e anotações no documento científico final formatado.

- **Pesquisa:** Buscar 3 ou 4 artigos recentes (de 2023 para cá) sobre aplicações práticas para usar na "Revisão de Literatura".
- **Ação:** Preencher a estrutura do artigo utilizando o template `main.tex`. Usar o `.csv` da Fase 3 para gerar gráficos de barra (Tempo vs. Features) e colocá-los na seção de "Resultados e Discussões".
- **Buscas no EBSCO (Contexto da Introdução):** Artigos mais amplos para dar peso acadêmico logo no início do texto, estabelecendo que o QAOA é o estado da arte para computadores quânticos de curto prazo (era NISQ).
    - `"QAOA" AND "supervised learning"`
    - `"Quantum Machine Learning" AND "NISQ era" AND "Classification"`
