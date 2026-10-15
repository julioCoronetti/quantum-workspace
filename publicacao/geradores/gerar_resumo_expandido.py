import zipfile
import xml.etree.ElementTree as ET
import os

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_PATH = str(BASE_DIR / "templates" / "Template_ResumoExpandido2026.docx")
OUTPUT_PATH = str(BASE_DIR / "dist" / "Resumo_Expandido_Julio_Regino_2026.docx")

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

def make_p(runs, jc="both", first_line=708, space_after=100, line_spacing=300, pStyle=None, numPr=None, keepNext=False):
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
    return make_p([r], jc="both", first_line=0, space_after=120, line_spacing=300, pStyle="Ttulo1", numPr=num_xml, keepNext=True)

def make_table(headers, rows, caption_text):
    caption = make_p([make_run(caption_text, bold=True, font_size=20)], jc="both", first_line=0, space_after=50, line_spacing=240, keepNext=True)
    
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
        p = make_p([make_run(h, bold=True, font_size=19)], jc="center", first_line=0, space_after=30, line_spacing=220)
        tbl_xml.append(p)
        tbl_xml.append('</w:tc>')
    tbl_xml.append('</w:tr>')
    
    for row in rows:
        tbl_xml.append('<w:tr>')
        for idx, cell in enumerate(row):
            tbl_xml.append('<w:tc>')
            jc = "left" if idx == 0 and len(cell) > 5 else "center"
            p = make_p([make_run(cell, bold=False, font_size=19)], jc=jc, first_line=0, space_after=25, line_spacing=220)
            tbl_xml.append(p)
            tbl_xml.append('</w:tc>')
        tbl_xml.append('</w:tr>')
        
    tbl_xml.append('</w:tbl>')
    
    space_after_tbl = make_p([make_run("", font_size=12)], jc="both", first_line=0, space_after=80, line_spacing=200)
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
      <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve"> Discente, Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, julio.regino2@senaisp.edu.br.</w:t></w:r>
    </w:p>
  </w:footnote>
  <w:footnote w:id="2">
    <w:p>
      <w:pPr><w:pStyle w:val="Textodenotaderodap"/></w:pPr>
      <w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr><w:footnoteRef/></w:r>
      <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve"> Docente, Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, caina.silva@sp.senai.br.</w:t></w:r>
    </w:p>
  </w:footnote>
