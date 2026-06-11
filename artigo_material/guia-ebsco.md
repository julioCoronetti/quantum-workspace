# Guia de busca na EBSCO para o artigo

Este arquivo serve como roteiro para buscar referencias academicas na plataforma EBSCO usando o acesso da faculdade.

## Ideia geral

A EBSCO deve ser usada para fortalecer a base academica do artigo com artigos revisados, metadados confiaveis, DOI e exportacao de citacoes. A ideia nao e descartar as referencias fundamentais ja separadas, mas complementar com pesquisas mais recentes e especificas.

As referencias fundacionais que continuam importantes sao:

- Farhi, Goldstone e Gutmann (2014), para QAOA.
- Preskill (2018), para a era NISQ.
- Cerezo et al. (2021), para algoritmos variacionais.
- Havlicek et al. (2019), para quantum machine learning aplicado a classificacao.
- Schuld e Killoran (2019), para feature maps quanticos.
- Glover, Kochenberger e Du (2019), para QUBO.

A EBSCO entra como camada adicional para encontrar artigos mais recentes, revisados e conectados diretamente ao recorte da IC.

## Filtros recomendados

Ao pesquisar na EBSCO, priorizar:

- Artigos revisados por pares, se houver filtro `Peer reviewed`.
- Publicacoes entre 2020 e 2026.
- Para revisao recente, priorizar 2023 a 2026.
- Artigos com DOI.
- Artigos de periodicos cientificos, quando houver essa opcao.
- Texto completo quando disponivel, mas DOI, resumo e metadados ja ajudam.
- Artigos em ingles, pois a area de computacao quantica tem maior volume de publicacao nesse idioma.

## Buscas principais

### QAOA e aprendizado de maquina

```text
"Quantum Approximate Optimization Algorithm" AND "machine learning"
```

Uso esperado no artigo:

- Introducao.
- Revisao de Literatura.
- Justificativa para usar QAOA como algoritmo de otimizacao.

### QAOA aplicado a classificacao

```text
"QAOA" AND ("classification" OR "supervised learning")
```

Uso esperado no artigo:

- Revisao de Literatura.
- Discussao sobre o quanto ja existe de aplicacao direta de QAOA em classificacao supervisionada.
- Identificacao de lacunas da pesquisa.

### QUBO e SVM

```text
"QUBO" AND ("support vector machine" OR "SVM")
```

Uso esperado no artigo:

- Revisao de Literatura.
- Metodologia.
- Justificativa para transformar classificacao em problema de otimizacao discreta.

### QUBO e machine learning

```text
"QUBO" AND "machine learning"
```

Uso esperado no artigo:

- Explicar a relacao entre modelos de aprendizado de maquina e formulacoes de otimizacao binaria.
- Encontrar exemplos parecidos com o caminho da IC.

### Quantum machine learning e classificacao

```text
"Quantum machine learning" AND "classification" AND "NISQ"
```

Uso esperado no artigo:

- Introducao.
- Revisao de Literatura.
- Contextualizacao de classificadores quanticos em dispositivos ou simuladores NISQ.

### Variational quantum classifier e otimizadores

```text
"Variational quantum classifier" AND ("SPSA" OR "COBYLA")
```

Uso esperado no artigo:

- Justificar a Fase 1.
- Discutir por que SPSA pode ser relevante em cenarios ruidosos.
- Comparar SPSA e COBYLA em simuladores ou ambientes NISQ.

### Otimizadores em algoritmos variacionais

```text
"variational quantum algorithm" AND ("SPSA" OR "COBYLA") AND "optimizer"
```

Uso esperado no artigo:

- Revisao de Literatura.
- Discussao sobre treinamento hibrido quantico-classico.
- Interpretacao dos resultados da Fase 1.

### Simuladores quanticos e escalabilidade

```text
"quantum simulator" AND ("scaling" OR "performance" OR "qubits")
```

Uso esperado no artigo:

- Discussao dos resultados.
- Justificativa para o aumento de tempo quando o numero de features/qubits cresce.
- Explicacao das limitacoes de simuladores em computadores classicos.

### PCA e reducao de dimensionalidade em QML

```text
"Quantum machine learning" AND ("PCA" OR "feature reduction")
```

Uso esperado no artigo:

- Metodologia.
- Justificativa para reduzir dimensionalidade antes de usar circuitos quanticos.
- Discussao sobre limitacoes de qubits e custo computacional.

## O que salvar de cada artigo

Para cada artigo promissor, salvar:

- Titulo.
- Autores.
- Ano.
- Nome do periodico ou conferencia.
- DOI.
- Link permanente.
- Resumo.
- 2 ou 3 frases dizendo por que o artigo serve para a IC.
- Arquivo `.bib` ou `.ris`, se a EBSCO permitir exportar.

## Como decidir se um artigo entra no trabalho

Um artigo deve entrar se ajudar em pelo menos uma destas funcoes:

- Explicar QAOA.
- Explicar a era NISQ e suas limitacoes.
- Relacionar computacao quantica com classificacao supervisionada.
- Justificar o uso de QUBO.
- Relacionar SVM ou classificacao com QUBO.
- Justificar o uso de PCA/reducao de dimensionalidade.
- Explicar otimizadores como SPSA e COBYLA.
- Sustentar a discussao sobre tempo de execucao e escalabilidade.

Evitar artigos que:

- Nao tenham relacao clara com QAOA, QUBO, SVM, classificacao ou QML.
- Falem de computacao quantica de forma muito generica.
- Nao tenham DOI ou informacoes bibliograficas confiaveis, a menos que sejam muito relevantes.
- Prometam vantagem quantica sem metodologia clara.

## Fluxo recomendado

1. Fazer as buscas principais na EBSCO.
2. Separar de 10 a 15 artigos candidatos.
3. Exportar as citacoes em `.bib` ou `.ris`.
4. Salvar os PDFs ou links permanentes, se disponiveis.
5. Trazer os arquivos para o workspace.
6. Classificar cada artigo por uso: Introducao, Revisao de Literatura, Metodologia ou Discussao.
7. Escolher apenas as referencias realmente citadas para migrar ao `referencias.bib` do template.

## Meta para o artigo

Uma boa selecao final deve ter aproximadamente:

- 2 ou 3 referencias fundacionais sobre QAOA/NISQ.
- 2 ou 3 referencias sobre quantum machine learning/classificacao.
- 2 referencias sobre QUBO/SVM ou QUBO/machine learning.
- 1 ou 2 referencias sobre otimizadores variacionais.
- 1 ou 2 referencias sobre simuladores, escalabilidade ou reducao de dimensionalidade.

Isso deve ser suficiente para uma Revisao de Literatura forte sem sobrecarregar o artigo.
