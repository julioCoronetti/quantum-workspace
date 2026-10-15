import zipfile
import xml.etree.ElementTree as ET
import os

TEMPLATE_PATH = 'conversao/Template_ResumoExpandido2026.6bced2c68d504ba99fc5.docx'
OUTPUT_PATH = 'conversao/Resumo_Expandido_Julio_Regino_2026.docx'

def escape_xml(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))

def make_run(text, bold=False, italic=False, font_size=24, font_name="Arial"):
    rPr = []
    rPr.append(f'<w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
    if bold:
        rPr.append('<w:b/><w:bCs/>')
    if italic:
        rPr.append('<w:i/><w:iCs/>')
    rPr.append(f'<w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/>')
    rPr.append('<w:lang w:val="pt-BR"/>')
    rPr_xml = f"<w:rPr>{''.join(rPr)}</w:rPr>"
    return f'<w:r>{rPr_xml}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'

def make_p(runs, jc="both", first_line=708, space_after=120, line_spacing=360, pStyle=None, numPr=None, keepNext=False):
    pPr = []
    if pStyle:
        pPr.append(f'<w:pStyle w:val="{pStyle}"/>')
    if keepNext:
        pPr.append('<w:keepNext/>')
    if numPr:
        pPr.append(numPr)
    if jc:
        pPr.append(f'<w:jc w:val="{jc}"/>')
    
    ind_attrs = []
    if first_line:
        ind_attrs.append(f'w:firstLine="{first_line}"')
    if ind_attrs:
        pPr.append(f'<w:ind {" ".join(ind_attrs)}/>')
        
    sp_attrs = []
    if space_after is not None:
        sp_attrs.append(f'w:after="{space_after}"')
    if line_spacing:
        sp_attrs.append(f'w:line="{line_spacing}" w:lineRule="auto"')
    if sp_attrs:
        pPr.append(f'<w:spacing {" ".join(sp_attrs)}/>')
        
    pPr_xml = f"<w:pPr>{''.join(pPr)}</w:pPr>"
    runs_xml = ''.join(runs)
    return f'<w:p>{pPr_xml}{runs_xml}</w:p>'

def make_heading_1(text, num=True, num_val="2"):
    num_xml = f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num_val}"/></w:numPr>' if num else ''
    r = make_run(text, bold=True, font_size=24, font_name="Arial")
    return make_p([r], jc="both", first_line=0, space_after=180, line_spacing=360, pStyle="Ttulo1", numPr=num_xml, keepNext=True)

def make_heading_2(text):
    num_xml = '<w:numPr><w:ilvl w:val="1"/><w:numId w:val="2"/></w:numPr>'
    r = make_run(text, bold=True, font_size=24, font_name="Arial")
    return make_p([r], jc="both", first_line=0, space_after=120, line_spacing=360, pStyle="Ttulo2", numPr=num_xml, keepNext=True)

def make_table(headers, rows, caption_text):
    caption = make_p([make_run(caption_text, bold=True, font_size=20)], jc="both", first_line=0, space_after=60, line_spacing=240, keepNext=True)
    
    tbl_xml = []
    tbl_xml.append('<w:tbl>')
    tbl_xml.append('<w:tblPr>')
    tbl_xml.append('<w:tblStyle w:val="Tabelacomgrade"/>')
    tbl_xml.append('<w:tblW w:w="0" w:type="auto"/>')
    tbl_xml.append('<w:jc w:val="center"/>')
    tbl_xml.append('<w:tblBorders>')
    tbl_xml.append('<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>')
    tbl_xml.append('<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>')
    tbl_xml.append('<w:left w:val="none"/>')
    tbl_xml.append('<w:right w:val="none"/>')
    tbl_xml.append('<w:insideH w:val="none"/>')
    tbl_xml.append('<w:insideV w:val="none"/>')
    tbl_xml.append('</w:tblBorders>')
    tbl_xml.append('</w:tblPr>')
    
    tbl_xml.append('<w:tr>')
    for h in headers:
        tbl_xml.append('<w:tc>')
        tbl_xml.append('<w:tcPr>')
        tbl_xml.append('<w:tcBorders><w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/></w:tcBorders>')
        tbl_xml.append('</w:tcPr>')
        p = make_p([make_run(h, bold=True, font_size=20)], jc="center", first_line=0, space_after=40, line_spacing=240)
        tbl_xml.append(p)
        tbl_xml.append('</w:tc>')
    tbl_xml.append('</w:tr>')
    
    for row in rows:
        tbl_xml.append('<w:tr>')
        for idx, cell in enumerate(row):
            tbl_xml.append('<w:tc>')
            jc = "left" if idx == 0 and len(cell) > 5 else "center"
            p = make_p([make_run(cell, bold=False, font_size=20)], jc=jc, first_line=0, space_after=30, line_spacing=240)
            tbl_xml.append(p)
            tbl_xml.append('</w:tc>')
        tbl_xml.append('</w:tr>')
        
    tbl_xml.append('</w:tbl>')
    
    space_after_tbl = make_p([make_run("", font_size=12)], jc="both", first_line=0, space_after=120, line_spacing=240)
    return caption + ''.join(tbl_xml) + space_after_tbl

