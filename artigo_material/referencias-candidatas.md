# Referencias candidatas

Lista inicial de artigos e fontes tecnicas para sustentar o artigo. As referencias abaixo foram separadas por funcao no texto. Antes da versao final, conferir acesso institucional/EBSCO quando possivel e manter no `.bib` apenas o que for citado.

## Base conceitual: QAOA e NISQ

1. Farhi, Goldstone e Gutmann (2014) - *A Quantum Approximate Optimization Algorithm*
   - Link: https://arxiv.org/abs/1411.4028
   - DOI arXiv: https://doi.org/10.48550/arXiv.1411.4028
   - Uso no artigo: fonte original do QAOA, para explicar problema de otimizacao, parametro `p`, circuito alternado e aproximacao.
   - Status: usar.

2. Preskill (2018) - *Quantum Computing in the NISQ era and beyond*
   - Link: https://arxiv.org/abs/1801.00862
   - Publicado em: Quantum 2, 79 (2018)
   - DOI: https://doi.org/10.22331/q-2018-08-06-79
   - Uso no artigo: contextualizar NISQ, ruido, limitacoes de circuitos e expectativa moderada para dispositivos atuais.
   - Status: usar.

3. Bharti et al. (2022) - *Noisy intermediate-scale quantum (NISQ) algorithms*
   - Link: https://arxiv.org/abs/2101.08448
   - Publicado em: Reviews of Modern Physics 94, 015004 (2022)
   - DOI: https://doi.org/10.1103/RevModPhys.94.015004
   - Uso no artigo: revisao ampla sobre algoritmos NISQ, incluindo variacionais, QAOA e limitacoes.
   - Status: usar se a revisao de literatura precisar de uma fonte recente e forte.

4. Cerezo et al. (2021) - *Variational Quantum Algorithms*
   - Link: https://arxiv.org/abs/2012.09265
   - Publicado em: Nature Reviews Physics 3, 625-644 (2021)
   - DOI: https://doi.org/10.1038/s42254-021-00348-9
   - Uso no artigo: explicar algoritmos variacionais hibridos, otimizador classico, ansatz e desafios de treinabilidade/eficiencia.
   - Status: usar.

## Quantum machine learning e classificacao

5. Havlicek et al. (2019) - *Supervised learning with quantum enhanced feature spaces*
   - Link: https://arxiv.org/abs/1804.11326
   - Publicado em: Nature 567, 209-212 (2019)
   - DOI: https://doi.org/10.1038/s41586-019-0980-2
   - Uso no artigo: ligar classificacao supervisionada, SVM/kernel methods, VQC e espacos de Hilbert quanticos.
   - Status: usar.

6. Schuld e Killoran (2019) - *Quantum machine learning in feature Hilbert spaces*
   - Link: https://arxiv.org/abs/1803.07128
   - Publicado em: Physical Review Letters 122, 040504 (2019)
   - DOI: https://doi.org/10.1103/PhysRevLett.122.040504
   - Uso no artigo: fundamentar encoding de dados como feature map quantico e relacao com classificadores lineares/kernel.
   - Status: usar.

7. Rebentrost, Mohseni e Lloyd (2014) - *Quantum support vector machine for big data classification*
   - Link: https://arxiv.org/abs/1307.0471
   - Publicado em: Physical Review Letters 113, 130503 (2014)
   - DOI: https://doi.org/10.1103/PhysRevLett.113.130503
   - Uso no artigo: referencia historica de SVM quantico. Usar com cuidado, pois depende de premissas diferentes do nosso simulador Qiskit.
   - Status: opcional.

## QUBO, SVM e ponte para otimizacao

8. Bifulco e Roversi (2025) - *Exploring an implementation of quantum learning pipeline for support vector machines*
   - Link: https://arxiv.org/abs/2509.04983
   - DOI arXiv: https://doi.org/10.48550/arXiv.2509.04983
   - Uso no artigo: exemplo recente que reformula o dual do SVM como QUBO e conecta kernels quanticos com otimizacao por annealing.
   - Status: usar como referencia recente, mas deixar claro que e preprint.

9. Glover, Kochenberger e Du (2019) - *A Tutorial on Formulating and Using QUBO Models*
   - Link: https://arxiv.org/abs/1811.11538
   - DOI arXiv: https://doi.org/10.48550/arXiv.1811.11538
   - Uso no artigo: base geral para explicar QUBO como modelo de otimizacao binaria quadratica.
   - Status: usar como apoio metodologico para QUBO.

10. Lucas (2014) - *Ising formulations of many NP problems*
    - Link: https://www.frontiersin.org/articles/10.3389/fphy.2014.00005/full
    - DOI: https://doi.org/10.3389/fphy.2014.00005
    - Uso no artigo: relacionar formulacoes Ising/QUBO a problemas combinatorios.
    - Status: opcional para reforcar QUBO/Ising.

## Otimizadores e ruido

11. Spall (1992) - *Multivariate stochastic approximation using a simultaneous perturbation gradient approximation*
    - Publicado em: IEEE Transactions on Automatic Control 37(3), 332-341 (1992)
    - DOI: https://doi.org/10.1109/9.119632
    - Uso no artigo: fonte classica do SPSA.
    - Status: usar se discutirmos SPSA conceitualmente.

12. Pellow-Jarman et al. (2021) - *A Comparison of Various Classical Optimizers for a Variational Quantum Linear Solver*
    - Link: https://arxiv.org/abs/2106.08682
    - Uso no artigo: comparar otimizadores em algoritmos variacionais e discutir ruido.
    - Status: opcional para discussao da Fase 1.

13. Singh, Mishra e Majumder (2022) - *Benchmarking of Different Optimizers in the Variational Quantum Algorithms for Applications in Quantum Chemistry*
    - Link: https://arxiv.org/abs/2208.10285
    - Uso no artigo: apoio recente para discutir diferenca entre simulador ideal e ambiente ruidoso.
    - Status: opcional.

## Fontes tecnicas de implementacao

14. Qiskit Optimization documentation
    - Link: https://qiskit-community.github.io/qiskit-optimization/
    - Uso no projeto: orientar conversao para `QuadraticProgram`, QUBO e solvers.
    - Status: usar como documentacao tecnica, nao necessariamente como referencia principal do artigo.

15. Qiskit Algorithms documentation
    - Link: https://qiskit-community.github.io/qiskit-algorithms/
    - Uso no projeto: orientar uso de QAOA, otimizadores e primitives.
    - Status: usar como documentacao tecnica.
