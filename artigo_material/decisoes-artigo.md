# Decisões atuais do artigo

Data: 2026-06-12

Este arquivo registra as decisões assumidas para avançar o artigo sem depender, neste momento, de novas buscas na EBSCO ou de novas execuções pesadas no Codespace.

## Autoria e contato

- Usar o e-mail acadêmico do autor: `julio.regino2@senaisp.edu.br`.
- Manter Julio Coronetti Regino como discente do curso de Análise e Desenvolvimento de Sistemas.
- Manter Cainã Antunes como orientador no bloco de autoria.
- Pendência real: confirmar o e-mail institucional do orientador e se o template/evento exige orientador como coautor, nota de rodapé ou agradecimento.

## Status dos resultados

Decisão recomendada: tratar os resultados como **resultados preliminares de um estudo exploratório**.

Justificativa:

- A formulação QUBO implementada é um classificador linear discretizado, não uma implementação completa do dual do SVM.
- O pipeline QUBO/QAOA funcionou em instâncias pequenas.
- O custo computacional cresceu rapidamente com o aumento de variáveis binárias.
- O Codespace não é adequado para rodadas QAOA pesadas.

Como escrever no artigo:

- Correto: "os resultados preliminares indicam viabilidade em pequena escala".
- Correto: "a formulação QUBO/QAOA apresentou limitação prática de custo no ambiente de simulação".
- Evitar: "o QAOA superou métodos clássicos".
- Evitar: "foi implementado um SVM-QUBO completo".

## Novos experimentos

Decisão recomendada: **não executar novos experimentos QAOA pesados agora**.

Resultados atuais suficientes para o artigo:

- Baseline SVM/VQC da Fase 1.
- QAOA/QUBO com PCA=2.
- QAOA/QUBO com PCA=3.
- Rodada exploratória QAOA/QUBO com PCA=4.
- QUBO exato com PCA 2, 3, 4 e 5.

Novos experimentos só devem ser executados se o orientador pedir explicitamente.

## Figuras e tabelas

Decisão recomendada: manter tabelas no corpo principal do artigo e usar os gráficos SVG como material de apoio.

Justificativa:

- O template LaTeX atual ainda não foi compilado.
- O Codespace não possui `pdflatex`, `biber` ou `latexmk`.
- SVG pode exigir conversão para PNG ou PDF no Overleaf.

Pendência real:

- Testar no Overleaf se o template aceita SVG.
- Se não aceitar, converter os gráficos para PNG/PDF.

## EBSCO

Decisão atual: a EBSCO foi usada como complemento da revisão de literatura, sem substituir as referências fundacionais.

O artigo possui referências fundacionais sobre:

- QAOA.
- NISQ.
- Algoritmos variacionais.
- Quantum machine learning.
- QUBO.
- SPSA.

Também foram incorporados artigos EBSCO sobre:

- VQA/QAOA para otimização combinatória.
- SVM como QUBO em classificação binária.
- Pré-processamento em QML.
- VQCs em alta dimensionalidade.
- Otimizadores em QML.
- Limitações de hardware real e sensibilidade de VQCs.

Pendência residual:

- Buscar artigos adicionais somente se o orientador pedir uma referência ainda mais específica sobre QAOA aplicado diretamente à classificação supervisionada.

Buscas futuras, se necessário:

- `"QAOA" AND "classification"`
- `"QUBO" AND "support vector machine"`
- `"quantum machine learning" AND "NISQ"`
- `"variational quantum algorithm" AND "optimizer"`

## Próxima ação recomendada

Levar o artigo ao Overleaf para compilar e identificar problemas reais de formatação. Depois disso, revisar apenas os erros concretos de LaTeX, referências e layout.
