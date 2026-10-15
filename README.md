# quantum-workspace

Repositório da pesquisa de Iniciação Científica (UniSENAI): **Exploração do Algoritmo QAOA para Otimização em Modelos de Classificação Supervisionada utilizando Simuladores Quânticos**.

Compara classificadores clássicos (SVM linear) com abordagens quânticas variacionais (VQC) e combinatórias discretas (QUBO via QAOA e Solver Exato) utilizando o dataset *breast cancer* (*scikit-learn*) com redução dimensional via PCA.

---

## Estrutura do Repositório

```text
quantum-workspace/
├── experimentos/          # Scripts de computação quântica e machine learning
│   ├── script.py          # Fase 1: Baseline SVM vs VQC
│   ├── script_qaoa.py     # Fases 2 e 3: QUBO linear, QAOA e Solver Exato
│   └── gerar_graficos.py  # Geração das figuras vetoriais SVG
├── resultados/            # Dados empíricos brutos (.csv) e figuras (.svg)
├── publicacao/            # Manuscritos e editoração científica
│   ├── dist/              # Entregáveis finais (PDFs e DOCXs oficiais)
│   ├── geradores/         # Compiladores autônomos Python
│   ├── templates/         # Ativos gráficos e template institucional UniSENAI 2026
│   └── latex_original/    # Código-fonte LaTeX histórico e PDF de referência
├── pesquisa/              # Acervo de literatura e estado da arte
│   ├── ebsco/             # Metadados BibTeX exportados do EBSCO
│   └── planejamento/      # Checklists, notas e decisões metodológicas
├── testes/                # Logs e relatórios de execução técnica (01 a 06)
├── contexto-ic.md         # Escopo detalhado e contextualização da IC
└── requirements.txt       # Dependências de ambiente
```

---

## Dependências

Instale as dependências listadas em `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Execução dos Experimentos

### 1. Baseline Fase 1 (SVM vs VQC)
```bash
python3 experimentos/script.py
```

### 2. Formulação QUBO, QAOA e Solver Exato (Fases 2 e 3)
```bash
python3 experimentos/script_qaoa.py
```

### 3. Geração de Gráficos Vetoriais
```bash
python3 experimentos/gerar_graficos.py
```

---

## Compilação dos Documentos da Publicação

Os entregáveis finais são compilados de forma autônoma na pasta `publicacao/dist/`:

### Resumo Expandido (Submissão Oficial - 5 páginas)
```bash
python3 publicacao/geradores/gerar_resumo_expandido_pdf.py
python3 publicacao/geradores/gerar_resumo_expandido.py
```

### Versão Completa da Pesquisa (Memória Técnica - 7 páginas)
```bash
python3 publicacao/geradores/gerar_artigo_completo_pdf.py
python3 publicacao/geradores/gerar_artigo_completo_docx.py
```