</w:footnotes>'''

def build_document_xml():
    body_elements = []

    body_elements.append(make_p(
        [make_run("EXPLORAÇÃO DO ALGORITMO QAOA PARA OTIMIZAÇÃO EM MODELOS DE CLASSIFICAÇÃO SUPERVISIONADA UTILIZANDO SIMULADORES QUÂNTICOS", bold=True, font_size=24)],
        jc="center", first_line=0, space_after=100, line_spacing=260
    ))
    
    body_elements.append(make_p(
        [make_run("EXPLORATION OF THE QAOA ALGORITHM FOR OPTIMIZATION IN SUPERVISED CLASSIFICATION MODELS USING QUANTUM SIMULATORS", bold=True, font_size=24)],
        jc="center", first_line=0, space_after=180, line_spacing=260
    ))

    author_runs = [
        make_run("Julio Coronetti Regino", bold=True, font_size=24),
        '<w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:footnoteReference w:id="1"/></w:r>',
        make_run(", ", bold=False, font_size=24),
        make_run("Cainã Antunes", bold=True, font_size=24),
        '<w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr><w:footnoteReference w:id="2"/></w:r>'
    ]
    body_elements.append(make_p(author_runs, jc="both", first_line=0, space_after=180, line_spacing=260))

    body_elements.append(make_p([make_run("RESUMO", bold=True, font_size=24)], jc="both", first_line=0, space_after=60, line_spacing=260))
    resumo_text = ("Este trabalho avalia a formulação de tarefas de classificação supervisionada binária como problemas de Otimização Binária Quadrática Irrestrita (QUBO) e sua resolução pelo algoritmo QAOA em simuladores quânticos. O conjunto de dados breast cancer da biblioteca scikit-learn foi padronizado por escore Z, reduzido via PCA e reescalado para [0, 1], particionado com estratificação em 70% para treino e 30% para teste (seed 42). O classificador linear discretizado em variáveis binárias com penalização de norma e exclusão mútua de sinal foi confrontado com o SVM clássico e com o classificador variacional (VQC). Em instâncias com 2 componentes principais, o QAOA alcançou 90,00% de acurácia de teste em 3,70 s, contra 100,00% do SVM (0,0009 s) e 83,33% do VQC (12,81 s). A avaliação de escalabilidade até 5 componentes comprovou a estabilidade preditiva do modelo QUBO (90,00% exato), delimitando a barreira computacional da simulação clássica pelo crescimento exponencial do tempo de execução do QAOA.")
    body_elements.append(make_p([make_run(resumo_text, font_size=23)], jc="both", first_line=0, space_after=60, line_spacing=260))
    
    kw_pt = [make_run("Palavras-chave: ", bold=True, font_size=23), make_run("QAOA; QUBO; classificação supervisionada; aprendizado de máquina quântico; simuladores quânticos.", font_size=23)]
    body_elements.append(make_p(kw_pt, jc="both", first_line=0, space_after=140, line_spacing=260))

    body_elements.append(make_p([make_run("ABSTRACT", bold=True, font_size=24)], jc="both", first_line=0, space_after=60, line_spacing=260))
    abstract_text = ("This study evaluates the formulation of binary supervised classification tasks as Quadratic Unconstrained Binary Optimization (QUBO) problems solved by the QAOA algorithm on quantum simulators. The breast cancer dataset was standardized, reduced via PCA, scaled to [0, 1], and partitioned with stratification into 70% training and 30% testing subsets. A discretized linear classifier with regularized binary weights and mutual sign exclusion was compared against classical SVM and simulated VQC baselines. For instances with 2 principal components, QAOA achieved 90.00% test accuracy in 3.70 s, compared to 100.00% for SVM (0.0009 s) and 83.33% for VQC (12.81 s). Scalability tests across 2 to 5 components confirmed the functional stability of the QUBO formulation while highlighting the computational bottleneck of classical state-vector simulation, which scales exponentially with the number of qubits.")
    body_elements.append(make_p([make_run(abstract_text, italic=False, font_size=23)], jc="both", first_line=0, space_after=60, line_spacing=260))

    kw_en = [make_run("Keywords: ", bold=True, font_size=23), make_run("QAOA; QUBO; supervised classification; quantum machine learning; quantum simulators.", italic=False, font_size=23)]
    body_elements.append(make_p(kw_en, jc="both", first_line=0, space_after=180, line_spacing=260))

    body_elements.append(make_heading_1("1 INTRODUÇÃO", num=False))
    body_elements.append(make_p([make_run(
        "A computação quântica baseada em circuitos variacionais híbridos tem sido investigada para explorar novos modelos de otimização no regime de processadores com ruído e conectividade limitada (era NISQ). Embora modelos tradicionais de aprendizado supervisionado operem em espaços contínuos por otimização convexa, a representação de tarefas de classificação sob formalismos combinatórios discretos viabiliza sua execução em computadores quânticos através de matrizes de interação quadrática. Contudo, em plataformas clássicas de simulação por vetores de estado, a emulação das operações quânticas impõe custo de memória e tempo exponencialmente proporcional ao número de qubits, exigindo a caracterização empírica de sua viabilidade técnica frente a métodos consolidados."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    body_elements.append(make_p([make_run(
        "O objetivo deste trabalho é avaliar o desempenho do algoritmo QAOA (Quantum Approximate Optimization Algorithm) na resolução de problemas de classificação binária formulados como QUBO (Quadratic Unconstrained Binary Optimization), analisando a acurácia de generalização e o tempo computacional em simuladores quânticos. Especificamente, busca-se: 1) mapear a função de custo de um classificador linear discretizado para uma matriz QUBO com penalidades quadráticas; 2) contrastar as métricas de convergência do QAOA com o classificador SVM clássico e com o classificador quântico variacional (VQC); e 3) quantificar a escalabilidade temporal da abordagem frente ao incremento da dimensionalidade de entrada via componentes principais (PCA)."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    body_elements.append(make_p([make_run(
        "Essa abordagem fundamenta a investigação empírica do QAOA frente a baselines consolidados: postula-se que a formulação QUBO preserva a capacidade discriminativa em instâncias controladas, embora o custo de simulação clássica limite a profundidade e a dimensionalidade operacional perante algoritmos tradicionais."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("2 REVISÃO DE LITERATURA", num=False))
    body_elements.append(make_p([make_run(
        "Algoritmos quânticos variacionais (VQAs) empregam circuitos parametrizados cuja energia esperada é avaliada em processadores quânticos e atualizada iterativamente por rotinas clássicas de otimização (Bharti et al., 2022; Cerezo et al., 2021). O algoritmo QAOA, formulado originalmente por Farhi, Goldstone e Gutmann (2014), alterna a aplicação de operadores Hamiltonianos de custo e de mistura para conduzir o estado inicial a uma configuração que aproxima o mínimo de uma função combinatorial. Em tarefas de classificação, o aprendizado quântico tradicional explora espaços de Hilbert através de mapas de características e ansätze variacionais (Havlíček et al., 2019; Schuld; Killoran, 2019). No entanto, a modelagem direta da perda de classificação como uma função quadrática binária viabiliza a aplicação de amostradores e solvers quânticos combinatórios (Grange; Poss; Bourreau, 2024)."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    body_elements.append(make_p([make_run(
        "O paradigma QUBO expressa problemas de otimização discreta como formas quadráticas sobre vetores binários, equivalendo à representação do modelo de Ising (Glover; Kochenberger; Du, 2019; Lucas, 2014). Mapeamentos de Support Vector Machines para QUBO permitem explorar o espaço de parâmetros por meio de relaxações discretas (Guddanti et al., 2024). Em simulações clássicas de circuitos quânticos, a compressão dimensional prévia via PCA é indispensável para conter o dimensionamento do registrador de qubits e evitar a degradação temporal das rotinas de otimização (Mancilla; Pere, 2022; Qi et al., 2025). A escolha de otimizadores clássicos como COBYLA e SPSA determina a eficiência da convergência sob diferentes superfícies de custo e perturbações de amostragem (AL Ajmi; Shoaib, 2025; Spall, 1992)."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("3 METODOLOGIA", num=False))
    body_elements.append(make_p([make_run(
        "O protocolo experimental foi implementado em Python utilizando as bibliotecas scikit-learn (v1.4) e Qiskit (Qiskit v1.0, Qiskit Algorithms e Qiskit Optimization). Empregou-se o conjunto de dados breast cancer, extraindo-se uma amostra estratificada de 100 instâncias particionada em 70% para treinamento e 30% para teste com semente pseudoaleatória controlada (random_state = 42). O fluxo de pré-processamento consistiu em padronização por escore Z (StandardScaler ajustado no treino), redução de dimensionalidade por PCA e normalização linear no intervalo [0, 1] com MinMaxScaler."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    body_elements.append(make_p([make_run(
        "Para o baseline de referência, utilizou-se um SVM linear clássico e um modelo VQC composto pelo mapa de características ZZFeatureMap, ansatz variacional RealAmplitudes e otimizador SPSA com 100 iterações. Na formulação combinatória, o hiperplano de separação linear foi discretizado representando cada coeficiente w_j e o viés b por um par de variáveis binárias que codificam magnitudes positivas e negativas: c_k = s · (b_k^(+) - b_k^(-)), com escala s = 2,0 e 1 bit de resolução por sinal, totalizando n_bin = 2(d + 1) variáveis booleanas para d componentes PCA."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    body_elements.append(make_p([make_run(
        "A função objetivo minimizada adotou o critério de erro quadrático de margem com termos de regularização e penalidade de exclusão mútua de sinal: H = (1 / N) * ∑ (b + ∑ x_ij · w_j - y_i)² + λ_reg · ∑ w_j² + λ_mut · ∑ (b_k^(+) · b_k^(-)), onde y_i ∈ {-1, +1} denota o rótulo da classe, λ_reg = 0,05 é a regularização L2 de pesos e λ_mut = 0,25 é a penalidade que impede a ativação simultânea de bits de polaridade oposta do mesmo coeficiente. A matriz resultante foi solucionada pelo QAOA com uma repetição (p = 1), operador StatevectorSampler e otimizador COBYLA, contrastando-se com um solver exato por enumeração completa de 2⁶ a 2¹² estados."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("4 RESULTADOS E DISCUSSÕES", num=False))
    body_elements.append(make_p([make_run(
        "A Tabela 1 consolida os resultados dos baselines e da formulação combinatória para a instância com 2 componentes PCA (6 variáveis binárias). O SVM linear clássico alcançou acurácia de 100,00% em 0,0009 segundos, enquanto o VQC simulado obteve 83,33% em 12,8098 segundos. Tanto o solver exato quanto o QAOA convergiram para 90,00% de acurácia de teste, demonstrando que a discretização de parâmetros preserva a fronteira de decisão essencial, com o QAOA executando em 3,6997 segundos no simulador."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    t1_headers = ["Modelo", "Paradigma", "Vars Binárias", "Acurácia", "Tempo (s)"]
    t1_rows = [
        ["SVM linear", "Clássico", "-", "100,00%", "0,0009 s"],
        ["VQC simulado", "Quântico Variacional", "-", "83,33%", "12,8098 s"],
        ["QUBO Solver Exato", "Clássico Exaustivo", "6", "90,00%", "0,0824 s"],
        ["QAOA-QUBO linear", "Quântico Combinatório", "6", "90,00%", "3,6997 s"]
    ]
    body_elements.append(make_table(t1_headers, t1_rows, "Tabela 1: Desempenho comparativo dos modelos no conjunto de teste (PCA = 2)."))

    body_elements.append(make_p([make_run(
        "A Tabela 2 apresenta a escalabilidade computacional variando o número de componentes PCA de 2 a 5. O solver exato manteve acurácia invariante de 90,00% em todas as configurações, com tempo de busca escalando de 0,0824 s (6 variáveis, 64 estados) a 7,1497 s (12 variáveis, 4.096 estados). Em contrapartida, a emulação do QAOA apresentou acentuada sensibilidade dimensional: o tempo elevou-se para 41,7146 s em PCA = 3 (8 variáveis) e para 863,4231 s em PCA = 4 (10 variáveis, 1.024 estados quânticos), forçando a redução do COBYLA para 5 iterações para viabilizar a conclusão do experimento."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    t2_headers = ["PCA", "Vars", "Espaço de Estados", "Solver Exato (Tempo / Ac.)", "QAOA Simulado (Tempo / Ac.)"]
    t2_rows = [
        ["2", "6", "64 estados (2⁶)", "0,0824 s  /  90,00%", "3,6997 s  /  90,00%"],
        ["3", "8", "256 estados (2⁸)", "0,4580 s  /  90,00%", "41,7146 s  /  90,00%"],
        ["4", "10", "1.024 estados (2¹⁰)", "1,2578 s  /  90,00%", "863,4231 s* / 96,67%"],
        ["5", "12", "4.096 estados (2¹²)", "7,1497 s  /  90,00%", "-  (limite de simulação)"]
    ]
    body_elements.append(make_table(t2_headers, t2_rows, "Tabela 2: Escalabilidade computacional da formulação QUBO sob variação de componentes PCA."))
    body_elements.append(make_p([make_run("Nota: * Otimizador COBYLA limitado a 5 iterações por restrição de tempo de simulação.", italic=True, font_size=18)], jc="both", first_line=0, space_after=80, line_spacing=200))

    body_elements.append(make_p([make_run(
        "Na instância com 4 componentes, o QAOA registrou acurácia nominal de 96,67% (29 acertos em 30 amostras), superando a taxa de 90,00% do solver exato. Esse desvio resulta da aproximação estocástica do QAOA sobre o conjunto de treino que, pela discretização em passos de 2,0, produziu um ligeiro deslocamento do limiar do hiperplano que coincidiu com a classificação correta de duas instâncias limítrofes na partição de teste reduzida (flutuação amostral). Os resultados confirmam a convergência funcional do modelo QUBO e evidenciam que o gargalo operacional reside na multiplicação matricial clássica exigida para emular processadores quânticos."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("5 CONCLUSÃO", num=False))
    body_elements.append(make_p([make_run(
        "Este trabalho avaliou a transposição de modelos de classificação binária supervisionada para o paradigma combinatório QUBO resolvido por QAOA em simuladores quânticos. Os experimentos confirmaram a viabilidade funcional da formulação discreta, atingindo acurácia de 90,00% com 2 componentes PCA e mantendo a estabilidade preditiva no solver exato em todas as dimensões analisadas."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    body_elements.append(make_p([make_run(
        "O confronto com o SVM clássico confirmou a hipótese norteadora: enquanto o classificador tradicional treina em milissegundos, o QAOA simulado enfrenta severa restrição de escalabilidade decorrente do custo exponencial de cálculo de vetores de estado em CPUs clássicas. Conclui-se que a formulação QUBO proposta preserva as propriedades discriminativas da classificação linear, mas sua aplicabilidade prática em problemas de maior escala dependerá da execução nativa em hardware quântico da era NISQ."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("REFERÊNCIAS", num=False))
    refs = [
        "AL AJMI, N. A.; SHOAIB, M. Optimization Strategies in Quantum Machine Learning: A Performance Analysis. Applied Sciences, v. 15, n. 8, p. 4493, 2025.",
        "BHARTI, K. et al. Noisy intermediate-scale quantum algorithms. Reviews of Modern Physics, v. 94, n. 1, p. 015004, 2022.",
        "CEREZO, M. et al. Variational quantum algorithms. Nature Reviews Physics, v. 3, p. 625–644, 2021.",
        "FARHI, E.; GOLDSTONE, J.; GUTMANN, S. A Quantum Approximate Optimization Algorithm. arXiv:1411.4028, 2014.",
        "GLOVER, F.; KOCHENBERGER, G.; DU, Y. A Tutorial on Formulating and Using QUBO Models. arXiv:1811.11538, 2019.",
        "GRANGE, C.; POSS, M.; BOURREAU, E. An introduction to variational quantum algorithms for combinatorial optimization problems. Annals of Operations Research, v. 343, p. 847–884, 2024.",
        "GUDDANTI, S. S. et al. Pneumonia detection by binary classification: classical, quantum, and hybrid approaches for SVM. Frontiers in Computer Science, v. 5, 2024.",
        "HAVLÍČEK, V. et al. Supervised learning with quantum-enhanced feature spaces. Nature, v. 567, p. 209–212, 2019.",
        "LUCAS, A. Ising formulations of many NP problems. Frontiers in Physics, v. 2, p. 5, 2014.",
        "MANCILLA, J.; PERE, C. A Preprocessing Perspective for Quantum Machine Learning Classification Advantage Using NISQ Algorithms. Entropy, v. 24, p. 1656, 2022.",
        "QI, H. et al. A high-efficiency variational quantum classifier for high-dimensional data. Journal of Supercomputing, v. 81, p. 1–20, 2025.",
        "SCHULD, M.; KILLORAN, N. Quantum Machine Learning in Feature Hilbert Spaces. Physical Review Letters, v. 122, p. 040504, 2019.",
        "SPALL, J. C. Multivariate stochastic approximation using a simultaneous perturbation gradient approximation. IEEE Transactions on Automatic Control, v. 37, n. 3, p. 332–341, 1992."
    ]
    for ref in refs:
        body_elements.append(make_p([make_run(ref, font_size=20)], jc="both", first_line=0, space_after=50, line_spacing=220))

    body_elements.append(make_heading_1("AGRADECIMENTOS", num=False))
    body_elements.append(make_p([make_run(
        "Agradece-se à Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior pelo suporte institucional e de infraestrutura concedido ao desenvolvimento desta pesquisa."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("SOBRE O(S)AUTOR(ES)", num=False))
    body_elements.append(make_p([make_run("Sobre os autores:", bold=True, font_size=22)], jc="both", first_line=0, space_after=40, line_spacing=220))
    body_elements.append(make_p([make_run("_________________", bold=True, font_size=22)], jc="both", first_line=0, space_after=80, line_spacing=220))

    body_elements.append(make_p([make_run("i Julio Coronetti Regino (Autor)", bold=True, font_size=22)], jc="both", first_line=0, space_after=40, line_spacing=220, pStyle="Textodenotadefim"))
    author1_bio = (
        '<w:tbl><w:tblPr><w:tblStyle w:val="Tabelacomgrade"/><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'
        '<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        '</w:tblBorders></w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="1418"/><w:gridCol w:w="7643"/></w:tblGrid>'
        '<w:tr><w:tc><w:tcPr><w:tcW w:w="1418" w:type="dxa"/></w:tcPr>'
        + make_p([make_run("Foto", font_size=18)], jc="center", first_line=0, space_after=0, line_spacing=200) +
        '</w:tc><w:tc><w:tcPr><w:tcW w:w="7643" w:type="dxa"/></w:tcPr>'
        + make_p([make_run("Discente do curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas na Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior. Desenvolve pesquisa de Iniciação Científica focada em algoritmos variacionais quânticos (QAOA, VQC) e otimização combinatória (QUBO) aplicados a machine learning. E-mail: julio.regino2@senaisp.edu.br.", font_size=20)], jc="both", first_line=0, space_after=0, line_spacing=240) +
        '</w:tc></w:tr></w:tbl>'
    )
    body_elements.append(author1_bio)

    body_elements.append(make_p([make_run("", font_size=12)], jc="both", first_line=0, space_after=40, line_spacing=200))

    body_elements.append(make_p([make_run("ii Cainã Antunes (Orientador)", bold=True, font_size=22)], jc="both", first_line=0, space_after=40, line_spacing=220, pStyle="Textodenotadefim"))
    author2_bio = (
        '<w:tbl><w:tblPr><w:tblStyle w:val="Tabelacomgrade"/><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'
        '<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        '</w:tblBorders></w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="1418"/><w:gridCol w:w="7643"/></w:tblGrid>'
        '<w:tr><w:tc><w:tcPr><w:tcW w:w="1418" w:type="dxa"/></w:tcPr>'
        + make_p([make_run("Foto", font_size=18)], jc="center", first_line=0, space_after=0, line_spacing=200) +
        '</w:tc><w:tc><w:tcPr><w:tcW w:w="7643" w:type="dxa"/></w:tcPr>'
        + make_p([make_run("Docente e pesquisador na Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, atuando como orientador de projetos de iniciação científica e desenvolvimento tecnológico em inteligência artificial e computação avançada. E-mail: caina.silva@sp.senai.br.", font_size=20)], jc="both", first_line=0, space_after=0, line_spacing=240) +
        '</w:tc></w:tr></w:tbl>'
    )
    body_elements.append(author2_bio)

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
