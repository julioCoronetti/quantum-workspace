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

**Status:** Concluída.
**Objetivo Prático:** Traduzir a tarefa de classificação binária para o paradigma combinatório via QUBO (Quadratic Unconstrained Binary Optimization) e resolver via QAOA e solver exato.
- **Implementação:** Arquivo `experimentos/script_qaoa.py` integrando `qiskit_optimization`, discretização de coeficientes lineares e ansatz variacional.
- **Resultados validados:** Registro detalhado nos relatórios `testes/teste-04-qubo.md` e `testes/teste-05-qaoa-inicial.md`. Acurácia de 90,00% obtida com 2 componentes PCA em 3,70 s.

#### Fase 3: Pipeline de Estresse e Coleta de Dados

**Status:** Concluída.
**Objetivo Prático:** Avaliar a escalabilidade temporal e combinatória do modelo variando os componentes do PCA de 2 a 5.
- **Implementação:** Experimentos automatizados salvos em `resultados/resultados_qaoa_pca.csv` e `resultados/resultados_qubo_exato_pca.csv`.
- **Geração de Gráficos:** Script `gerar_graficos.py` gerando gráficos vetoriais em `resultados/`.
- **Métricas consolidadas:**
  - Solver exato: acurácia constante em 90,00%, tempo escalando de 0,08 s (6 variáveis) a 7,15 s (12 variáveis).
  - QAOA simulado: acurácia de 90,00% (PCA=2, 3,70 s), 90,00% (PCA=3, 41,71 s) e 96,67% (PCA=4, 863,42 s com `maxiter=5`).

#### Fase 4: Conversão para Template Oficial UniSENAI 2026

**Status:** Concluída.
**Objetivo Prático:** Adequar o relatório científico às normas e estilos do novo template de Resumo Expandido UniSENAI 2026 (Word e PDF).
- **Template DOCX Base:** `publicação/templates/Template_ResumoExpandido2026.docx`.
- **Compilador DOCX Nativo:** `publicação/geradores/gerar_resumo_expandido.py` gerando `publicação/dist/Resumo_Expandido_Julio_Regino_2026.docx`.
- **Compilador PDF Nativo:** `publicação/geradores/gerar_resumo_expandido_pdf.py` gerando `publicação/dist/Resumo_Expandido_Julio_Regino_2026.pdf`.
- **Identidade Visual:** Cunha vermelha superior direita (`#F9131E`), faixa trapezoidal cinza inferior (`#EBEBEB`) e logotipo oficial do SENAI vetorizado no rodapé.

#### Fase 5: Refinamento Textual e Descontaminação de Padrões de IA

**Status:** Concluída em 2026-10-15.
**Objetivo Prático:** Eliminar traços sintéticos de geração automatizada, clichês de linguagem e inconsistências metodológicas apontadas em análise externa.
- **Ajustes de Redação:**
  - Eliminação de construções repetitivas da fórmula "não X, mas Y".
  - Reestruturação da Revisão de Literatura para abordagem direta do estado da arte e autores, removendo moldes de meta-justificação a cada parágrafo.
  - Redução drástica de anafóricos mecânicos ("Esse/Essa + substantivo") e menções redundantes a "NISQ".
  - Substituição de vocabulário inflado ("restrições severas", "desafio crítico", "etapa crítica", "trade-off") por terminologia técnica sóbria.
- **Consistência Científica e Metodológica:**
  - Esclarecimento analítico da acurácia de 96,67% do QAOA (PCA=4) vs 90,00% do solver exato: decorrente de discretização limítrofe sobre partição reduzida de teste (30 instâncias), caracterizando flutuação amostral.
  - Substituição de termos de jargão de código por notação matemática formal.
  - Padronização institucional de afiliação e biografia: Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior.
  - Correção tipográfica do título da Seção 3: `3 METODOLOGIA`.

---

## Guia para Continuidade em Outro Ambiente

Para retomar o desenvolvimento deste projeto em uma nova máquina ou ambiente de desenvolvimento:

1. **Clonagem do Repositório:**
   ```bash
   git clone https://github.com/julioCoronetti/quantum-workspace.git
   cd quantum-workspace
   git checkout main
   ```

2. **Configuração do Ambiente Virtual Python:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Regeneração dos Documentos Científicos (DOCX e PDF):**
   Os scripts utilizam apenas a biblioteca padrão do Python (`zipfile`, `zlib`, `struct`), sem necessidade de dependências pesadas adicionais:
   ```bash
   # Compilação do Resumo Expandido (5 páginas)
   python3 publicação/geradores/gerar_resumo_expandido.py
   python3 publicação/geradores/gerar_resumo_expandido_pdf.py

   # Compilação da Versão Completa da Pesquisa (7 páginas)
   python3 publicação/geradores/gerar_artigo_completo_docx.py
   python3 publicação/geradores/gerar_artigo_completo_pdf.py
   ```

4. **Estrutura dos Arquivos Principais:**
   - `publicação/dist/`: Documentos finais oficiais formatados para entrega.
   - `publicação/geradores/`: Scripts geradores dos documentos em PDF e Word.
   - `publicação/templates/`: Ativos gráficos e arquivo modelo institucional.
   - `experimentos/script.py`: Pipeline do baseline clássico (SVM) e quântico variacional (VQC).
   - `experimentos/script_qaoa.py`: Pipeline de formulação QUBO, QAOA e solver exato por força bruta.
   - `experimentos/gerar_graficos.py`: Script gerador dos gráficos de acurácia e tempo.
   - `resultados/`: Arquivos CSV com as medições empíricas brutas e figuras vetoriais.
   - `testes/`: Relatórios detalhados de cada bateria experimental executada.