def build_footnotes_xml():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:footnotes xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" mc:Ignorable="w14">
  <w:footnote w:type="separator" w:id="-1">
    <w:p><w:r><w:separator/></w:r></w:p>
  </w:footnote>
  <w:footnote w:type="continuationSeparator" w:id="0">
    <w:p><w:r><w:continuationSeparator/></w:r></w:p>
  </w:footnote>
  <w:footnote w:id="1">
    <w:p>
      <w:pPr><w:pStyle w:val="Textodenotaderodap"/></w:pPr>
      <w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr><w:footnoteRef/></w:r>
      <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve"> Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, julio.regino2@senaisp.edu.br.</w:t></w:r>
    </w:p>
  </w:footnote>
  <w:footnote w:id="2">
    <w:p>
      <w:pPr><w:pStyle w:val="Textodenotaderodap"/></w:pPr>
      <w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr><w:footnoteRef/></w:r>
      <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve"> Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, caina.silva@sp.senai.br.</w:t></w:r>
    </w:p>
  </w:footnote>
</w:footnotes>'''

def build_document_xml():
    body_elements = []

    # Title PT (Bold, centered, all caps)
    body_elements.append(make_p(
        [make_run("EXPLORAÇÃO DO ALGORITMO QAOA PARA OTIMIZAÇÃO EM MODELOS DE CLASSIFICAÇÃO SUPERVISIONADA UTILIZANDO SIMULADORES QUÂNTICOS", bold=True, font_size=24)],
        jc="center", first_line=0, space_after=120, line_spacing=280
    ))
    
    # Title EN (Bold, centered, all caps)
    body_elements.append(make_p(
        [make_run("EXPLORATION OF THE QAOA ALGORITHM FOR OPTIMIZATION IN SUPERVISED CLASSIFICATION MODELS USING QUANTUM SIMULATORS", bold=True, font_size=24)],
        jc="center", first_line=0, space_after=240, line_spacing=280
    ))

    # Authors with footnotes
    author_runs = [
        make_run("Julio Coronetti Regino", bold=True, font_size=24),
        '<w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:footnoteReference w:id="1"/></w:r>',
        make_run(", ", bold=False, font_size=24),
        make_run("Cainã Antunes", bold=True, font_size=24),
        '<w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:footnoteReference w:id="2"/></w:r>'
    ]
    body_elements.append(make_p(author_runs, jc="both", first_line=0, space_after=240, line_spacing=280))

    # RESUMO
    body_elements.append(make_p([make_run("RESUMO", bold=True, font_size=24)], jc="both", first_line=0, space_after=80, line_spacing=300))
    resumo_text = ("Este estudo investiga a viabilidade de formulações de otimização combinatória quadrática associadas ao algoritmo QAOA em tarefas de classificação supervisionada binária, utilizando simuladores quânticos e confronto com métodos clássicos. O procedimento experimental empregou a base breast cancer da biblioteca scikit-learn, dividida de forma estratificada em treino (70%) e teste (30%). O pré-processamento consistiu em padronização por escore Z, redução dimensional por PCA e normalização linear no intervalo [0, 1]. Inicialmente, estabeleceu-se um controle comparativo formado por um classificador SVM linear clássico e um modelo VQC simulado. Em seguida, implementou-se uma formulação QUBO de classificador linear discretizado, resolvida via QAOA em instâncias de 2 a 4 componentes principais e por solver exato até 5 componentes. O baseline clássico SVM alcançou 100,00% de acurácia em 0,0009 s, enquanto o VQC obteve 83,33% em 12,81 s. Na abordagem QUBO resolvida com QAOA, a instância com 2 componentes atingiu 90,00% de acurácia em 3,70 s, e a instância com 4 componentes obteve 96,67% em 863,42 s, decorrente de flutuação amostral no limiar de decisão sobre o teste. Os resultados confirmam a convergência funcional do modelo em pequena escala e evidenciam o crescimento exponencial do tempo de simulação frente ao espaço combinatório de busca.")
    body_elements.append(make_p([make_run(resumo_text, font_size=24)], jc="both", first_line=0, space_after=80, line_spacing=300))
    
    kw_pt = [make_run("Palavras-chave: ", bold=True, font_size=24), make_run("QAOA; QUBO; classificação supervisionada; aprendizado de máquina quântico; simuladores quânticos.", font_size=24)]
    body_elements.append(make_p(kw_pt, jc="both", first_line=0, space_after=200, line_spacing=300))

    # ABSTRACT
    body_elements.append(make_p([make_run("ABSTRACT", bold=True, font_size=24)], jc="both", first_line=0, space_after=80, line_spacing=300))
    abstract_text = ("This study investigates the feasibility of quadratic combinatorial optimization formulations combined with the QAOA algorithm in binary supervised classification tasks, using quantum simulators and comparison with classical baselines. The experimental procedure employed the breast cancer dataset from scikit-learn, split with stratification into training (70%) and testing (30%) subsets. Preprocessing consisted of Z-score standardization, PCA dimensionality reduction, and linear min-max scaling to the [0, 1] interval. Initially, a comparative baseline was established with a classical linear SVM and a simulated VQC. Subsequently, a discretized linear classifier was formulated as a QUBO problem, solved via QAOA for instances with 2 to 4 principal components and via an exact solver up to 5 components. The classical SVM achieved 100.00% accuracy in 0.0009 s, while VQC achieved 83.33% in 12.81 s. In the QUBO formulation solved by QAOA, the 2-component instance reached 90.00% accuracy in 3.70 s, and the 4-component instance reached 96.67% in 863.42 s due to sampling boundary fluctuations on the test split. The findings confirm functional convergence in small instances and highlight exponential simulation overhead across the combinatorial search space.")
    body_elements.append(make_p([make_run(abstract_text, italic=False, font_size=24)], jc="both", first_line=0, space_after=80, line_spacing=300))

    kw_en = [make_run("Keywords: ", bold=True, font_size=24), make_run("QAOA; QUBO; supervised classification; quantum machine learning; quantum simulators.", italic=False, font_size=24)]
    body_elements.append(make_p(kw_en, jc="both", first_line=0, space_after=240, line_spacing=300))

    # 1 INTRODUÇÃO (matching template structure)
    body_elements.append(make_heading_1("1 INTRODUÇÃO", num=False))
    body_elements.append(make_p([make_run(
        "A computação quântica possibilita novas abordagens para a modelagem de problemas de otimização combinatória e aprendizado de máquina. No estágio atual do desenvolvimento de hardware, denominado era NISQ (Noisy Intermediate-Scale Quantum), os dispositivos físicos possuem número limitado de qubits suscetíveis a ruído e decoerência, restringindo a profundidade viável dos circuitos (Preskill, 2018; Bharti et al., 2022). Diante dessas características físicas, os algoritmos híbridos variacionais clássico-quânticos consolidaram-se como metodologia prática para investigação empírica, distribuindo as etapas computacionais entre processadores quânticos parametrizados e rotinas clássicas de otimização (Cerezo et al., 2021; Grange; Poss; Bourreau, 2024)."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))

    body_elements.append(make_heading_2("1.1 Problema de pesquisa"))
    body_elements.append(make_p([make_run(
        "A transposição de algoritmos de aprendizado supervisionado para ambientes quânticos requer o mapeamento de funções de custo em operadores Hamiltonianos tratáveis. Em simulações clássicas de circuitos quânticos, a exigência de memória e processamento cresce exponencialmente com o número de variáveis de estado. O problema investigado consiste em determinar a viabilidade técnica e os custos operacionais da modelagem de tarefas de classificação supervisionada sob a estrutura de Otimização Binária Quadrática Irrestrita (QUBO), avaliada por meio do algoritmo QAOA em simuladores de vetores de estado."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))

    body_elements.append(make_heading_2("1.2 Objetivo(s)"))
    body_elements.append(make_p([make_run(
        "O objetivo geral deste trabalho é avaliar o desempenho do algoritmo QAOA na resolução de tarefas de classificação supervisionada binária formuladas como QUBO, confrontando acurácia e tempo de processamento com modelos clássicos (SVM) e variacionais (VQC). Especificamente, busca-se: 1) Formular a tarefa de classificação binária como um problema de otimização quadrática discreta; 2) Avaliar a convergência do QAOA em instâncias de baixa dimensionalidade; 3) Medir comparativamente métricas de acurácia e tempo de execução; 4) Analisar a escalabilidade computacional frente ao acréscimo de atributos gerados por PCA."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))

    body_elements.append(make_heading_2("1.3 Justificativa"))
    body_elements.append(make_p([make_run(
        "O algoritmo QAOA (Quantum Approximate Optimization Algorithm) foi concebido para aproximar soluções em problemas combinatórios discretos (Farhi; Goldstone; Gutmann, 2014). Embora a classificação linear convencional seja solucionada por programação matemática contínua, a conversão para formulações QUBO permite investigar o comportamento de amostradores quânticos aplicados à minimização de erros de predição (Glover; Kochenberger; Du, 2019; Lucas, 2014). O foco da investigação reside em caracterizar a acurácia alcançável e a dinâmica de custo computacional dessa abordagem em cenários reduzidos, estabelecendo parâmetros empíricos sobre a viabilidade de execução em plataformas de simulação clássica."
    )], jc="both", first_line=708, space_after=180, line_spacing=360))

    # 2 REVISÃO DE LITERATURA (continuous flow matching template structure)
    body_elements.append(make_heading_1("2 REVISÃO DE LITERATURA", num=False))
    body_elements.append(make_p([make_run(
        "O paradigma variacional constitui a base operacional dos algoritmos para sistemas quânticos intermediários, estruturando a avaliação do estado quântico em circuitos parametrizados e o ajuste de ângulos por algoritmos de otimização clássicos (Preskill, 2018; Bharti et al., 2022; Cerezo et al., 2021). Investigações empíricas recentes sobre processadores físicos e simulados mostram que a fidelidade das portas lógicas e a conectividade física entre qubits condicionam a estabilidade dos modelos, demandando circuitos de baixa profundidade e controle rigoroso de ruídos de amostragem (Singh; Vishwakarma, 2026; Park; Son, 2026). Nesse contexto, Grange, Poss e Bourreau (2024) sistematizam o emprego de algoritmos variacionais na resolução de problemas combinatórios mapeados para matrizes de interação de spin."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))
    body_elements.append(make_p([make_run(
        "O funcionamento do QAOA fundamenta-se na aplicação alternada de operadores de custo e operadores de mistura sobre uma superposição homogênea de estados (Farhi; Goldstone; Gutmann, 2014). O operador de custo reflete os termos da função objetivo booleana no circuito, enquanto o operador de mistura promove a transição entre estados da base computacional. O número de camadas do circuito controla a precisão da aproximação assintótica, sendo adotada a configuração unitária de uma camada em experimentos de simulação para limitar a complexidade temporal e atenuar a dispersão do gradiente durante o ajuste numérico."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))
    body_elements.append(make_p([make_run(
        "No aprendizado de máquina quântico, a classificação baseia-se no mapeamento de vetores de atributos para espaços de Hilbert de alta dimensionalidade por meio de portas unitárias parametrizadas (Schuld; Killoran, 2019; Havlíček et al., 2019). Em revisão sistemática, Sood e Agrewal (2024) documentam que as abordagens predominantes envolvem classificadores variacionais e métodos de kernel quântico inspirados em Support Vector Machines (Rebentrost; Mohseni; Lloyd, 2014). A adaptação dessas arquiteturas para o domínio combinatório requer a discretização dos pesos do modelo, transpondo os coeficientes contínuos para um conjunto finito de variáveis binárias."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))
    body_elements.append(make_p([make_run(
        "A compressão prévia dos atributos é apontada pela literatura como condição para viabilizar simulações quânticas com contagem controlada de qubits. Mancilla e Pere (2022) demonstram que a redução dimensional por Análise de Componentes Principais (PCA) atenua o custo de amostragem em rotinas de classificação quântica. De forma convergente, Qi et al. (2025) reportam que a elevação no número de atributos demanda acréscimo proporcional de qubits e sobrecarrega a convergência em modelos variacionais. Adicionalmente, a literatura reporta que o comportamento dos algoritmos variacionais depende diretamente do otimizador clássico selecionado (AL Ajmi; Shoaib, 2025). O método SPSA (Simultaneous Perturbation Stochastic Approximation), desenvolvido por Spall (1992), destaca-se em ambientes sujeitos a ruído por estimar o gradiente com número constante de avaliações da função objetivo, enquanto rotinas determinísticas baseadas em simplex, como o COBYLA, apresentam bom desempenho em superfícies suaves de baixa dimensão."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))
    body_elements.append(make_p([make_run(
        "O modelo QUBO consiste na minimização irrestrita de funções quadráticas sobre vetores binários, correspondendo diretamente à formulação do vidro de spin de Ising (Glover; Kochenberger; Du, 2019; Lucas, 2014). Trabalhos recentes investigam o mapeamento de classificadores SVM para QUBO como mecanismo de exploração híbrida (Guddanti et al., 2024). Essa modelagem discretiza os parâmetros do hiperplano de separação e permite submeter a matriz de penalidades resultante a algoritmos quânticos de busca aproximada."
    )], jc="both", first_line=708, space_after=180, line_spacing=360))

    # 3 METODOLOGIA (matching template title case)
    body_elements.append(make_heading_1("3 METODOLOGIA", num=False))
    body_elements.append(make_p([make_run(
        "O experimento foi desenvolvido em linguagem Python, com base nos pacotes scikit-learn, Qiskit, Qiskit Machine Learning e Qiskit Optimization. A infraestrutura de testes foi estruturada em dois módulos analíticos: o módulo de calibração de baselines, composto por SVM linear clássico e classificador variacional quântico (VQC) simulado, e o módulo de otimização combinatória, responsável pela formulação QUBO e execuções via QAOA e solver exato."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))
    body_elements.append(make_p([make_run(
        "Utilizou-se o conjunto de dados breast cancer da biblioteca scikit-learn. Extraiu-se uma amostra estratificada de 100 registros, preservando a proporção original das classes. A amostra foi segmentada em 70% para treinamento e 30% para teste com semente pseudoaleatória controlada. O protocolo de pré-processamento compreendeu três etapas encadeadas: 1) Padronização por escore Z via StandardScaler, com parâmetros ajustados estritamente sobre a partição de treino; 2) Redução dimensional por PCA, calculando as direções principais apenas com dados de treino; 3) Normalização linear no intervalo [0, 1] através do operador MinMaxScaler. Esse fluxo impediu vazamento de dados de teste para a etapa de ajuste dos modelos."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))
    body_elements.append(make_p([make_run(
        "O modelo clássico de referência consistiu em um SVM com kernel linear. Em paralelo, implementou-se um circuito VQC simulado composto pelo mapa de características ZZFeatureMap, ansatz variacional RealAmplitudes e otimizador SPSA configurado com 100 iterações. Esse modelo forneceu o referencial quântico variacional inicial antes da transição para a abordagem combinatória."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))
    body_elements.append(make_p([make_run(
        "No módulo de otimização combinatória, a tarefa de classificação binária foi modelada como um classificador linear discretizado. Os coeficientes angulares de cada componente e o termo independente de viés foram representados por pares de variáveis binárias que refletem contribuições positivas e negativas. Para uma dimensão de d componentes principais, o sistema resultou em n_bin = 2(d + 1) variáveis booleanas. A função objetivo minimizada adotou o critério de erro quadrático de margem: (1 / n) * ∑ (b + x_i · w - y_i)², onde b representa o viés discretizado, w é o vetor de pesos binários, x_i denota o vetor de atributos normalizados e y_i ∈ {-1, +1} o rótulo de classe. Incorporou-se à matriz termos de regularização quadrática sobre a amplitude dos pesos e penalidades diagonais cruzadas para impedir a ativação simultânea de bits positivos e negativos pertencentes ao mesmo coeficiente."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))
    body_elements.append(make_p([make_run(
        "O problema QUBO foi solucionado pelo QAOA com o operador StatevectorSampler, uma repetição (p = 1) e otimizador COBYLA. Para fins de controle da formulação matemática, desenvolveu-se também um resolvedor exato por enumeração exaustiva de estados, aplicado às instâncias de 2 a 5 componentes principais (2⁶ a 2¹² estados). Registraram-se as variáveis de acurácia no conjunto de teste independente, tempo de execução em segundos, quantidade de componentes PCA e número de variáveis binárias."
    )], jc="both", first_line=708, space_after=180, line_spacing=360))

    # 4 RESULTADOS E DISCUSSÕES
    body_elements.append(make_heading_1("4 RESULTADOS E DISCUSSÕES", num=False))
    body_elements.append(make_p([make_run(
        "A Tabela 1 apresenta os resultados obtidos na etapa de calibração dos baselines. O SVM clássico linear atingiu 100,00% de acurácia no conjunto de teste em 0,0009 segundos. O classificador VQC simulado alcançou acurácia de 83,33% em 12,8098 segundos. Esse índice confirmou a capacidade do circuito variacional com emaranhamento em ajustar uma fronteira de separação eficaz, embora exigindo tempo computacional expressivamente superior ao método clássico."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))

    # Table 1
    t1_headers = ["Modelo", "Acurácia", "Tempo"]
    t1_rows = [
        ["SVM linear", "100,00%", "0,0009 s"],
        ["VQC simulado", "83,33%", "12,8098 s"]
    ]
    body_elements.append(make_table(t1_headers, t1_rows, "Tabela 1: Resultado comparativo do baseline experimental."))

    body_elements.append(make_p([make_run(
        "Na formulação QUBO com 2 componentes de PCA (Tabela 2), totalizando 6 variáveis binárias, o algoritmo QAOA convergiu em 3,6997 segundos com acurácia de 90,00% no conjunto de teste, enquanto o SVM linear manteve 100,00%. O resultado atesta que a discretização de parâmetros em variáveis booleanas preserva a capacidade discriminativa essencial da fronteira de classificação em dimensões reduzidas."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))

    # Table 2
    t2_headers = ["Modelo", "Variáveis binárias", "Acurácia", "Tempo"]
    t2_rows = [
        ["SVM linear", "0", "100,00%", "0,0013 s"],
        ["QAOA-QUBO linear", "6", "90,00%", "3,6997 s"]
    ]
    body_elements.append(make_table(t2_headers, t2_rows, "Tabela 2: Desempenho do QAOA em formulação QUBO com 2 componentes principais."))

    body_elements.append(make_p([make_run(
        "A Tabela 3 consolida a avaliação da formulação QUBO utilizando o solver exato em instâncias de 2 a 5 componentes PCA. A acurácia manteve-se constante em 90,00% em todas as configurações testadas. O tempo necessário para a busca global aumentou progressivamente de 0,0824 segundos (6 variáveis, 64 estados) para 7,1497 segundos (12 variáveis, 4096 estados). A estabilidade do índice de acerto evidencia que a formulação quadrática discreta retém a consistência da solução, transferindo o gargalo operacional para o custo combinatório do espaço de busca."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))

    # Table 3
    t3_headers = ["PCA", "Variáveis binárias", "Acurácia QUBO", "Tempo QUBO"]
    t3_rows = [
        ["2", "6", "90,00%", "0,0824 s"],
        ["3", "8", "90,00%", "0,4580 s"],
        ["4", "10", "90,00%", "1,2578 s"],
        ["5", "12", "90,00%", "7,1497 s"]
    ]
    body_elements.append(make_table(t3_headers, t3_rows, "Tabela 3: Avaliação por solver exato da formulação QUBO sob variação de componentes PCA."))

    body_elements.append(make_p([make_run(
        "A Tabela 4 detalha as execuções do algoritmo QAOA conforme o aumento da dimensão de entrada. O tempo de emulação quântica elevou-se para 41,7146 segundos com 3 componentes (8 variáveis) e alcançou 863,4231 segundos com 4 componentes (10 variáveis binárias, correspondendo a 1024 estados quânticos). Na instância com 4 componentes, a latência de cálculo impôs a redução do parâmetro de iterações do COBYLA de 20 para 5 iterações."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))

    # Table 4
    t4_headers = ["PCA", "Variáveis binárias", "Maxiter", "Acurácia QAOA", "Tempo QAOA"]
    t4_rows = [
        ["2", "6", "20", "90,00%", "3,6997 s"],
        ["3", "8", "20", "90,00%", "41,7146 s"],
        ["4", "10", "5", "96,67%", "863,4231 s"]
    ]
    body_elements.append(make_table(t4_headers, t4_rows, "Tabela 4: Desempenho do algoritmo QAOA sob escalonamento de componentes PCA."))

    body_elements.append(make_p([make_run(
        "Observa-se que na configuração com 4 componentes PCA, a acurácia no conjunto de teste alcançou 96,67% (29 acertos em 30 amostras), superando a taxa de 90,00% obtida pelo solver exato. Esse comportamento decorre da discretização dos pesos em um conjunto finito de valores e da sensibilidade do hiperplano de separação na partição de teste reduzida (30 instâncias): enquanto o solver exato minimizou estritamente a função de perda quadrática global sobre os dados de treino, a solução aproximada encontrada pelo QAOA gerou um deslocamento pontual do limiar de decisão que, fortuitamente, classificou corretamente duas amostras limítrofes adicionais no teste, caracterizando flutuação amostral."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))

    body_elements.append(make_p([make_run(
        "A correlação entre as séries de teste reflete a distinção entre convergência funcional e escalabilidade computacional em simuladores de vetor de estado. Embora o QAOA tenha demonstrado capacidade de convergência em pequenas dimensões, a multiplicação matricial emulada em processadores clássicos sofre rápido decaimento de desempenho à medida que o número de variáveis cresce. O índice de 100,00% obtido pelo SVM clássico associa-se à separabilidade linear favorável proporcionada pelo PCA na amostra de 100 dados, indicando a conveniência de validações cruzadas adicionais em bases maiores. Esses padrões corroboram as análises de Qi et al. (2025), Park e Son (2026) e Singh e Vishwakarma (2026) quanto ao custo de profundidade e dimensionamento de variáveis quânticas."
    )], jc="both", first_line=708, space_after=180, line_spacing=360))

    # 5 Conclusão (matching template title case)
    body_elements.append(make_heading_1("5 Conclusão", num=False))
    body_elements.append(make_p([make_run(
        "Este trabalho avaliou a aplicação do algoritmo QAOA na otimização de modelos de classificação supervisionada binária sob modelagem QUBO em ambientes de simulação quântica. Os resultados obtidos confirmam a viabilidade funcional da formulação em pequenas instâncias, alcançando taxas de acurácia de 90,00% com 2 componentes principais e 96,67% com 4 componentes no conjunto de teste."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))
    body_elements.append(make_p([make_run(
        "A contribuição da pesquisa reside na caracterização prática do pipeline de discretização de classificadores lineares em sistemas quadráticos binários e na mensuração empírica do tempo de execução emulado. A comparação com baselines clássicos evidencia que o SVM linear permanece como solução significativamente mais rápida em infraestruturas tradicionais. A rápida elevação temporal do QAOA sob emulação clássica delimita o gargalo de simulação frente à expansão do espaço combinatório."
    )], jc="both", first_line=708, space_after=120, line_spacing=360))
    body_elements.append(make_p([make_run(
        "Trabalhos futuros devem aprofundar formulações baseadas no problema dual exato do SVM, investigar técnicas de relaxação contínua para discretização e avaliar a execução dos circuitos em processadores quânticos físicos ou ambientes simulados com perfis específicos de ruído."
    )], jc="both", first_line=708, space_after=180, line_spacing=360))

    # Referências (matching template title case, unnumbered)
    body_elements.append(make_heading_1("Referências", num=False))
    refs = [
        "AL AJMI, Nouf Ali; SHOAIB, Muhammad. Optimization Strategies in Quantum Machine Learning: A Performance Analysis. Applied Sciences (2076-3417), v. 15, n. 8, p. 4493, 2025. ISSN 20763417. Disponível em: https://research.ebsco.com/plink/3e7e0c3c-679b-3f4b-9386-85a706fd46a7.",
        "BHARTI, Kishor et al. Noisy intermediate-scale quantum algorithms. Reviews of Modern Physics, v. 94, n. 1, p. 015004, 2022. DOI: 10.1103/RevModPhys.94.015004.",
        "CEREZO, M. et al. Variational quantum algorithms. Nature Reviews Physics, v. 3, p. 625–644, 2021. DOI: 10.1038/s42254-021-00348-9.",
        "FARHI, Edward; GOLDSTONE, Jeffrey; GUTMANN, Sam. A Quantum Approximate Optimization Algorithm. [S. l.: s. n.], 2014. DOI: 10.48550/arXiv.1411.4028. arXiv: 1411.4028 [quant-ph].",
        "GLOVER, Fred; KOCHENBERGER, Gary; DU, Yu. A Tutorial on Formulating and Using QUBO Models. [S. l.: s. n.], 2019. DOI: 10.48550/arXiv.1811.11538. arXiv: 1811.11538 [cs.DS].",
        "GRANGE, Camille; POSS, Michael; BOURREAU, Eric. An introduction to variational quantum algorithms for combinatorial optimization problems. Annals of Operations Research, v. 343, n. 2, p. 847–884, 2024. ISSN 02545330. Disponível em: https://research.ebsco.com/plink/5db591f8-71aa-368f-b7cd-7838eab941d5.",
        "GUDDANTI, Sai Sakunthala et al. Pneumonia detection by binary classification: classical, quantum, and hybrid approaches for support vector machine (SVM). Frontiers in Computer Science, v. 5, 2024. ISSN 26249898. Disponível em: https://research.ebsco.com/plink/1060a67e-2766-36ff-9ebf-39f6532995c6.",
        "HAVLÍČEK, Vojtěch et al. Supervised learning with quantum-enhanced feature spaces. Nature, v. 567, p. 209–212, 2019. DOI: 10.1038/s41586-019-0980-2.",
        "LUCAS, Andrew. Ising formulations of many NP problems. Frontiers in Physics, v. 2, p. 5, 2014. DOI: 10.3389/fphy.2014.00005.",
        "MANCILLA, Javier; PERE, Christophe. A Preprocessing Perspective for Quantum Machine Learning Classification Advantage in Finance Using NISQ Algorithms. Entropy, v. 24, n. 11, p. 1656, 2022. ISSN 10994300. Disponível em: https://research.ebsco.com/plink/51742d2e-df02-365d-92e6-498f5ca8d671.",
        "PARK, Seungun; SON, Yunsik. Sensitivity Analysis of Variational Quantum Classifiers for Identifying Dummy Power Traces in Side-Channel Analysis. Applied Sciences (2076-3417), v. 16, n. 7, p. 3243, 2026. ISSN 20763417. Disponível em: https://research.ebsco.com/plink/29be799f-895e-3701-894a-710a41299b9d.",
        "PRESKILL, John. Quantum Computing in the NISQ era and beyond. Quantum, v. 2, p. 79, 2018. DOI: 10.22331/q-2018-08-06-79.",
        "QI, Han et al. A high-efficiency variational quantum classifier for high-dimensional data. Journal of Supercomputing, v. 81, n. 1, p. 1–20, 2025. ISSN 09208542. Disponível em: https://research.ebsco.com/plink/dfae7ab3-6bc0-38d5-804a-d2c66fa2bdee.",
        "REBENTROST, Patrick; MOHSENI, Masoud; LLOYD, Seth. Quantum support vector machine for big data classification. Physical Review Letters, v. 113, p. 130503, 2014. DOI: 10.1103/PhysRevLett.113.130503.",
        "SCHULD, Maria; KILLORAN, Nathan. Quantum Machine Learning in Feature Hilbert Spaces. Physical Review Letters, v. 122, p. 040504, 2019. DOI: 10.1103/PhysRevLett.122.040504.",
        "SINGH, Sumitra; VISHWAKARMA, Dinesh Kumar. Performance Analysis of Quantum Arithmetic Circuits on IBM Eagle Processor. Defence Science Journal, v. 76, n. 2, p. 233–241, 2026. ISSN 0011-748X. Disponível em: https://research.ebsco.com/plink/434534d9-2076-32a7-86ab-e90a24e06b17.",
        "SOOD, Sandeep Kumar; AGREWAL, Monika. Quantum Machine Learning for Computational Methods in Engineering: A Systematic Review. Archives of Computational Methods in Engineering, v. 31, n. 3, p. 1555–1577, 2024. ISSN 11343060. Disponível em: https://research.ebsco.com/plink/ad938df6-0f8a-30be-9aff-61759dcec81a.",
        "SPALL, James C. Multivariate stochastic approximation using a simultaneous perturbation gradient approximation. IEEE Transactions on Automatic Control, v. 37, n. 3, p. 332–341, 1992. DOI: 10.1109/9.119632."
    ]
    for ref in refs:
        body_elements.append(make_p([make_run(ref, font_size=24)], jc="both", first_line=0, space_after=120, line_spacing=240))

    # AGRADECIMENTOS (bold, all caps, unnumbered)
    body_elements.append(make_heading_1("AGRADECIMENTOS", num=False))
    body_elements.append(make_p([make_run(
        "Agradece-se ao SENAI pelo apoio institucional ao desenvolvimento desta iniciação científica."
    )], jc="both", first_line=708, space_after=180, line_spacing=360))

    # SOBRE O(S)AUTOR(ES) (matching template exact naming: no space between O(S) and AUTOR)
    body_elements.append(make_heading_1("SOBRE O(S)AUTOR(ES)", num=False))
    body_elements.append(make_p([make_run("Sobre os autores:", bold=True, font_size=24)], jc="both", first_line=0, space_after=60, line_spacing=240))
    body_elements.append(make_p([make_run("_________________", bold=True, font_size=24)], jc="both", first_line=0, space_after=120, line_spacing=240))

    # Author 1 bio table
    body_elements.append(make_p([make_run("i Julio Coronetti Regino (Autor)", bold=True, font_size=24)], jc="both", first_line=0, space_after=60, line_spacing=240, pStyle="Textodenotadefim"))
    author1_bio = (
        '<w:tbl><w:tblPr><w:tblStyle w:val="Tabelacomgrade"/><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'
        '<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        '</w:tblBorders></w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="1418"/><w:gridCol w:w="7643"/></w:tblGrid>'
        '<w:tr><w:tc><w:tcPr><w:tcW w:w="1418" w:type="dxa"/></w:tcPr>'
        + make_p([make_run("Foto", font_size=20)], jc="center", first_line=0, space_after=0, line_spacing=240) +
        '</w:tc><w:tc><w:tcPr><w:tcW w:w="7643" w:type="dxa"/></w:tcPr>'
        + make_p([make_run("Discente do curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas na Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior. Desenvolve pesquisa de Iniciação Científica focada em algoritmos variacionais quânticos (QAOA, VQC) e otimização combinatória (QUBO) aplicados a machine learning. E-mail: julio.regino2@senaisp.edu.br.", font_size=22)], jc="both", first_line=0, space_after=0, line_spacing=280) +
        '</w:tc></w:tr></w:tbl>'
    )
    body_elements.append(author1_bio)

    body_elements.append(make_p([make_run("", font_size=12)], jc="both", first_line=0, space_after=60, line_spacing=240))

    # Author 2 bio table
    body_elements.append(make_p([make_run("ii Cainã Antunes (Orientador)", bold=True, font_size=24)], jc="both", first_line=0, space_after=60, line_spacing=240, pStyle="Textodenotadefim"))
    author2_bio = (
        '<w:tbl><w:tblPr><w:tblStyle w:val="Tabelacomgrade"/><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'
        '<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        '</w:tblBorders></w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="1418"/><w:gridCol w:w="7643"/></w:tblGrid>'
        '<w:tr><w:tc><w:tcPr><w:tcW w:w="1418" w:type="dxa"/></w:tcPr>'
        + make_p([make_run("Foto", font_size=20)], jc="center", first_line=0, space_after=0, line_spacing=240) +
        '</w:tc><w:tc><w:tcPr><w:tcW w:w="7643" w:type="dxa"/></w:tcPr>'
        + make_p([make_run("Docente e pesquisador na Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, atuando como orientador de projetos de iniciação científica e desenvolvimento tecnológico em inteligência artificial e computação avançada. E-mail: caina.silva@sp.senai.br.", font_size=22)], jc="both", first_line=0, space_after=0, line_spacing=280) +
        '</w:tc></w:tr></w:tbl>'
    )
    body_elements.append(author2_bio)

    # sectPr (preserves header1 with red wedge and footer1 with gray shape and cropped logo)
    sectPr = '<w:sectPr w:rsidR="0046777C" w:rsidRPr="00FF5642" w:rsidSect="00A223E8"><w:headerReference w:type="default" r:id="rId7"/><w:footerReference w:type="default" r:id="rId8"/><w:type w:val="continuous"/><w:pgSz w:w="11910" w:h="16840"/><w:pgMar w:top="1701" w:right="1134" w:bottom="1134" w:left="1701" w:header="720" w:footer="906" w:gutter="0"/><w:cols w:space="720"/></w:sectPr>'
    body_elements.append(sectPr)

    doc_header = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex" xmlns:cx1="http://schemas.microsoft.com/office/drawing/2015/9/8/chartex" xmlns:cx2="http://schemas.microsoft.com/office/drawing/2015/10/21/chartex" xmlns:cx3="http://schemas.microsoft.com/office/drawing/2016/5/9/chartex" xmlns:cx4="http://schemas.microsoft.com/office/drawing/2016/5/10/chartex" xmlns:cx5="http://schemas.microsoft.com/office/drawing/2016/5/11/chartex" xmlns:cx6="http://schemas.microsoft.com/office/drawing/2016/5/12/chartex" xmlns:cx7="http://schemas.microsoft.com/office/drawing/2016/5/13/chartex" xmlns:cx8="http://schemas.microsoft.com/office/drawing/2016/5/14/chartex" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:aink="http://schemas.microsoft.com/office/drawing/2016/ink" xmlns:am3d="http://schemas.microsoft.com/office/drawing/2017/model3d" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid" xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 w15 w16se w16cid wp14">
<w:body>'''

    doc_footer = '''</w:body></w:document>'''

    return doc_header + ''.join(body_elements) + doc_footer

def convert():
    print("Atualizando Resumo_Expandido_Julio_Regino_2026.docx com a estrutura exata do template...")
    new_doc_xml = build_document_xml()
    new_footnotes_xml = build_footnotes_xml()
    
    with zipfile.ZipFile(TEMPLATE_PATH, 'r') as zin:
        with zipfile.ZipFile(OUTPUT_PATH, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/document.xml':
                    zout.writestr(item, new_doc_xml.encode('utf-8'))
                elif item.filename == 'word/footnotes.xml':
                    zout.writestr(item, new_footnotes_xml.encode('utf-8'))
                else:
                    zout.writestr(item, zin.read(item.filename))
                    
    print(f"Sucesso! Arquivo .docx atualizado em: {OUTPUT_PATH}")

if __name__ == '__main__':
    convert()
