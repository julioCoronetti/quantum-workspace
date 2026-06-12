# Checklist do artigo

## Planejamento

- [x] Definir tema, objetivos e hipotese norteadora em `contexto-ic.md`.
- [x] Estabilizar baseline VQC/SVM da Fase 1.
- [x] Registrar resultado da Fase 1 em `testes/teste-03.md`.
- [x] Criar pasta de apoio do artigo.
- [ ] Validar com o orientador a decisão de apresentar os resultados como estudo exploratório preliminar.

## Referencias

- [x] Separar referencias candidatas centrais.
- [ ] Confirmar no EBSCO/portal institucional quais referencias complementares serao usadas formalmente.
- [x] Remover referencias de exemplo do `referencias.bib` do template.
- [x] Migrar referencias fundacionais usadas para `template_artigo_congresso_unisenai/referencias.bib`.

## Experimentos

- [x] Baseline classico SVM e VQC simulado da Fase 1.
- [x] Implementar formulacao QUBO para o problema de classificacao.
- [x] Implementar pipeline QAOA/Qiskit Optimization.
- [x] Executar comparacao SVM classico vs. abordagem QAOA/QUBO.
- [x] Executar variacao preliminar de PCA com 2, 3, 4 e 5 componentes usando QUBO exato.
- [x] Definir resultados atuais como base preliminar/final do estudo exploratório.
- [x] Salvar resultados preliminares em CSV.
- [x] Gerar graficos preliminares para tempo e acuracia.

## Escrita

- [x] Definir titulo final em portugues e ingles.
- [ ] Confirmar e-mail do orientador e formato final da autoria no template do evento.
- [x] Escrever rascunho da Introducao.
- [x] Estruturar Revisao de Literatura com marcadores de citacao.
- [x] Substituir marcadores da Revisao por citacoes fundacionais verificadas.
- [ ] Complementar Revisao com artigos recentes da EBSCO.
- [x] Escrever Metodologia baseada nos scripts executados.
- [x] Escrever Resultados e Discussoes apenas com dados medidos.
- [x] Escrever Conclusao e trabalhos futuros.
- [x] Revisar resumo/abstract conforme decisão de estudo exploratório preliminar.
- [ ] Compilar o LaTeX em ambiente com `pdflatex` e `biber`.
