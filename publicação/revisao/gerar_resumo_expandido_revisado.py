import zipfile
import xml.etree.ElementTree as ET
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = str(BASE_DIR / "templates" / "Template_ResumoExpandido2026.docx")
OUTPUT_PATH = str(Path(__file__).resolve().parent / "Resumo_Expandido_Julio_Regino_2026_Revisado.docx")
DIST_PATH = str(BASE_DIR / "dist" / "Resumo_Expandido_Julio_Regino_2026.docx")

def escape_xml(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&apos;'))

def make_run(text, bold=False, italic=False, font_size=21, font_name="Arial", vert_align=None):
    rPr = []
    rPr.append(f'<w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
    if bold:
        rPr.append('<w:b/><w:bCs/>')
    if italic:
        rPr.append('<w:i/><w:iCs/>')
    rPr.append(f'<w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/>')
    if vert_align:
        rPr.append(f'<w:vertAlign w:val="{vert_align}"/>')
    rPr.append('<w:lang w:val="pt-BR"/>')
    rPr_xml = f"<w:rPr>{''.join(rPr)}</w:rPr>"
    return f'<w:r>{rPr_xml}<w:t xml:space="preserve">{escape_xml(text)}</w:t></w:r>'

def make_p(runs, jc="both", first_line=708, space_after=80, space_before=None, line_spacing=260, pStyle=None, numPr=None, keepNext=False):
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
    if space_before is not None:
        sp_attrs.append(f'w:before="{space_before}"')
    if space_after is not None:
        sp_attrs.append(f'w:after="{space_after}"')
    if line_spacing:
        sp_attrs.append(f'w:line="{line_spacing}" w:lineRule="auto"')
    if sp_attrs:
        pPr.append(f'<w:spacing {" ".join(sp_attrs)}/>')
        
    pPr_xml = f"<w:pPr>{''.join(pPr)}</w:pPr>"
    runs_xml = ''.join(runs)
    return f'<w:p>{pPr_xml}{runs_xml}</w:p>'

def make_heading_1(text, num=True, num_val="2", space_before=200, space_after=100):
    num_xml = f'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="{num_val}"/></w:numPr>' if num else ''
    r = make_run(text, bold=True, font_size=23, font_name="Arial")
    return make_p([r], jc="both", first_line=0, space_before=space_before, space_after=space_after, line_spacing=280, pStyle="Ttulo1", numPr=num_xml, keepNext=True)

def make_equation():
    return (
        '<w:p>'
        '<w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr>'
        '<m:oMathPara><m:oMath>'
        '<m:r><m:t>H(b, w) = </m:t></m:r>'
        '<m:f><m:fPr><m:type m:val="bar"/></m:fPr><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>N</m:t></m:r></m:den></m:f>'
        '<m:nary>'
        '<m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>'
        '<m:sub><m:r><m:t>i=1</m:t></m:r></m:sub>'
        '<m:sup><m:r><m:t>N</m:t></m:r></m:sup>'
        '<m:e>'
        '<m:sSup>'
        '<m:e>'
        '<m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e>'
        '<m:r><m:t>b + </m:t></m:r>'
        '<m:nary>'
        '<m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>'
        '<m:sub><m:r><m:t>j=1</m:t></m:r></m:sub>'
        '<m:sup><m:r><m:t>d</m:t></m:r></m:sup>'
        '<m:e>'
        '<m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>ij</m:t></m:r></m:sub></m:sSub>'
        '<m:sSub><m:e><m:r><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:t>j</m:t></m:r></m:sub></m:sSub>'
        '</m:e>'
        '</m:nary>'
        '<m:r><m:t> - </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>y</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub>'
        '</m:e></m:d>'
        '</m:e>'
        '<m:sup><m:r><m:t>2</m:t></m:r></m:sup>'
        '</m:sSup>'
        '</m:e>'
        '</m:nary>'
        '<m:r><m:t> + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>λ</m:t></m:r></m:e><m:sub><m:r><m:t>reg</m:t></m:r></m:sub></m:sSub>'
        '<m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e>'
        '<m:sSup><m:e><m:r><m:t>b</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup>'
        '<m:r><m:t> + </m:t></m:r>'
        '<m:nary>'
        '<m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>'
        '<m:sub><m:r><m:t>j=1</m:t></m:r></m:sub>'
        '<m:sup><m:r><m:t>d</m:t></m:r></m:sup>'
        '<m:e>'
        '<m:sSubSup><m:e><m:r><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:t>j</m:t></m:r></m:sub><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSubSup>'
        '</m:e>'
        '</m:nary>'
        '</m:e></m:d>'
        '<m:r><m:t> + </m:t></m:r>'
        '<m:sSub><m:e><m:r><m:t>λ</m:t></m:r></m:e><m:sub><m:r><m:t>mut</m:t></m:r></m:sub></m:sSub>'
        '<m:nary>'
        '<m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>'
        '<m:sub><m:r><m:t>k=0</m:t></m:r></m:sub>'
        '<m:sup><m:r><m:t>d</m:t></m:r></m:sup>'
        '<m:e>'
        '<m:sSubSup><m:e><m:r><m:t>b</m:t></m:r></m:e><m:sub><m:r><m:t>k</m:t></m:r></m:sub><m:sup><m:r><m:t>(+)</m:t></m:r></m:sup></m:sSubSup>'
        '<m:sSubSup><m:e><m:r><m:t>b</m:t></m:r></m:e><m:sub><m:r><m:t>k</m:t></m:r></m:sub><m:sup><m:r><m:t>(-)</m:t></m:r></m:sup></m:sSubSup>'
        '</m:e>'
        '</m:nary>'
        '<m:r><m:t>            (1)</m:t></m:r>'
        '</m:oMath></m:oMathPara>'
        '</w:p>'
    )

def make_table(headers, rows, caption_text):
    caption = make_p([make_run(caption_text, bold=True, font_size=19)], jc="both", first_line=0, space_before=160, space_after=60, line_spacing=220, keepNext=True)
    
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
        p = make_p([make_run(h, bold=True, font_size=18)], jc="center", first_line=0, space_after=25, line_spacing=210)
        tbl_xml.append(p)
        tbl_xml.append('</w:tc>')
    tbl_xml.append('</w:tr>')
    
    for row in rows:
        tbl_xml.append('<w:tr>')
        for idx, cell in enumerate(row):
            tbl_xml.append('<w:tc>')
            jc = "left" if idx == 0 and len(cell) > 5 else "center"
            p = make_p([make_run(cell, bold=False, font_size=18)], jc=jc, first_line=0, space_after=20, line_spacing=210)
            tbl_xml.append(p)
            tbl_xml.append('</w:tc>')
        tbl_xml.append('</w:tr>')
        
    tbl_xml.append('</w:tbl>')
    
    space_after_tbl = make_p([make_run("", font_size=10)], jc="both", first_line=0, space_after=50, line_spacing=180)
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
      <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr><w:t xml:space="preserve"> Discente, Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, julio.regino2@senaisp.edu.br.</w:t></w:r>
    </w:p>
  </w:footnote>
  <w:footnote w:id="2">
    <w:p>
      <w:pPr><w:pStyle w:val="Textodenotaderodap"/></w:pPr>
      <w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr><w:footnoteRef/></w:r>
      <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr><w:t xml:space="preserve"> Docente, Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, caina.silva@sp.senai.br.</w:t></w:r>
    </w:p>
  </w:footnote>
</w:footnotes>'''

def build_document_xml():
    body_elements = []

    body_elements.append(make_p(
        [make_run("EXPLORAÇÃO DO ALGORITMO QAOA PARA OTIMIZAÇÃO EM MODELOS DE CLASSIFICAÇÃO SUPERVISIONADA UTILIZANDO SIMULADORES QUÂNTICOS", bold=True, font_size=23)],
        jc="center", first_line=0, space_after=80, line_spacing=250
    ))
    
    body_elements.append(make_p(
        [make_run("EXPLORATION OF THE QAOA ALGORITHM FOR OPTIMIZATION IN SUPERVISED CLASSIFICATION MODELS USING QUANTUM SIMULATORS", bold=True, font_size=23)],
        jc="center", first_line=0, space_after=140, line_spacing=250
    ))

    author_runs = [
        make_run("Julio Coronetti Regino", bold=True, font_size=22),
        '<w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr><w:footnoteReference w:id="1"/></w:r>',
        make_run(", i, ", bold=False, font_size=22),
        make_run("Cainã Antunes", bold=True, font_size=22),
        '<w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr><w:footnoteReference w:id="2"/></w:r>',
        make_run(", ii", bold=False, font_size=22)
    ]
    body_elements.append(make_p(author_runs, jc="both", first_line=0, space_after=140, line_spacing=250))

    body_elements.append(make_p([make_run("RESUMO", bold=True, font_size=22)], jc="both", first_line=0, space_after=50, line_spacing=250))
    resumo_runs = [
        make_run("Este trabalho investiga a formulação da classificação supervisionada binária como um problema de Otimização Binária Quadrática Irrestrita (QUBO), resolvido via algoritmo QAOA em simuladores quânticos analíticos de vetores de estado. A partir de uma subamostra estratificada de 100 instâncias (37 da classe maligna e 63 da benigna) do conjunto breast cancer (scikit-learn), particionada em 70% para treino e 30% para teste, avaliou-se um classificador linear com pesos discretizados frente ao SVM linear clássico e ao classificador quântico variacional (VQC). Para prevenir rigorosamente qualquer vazamento de dados (data leakage), a padronização por escore Z, a Análise de Componentes Principais (PCA) e a normalização linear em [0, 1] foram ajustadas exclusivamente na partição de treinamento e aplicadas no teste. Enquanto o VQC treina as rotações de portas lógicas em um circuito quântico classificador, o QAOA otimiza os coeficientes discretizados de uma função de perda clássica mapeada para QUBO. Com 2 componentes PCA, tanto o solver exato quanto o QAOA convergiram para o mesmo valor ótimo de função objetivo (0,8736) no treino e registraram 90,00% de acurácia observada no teste (QAOA em 3,70 s, SVM em 0,0010 s e VQC em 12,81 s). A avaliação de escalabilidade abrangeu o QAOA de 2 a 4 componentes e o solver exato de 2 a 5 componentes. O QAOA manteve o custo ótimo em PCA = 3 (0,8736; 90,00%; 41,71 s) e obteve 96,67% em PCA = 4 (863,42 s) sobre uma solução subótima no treino (0,8764), cuja oscilação constitui hipótese de flutuação amostral decorrente da partição de teste reduzida. O solver exato alcançou 90,00% em PCA = 5 (7,15 s; 12 variáveis), confirmando a viabilidade representacional da modelagem e caracterizando os limites operacionais na simulação clássica de amplitudes quânticas.", font_size=21)
    ]
    body_elements.append(make_p(resumo_runs, jc="both", first_line=0, space_after=50, line_spacing=250))
    
    kw_pt = [make_run("Palavras-chave: ", bold=True, font_size=21), make_run("QAOA; QUBO; classificação supervisionada; aprendizado de máquina quântico; simuladores quânticos.", font_size=21)]
    body_elements.append(make_p(kw_pt, jc="both", first_line=0, space_after=120, line_spacing=250))

    body_elements.append(make_p([make_run("ABSTRACT", bold=True, font_size=22)], jc="both", first_line=0, space_after=50, line_spacing=250))
    abstract_runs = [
        make_run("This study investigates the formulation of binary supervised classification as a Quadratic Unconstrained Binary Optimization (QUBO) problem solved by the QAOA algorithm on quantum statevector simulators. Using a stratified subset of 100 instances (37 malignant, 63 benign) from the breast cancer dataset, partitioned into 70% training and 30% testing subsets, a discretized linear classifier was evaluated against classical linear SVM and simulated Variational Quantum Classifier (VQC) baselines. To strictly prevent data leakage, Z-score standardization, Principal Component Analysis (PCA), and [0, 1] min-max normalization were fitted exclusively on the training partition and applied to the test partition. While VQC adjusts parameterized gate rotations in a quantum circuit, QAOA optimizes the discretized coefficients of a classical quadratic loss mapped to QUBO. With 2 PCA components, both the exact solver and QAOA converged to the optimal objective function value (0.8736) on training, achieving 90.00% observed test accuracy (QAOA in 3.70 s, SVM in 0.0010 s, and VQC in 12.81 s). Scalability evaluation assessed QAOA from 2 to 4 components and the exact solver from 2 to 5 components. QAOA retained the optimal cost at PCA = 3 (0.8736; 90.00%; 41.71 s) and yielded 96.67% at PCA = 4 (863.42 s) with a suboptimal training cost (0.8764), hypothesized as a sample fluctuation on the small test partition. The exact solver reached 90.00% at PCA = 5 (7.15 s; 12 variables), demonstrating representational viability while characterizing the operational runtime bottleneck of classical statevector simulation.", italic=False, font_size=21)
    ]
    body_elements.append(make_p(abstract_runs, jc="both", first_line=0, space_after=50, line_spacing=250))

    kw_en = [make_run("Keywords: ", bold=True, font_size=21), make_run("QAOA; QUBO; supervised classification; quantum machine learning; quantum simulators.", italic=False, font_size=21)]
    body_elements.append(make_p(kw_en, jc="both", first_line=0, space_after=160, line_spacing=250))

    # 1 INTRODUÇÃO
    body_elements.append(make_heading_1("1 INTRODUÇÃO", num=False))
    body_elements.append(make_p([make_run(
        "A computação quântica baseada em circuitos variacionais híbridos tem sido amplamente investigada para explorar novos paradigmas "
        "de otimização sob as restrições da era NISQ (Noisy Intermediate-Scale Quantum), caracterizada por conectividade limitada e presença "
        "de ruído (Bharti et al., 2022). Embora o aprendizado supervisionado convencional opere tradicionalmente em espaços contínuos por "
        "meio de otimização convexa, a representação de tarefas de classificação sob formalismos combinatórios discretos viabiliza sua "
        "resolução em arquiteturas quânticas através de matrizes de interação quadrática (Grange; Poss; Bourreau, 2024).", font_size=21
    )], jc="both", first_line=708, space_after=80, line_spacing=260))

    body_elements.append(make_p([make_run(
        "Nesse contexto, cabe distinguir duas vertentes fundamentais do aprendizado de máquina quântico: enquanto classificadores "
        "quânticos variacionais (VQC) ajustam os parâmetros contínuos de rotação de um circuito quântico classificador atuando sobre "
        "espaços de Hilbert (Havlíček et al., 2019; Schuld; Killoran, 2019), a abordagem baseada no algoritmo QAOA (Quantum Approximate "
        "Optimization Algorithm) utiliza circuitos quânticos parametrizados para encontrar as configurações binárias que minimizam uma "
        "função de custo combinatória mapeada para QUBO (Quadratic Unconstrained Binary Optimization) (Farhi; Goldstone; Gutmann, 2014; "
        "Glover; Kochenberger; Du, 2019). Em simuladores clássicos por vetores de estado, contudo, a representação exata de 2", font_size=21
    ), make_run("n", font_size=21, vert_align="superscript"), make_run(
        " amplitudes impõe um crescimento exponencial no tempo de processamento conforme o registrador de qubits se expande, exigindo a caracterização "
        "empírica de sua escalabilidade perante métodos consolidados.", font_size=21
    )], jc="both", first_line=708, space_after=80, line_spacing=260))

    body_elements.append(make_p([make_run(
        "O objetivo deste estudo é avaliar o desempenho do algoritmo QAOA na resolução de tarefas de classificação binária formuladas "
        "como QUBO, analisando a acurácia de generalização observada e o tempo computacional em simuladores quânticos frente ao SVM linear "
        "clássico e ao VQC simulado. O escopo compreende: 1) mapear a perda de um classificador linear discretizado para uma matriz QUBO com "
        "penalidades quadráticas; 2) verificar o impacto da prevenção rigorosa de vazamento de dados (data leakage) no fluxo de "
        "pré-processamento via Análise de Componentes Principais (PCA, do inglês Principal Component Analysis); 3) comparar o desempenho "
        "observado e os valores de custo atingidos pelo QAOA e por um solver combinatorial exato; e 4) delimitar a escalabilidade da "
        "simulação clássica, avaliando o QAOA em instâncias de 2 a 4 componentes PCA e o solver exato até 5 componentes.", font_size=21
    )], jc="both", first_line=708, space_after=120, line_spacing=260))

    # 2 REVISÃO DE LITERATURA
    body_elements.append(make_heading_1("2 REVISÃO DE LITERATURA", num=False))
    body_elements.append(make_p([make_run(
        "Algoritmos quânticos variacionais (VQAs) utilizam circuitos parametrizados cuja energia esperada é mensurada e otimizada "
        "iterativamente por rotinas clássicas (Cerezo et al., 2021). O algoritmo QAOA, proposto por Farhi, Goldstone e Gutmann (2014), "
        "alterna operadores Hamiltonianos de custo e de mistura para guiar o estado quântico em direção à solução ótima de problemas "
        "combinatórios discretos. Em classificação, o paradigma dominante explora mapas de características quânticos (Havlíček et al., "
        "2019; Schuld; Killoran, 2019). Todavia, a modelagem de fronteiras de decisão como problemas quadráticos irrestritos viabiliza o "
        "emprego direto de otimizadores combinatórios quânticos (Grange; Poss; Bourreau, 2024).", font_size=21
    )], jc="both", first_line=708, space_after=80, line_spacing=260))

    body_elements.append(make_p([make_run(
        "O formalismo QUBO mapeia problemas de otimização combinatória sobre vetores booleanos, mantendo equivalência direta com o modelo "
        "físico de Ising (Glover; Kochenberger; Du, 2019; Lucas, 2014). Mapeamentos de classificadores do tipo Support Vector Machine para "
        "QUBO permitem explorar o espaço discreto de parâmetros (Guddanti et al., 2024). Em plataformas clássicas de simulação quântica, a "
        "redução prévia de dimensionalidade por PCA é indispensável para conter a dimensão do registrador de qubits e viabilizar a "
        "convergência das rotinas de otimização (Mancilla; Pere, 2022; Qi et al., 2025). Ademais, a seleção e a tolerância de otimizadores "
        "clássicos como COBYLA e SPSA governam a estabilidade da convergência em circuitos variacionais (AL Ajmi; Shoaib, 2025; Spall, 1992).", font_size=21
    )], jc="both", first_line=708, space_after=120, line_spacing=260))

    # 3 METODOLOGIA
    body_elements.append(make_heading_1("3 METODOLOGIA", num=False))
    body_elements.append(make_p([make_run(
        "O protocolo experimental utilizou o conjunto de dados breast cancer da biblioteca scikit-learn (569 instâncias, 30 atributos). "
        "Extraiu-se uma subamostra estratificada de 100 instâncias, preservando a proporção de 37 amostras da classe 0 (maligno) e 63 da "
        "classe 1 (benigno). Essa amostra foi particionada com estratificação em 70% para treinamento (N = 70: 26 classe 0 e 44 classe 1) "
        "e 30% para teste (30 instâncias: 11 classe 0 e 19 classe 1), fixando a semente pseudoaleatória controlada (random_state = 42). "
        "Para evitar estritamente qualquer vazamento de dados (data leakage), o fluxo de pré-processamento foi ajustado exclusivamente "
        "no conjunto de treino: a padronização por escore Z (StandardScaler), a redução dimensional por PCA e o reescalonamento no "
        "intervalo [0, 1] (MinMaxScaler) foram calibrados no treino e subsequentemente aplicados à partição de teste.", font_size=21
    )], jc="both", first_line=708, space_after=80, line_spacing=260))

    p2_runs = [
        make_run("Na formulação combinatória, o hiperplano de separação linear foi discretizado representando cada coeficiente de peso ", font_size=21),
        make_run("w", italic=True, font_size=21),
        make_run("j", italic=True, font_size=21, vert_align="subscript"),
        make_run(" (", font_size=21),
        make_run("j", italic=True, font_size=21),
        make_run(" ∈ {1, ..., ", font_size=21),
        make_run("d", italic=True, font_size=21),
        make_run("}) e o viés ", font_size=21),
        make_run("b", italic=True, font_size=21),
        make_run(" por variáveis binárias booleanas que codificam magnitudes positivas e negativas: ", font_size=21),
        make_run("w", italic=True, font_size=21),
        make_run("j", italic=True, font_size=21, vert_align="subscript"),
        make_run(" = ", font_size=21),
        make_run("s", italic=True, font_size=21),
        make_run(" · (", font_size=21),
        make_run("b", italic=True, font_size=21),
        make_run("j", italic=True, font_size=21, vert_align="subscript"),
        make_run("(+)", font_size=21, vert_align="superscript"),
        make_run(" - ", font_size=21),
        make_run("b", italic=True, font_size=21),
        make_run("j", italic=True, font_size=21, vert_align="subscript"),
        make_run("(-)", font_size=21, vert_align="superscript"),
        make_run(") e ", font_size=21),
        make_run("b", italic=True, font_size=21),
        make_run(" = ", font_size=21),
        make_run("s", italic=True, font_size=21),
        make_run(" · (", font_size=21),
        make_run("b", italic=True, font_size=21),
        make_run("0", font_size=21, vert_align="subscript"),
        make_run("(+)", font_size=21, vert_align="superscript"),
        make_run(" - ", font_size=21),
        make_run("b", italic=True, font_size=21),
        make_run("0", font_size=21, vert_align="subscript"),
        make_run("(-)", font_size=21, vert_align="superscript"),
        make_run("), onde ", font_size=21),
        make_run("b", italic=True, font_size=21),
        make_run("k", italic=True, font_size=21, vert_align="subscript"),
        make_run("(+)", font_size=21, vert_align="superscript"),
        make_run(", ", font_size=21),
        make_run("b", italic=True, font_size=21),
        make_run("k", italic=True, font_size=21, vert_align="subscript"),
        make_run("(-)", font_size=21, vert_align="superscript"),
        make_run(" ∈ {0, 1}, com escala ", font_size=21),
        make_run("s", italic=True, font_size=21),
        make_run(" = 2,0 e 1 bit por sinal, totalizando ", font_size=21),
        make_run("n", italic=True, font_size=21),
        make_run("bin", font_size=21, vert_align="subscript"),
        make_run(" = 2(", font_size=21),
        make_run("d", italic=True, font_size=21),
        make_run(" + 1) variáveis binárias para ", font_size=21),
        make_run("d", italic=True, font_size=21),
        make_run(" componentes PCA. A função objetivo minimizada adotou o critério de erro quadrático de margem com penalização L2 e exclusão mútua de polaridade, conforme apresentado na Equação (1):", font_size=21)
    ]
    body_elements.append(make_p(p2_runs, jc="both", first_line=708, space_after=60, line_spacing=260))

    # Inserção da Equação em OMML nativo (Word Equation)
    body_elements.append(make_equation())

    p3_runs = [
        make_run("onde ", font_size=21),
        make_run("N", italic=True, font_size=21),
        make_run(" = 70 é o número de amostras de treino, ", font_size=21),
        make_run("y", italic=True, font_size=21),
        make_run("i", italic=True, font_size=21, vert_align="subscript"),
        make_run(" ∈ {-1, +1} denota o rótulo de classe, ", font_size=21),
        make_run("λ", italic=True, font_size=21),
        make_run("reg", font_size=21, vert_align="subscript"),
        make_run(" = 0,05 é o hiperparâmetro de regularização L2 aplicado a todos os coeficientes (incluindo o intercepto) e ", font_size=21),
        make_run("λ", italic=True, font_size=21),
        make_run("mut", font_size=21, vert_align="subscript"),
        make_run(" = 0,25 penaliza a ativação concorrente de bits de sinal oposto do mesmo coeficiente. A classe prevista para uma amostra de teste é obtida pelo sinal do score linear: ", font_size=21),
        make_run("ŷ", italic=True, font_size=21),
        make_run(" = 1 se (", font_size=21),
        make_run("b", italic=True, font_size=21),
        make_run(" + ∑", font_size=21),
        make_run("j=1", font_size=21, vert_align="subscript"),
        make_run("d", font_size=21, vert_align="superscript"),
        make_run(" ", font_size=21),
        make_run("x", italic=True, font_size=21),
        make_run("ij", italic=True, font_size=21, vert_align="subscript"),
        make_run(" · ", font_size=21),
        make_run("w", italic=True, font_size=21),
        make_run("j", italic=True, font_size=21, vert_align="subscript"),
        make_run(") ≥ 0,0, e ", font_size=21),
        make_run("ŷ", italic=True, font_size=21),
        make_run(" = 0 caso contrário, mapeando formalmente o limiar zero para a classe 1.", font_size=21)
    ]
    body_elements.append(make_p(p3_runs, jc="both", first_line=708, space_after=80, line_spacing=260))

    body_elements.append(make_p([make_run(
        "O protocolo computacional foi executado em ambiente Linux x86_64 dual-core (2 vCPUs @ 2,8 GHz, 8 GB RAM) sob Python 3.10+, "
        "empregando scikit-learn v1.4, qiskit v1.0, qiskit-algorithms v0.3.0, qiskit-optimization v0.6.1 e qiskit-machine-learning v0.7.2. "
        "O classificador clássico utilizou SVC(kernel='linear', C=1.0). O modelo VQC simulado adotou ZZFeatureMap(reps=1), ansatz "
        "RealAmplitudes(reps=1) (profundidade total de 6 camadas lógicas) e otimizador SPSA (maxiter=100, inicialização em 0,1, semente 42). "
        "O QAOA foi configurado com 1 camada (p = 1), ponto inicial dos ângulos (γ, β) fixado em 0,1, e simulador analítico "
        "StatevectorSampler(seed=42) operando no regime ideal exato (sem ruído e shots analíticos). O otimizador clássico COBYLA foi configurado "
        "com os limites: 20 iterações em PCA = 2, 20 iterações em PCA = 3 e 5 iterações em PCA = 4; a instância com PCA = 5 não foi submetida "
        "ao QAOA devido à projeção temporal. A solução binária retornada pelo QAOA é selecionada pelo MinimumEigenOptimizer, que extrai o "
        "autoestado de menor energia da função objetivo. Cada configuração empírica foi avaliada em uma única execução experimental (N = 1); "
        "os tempos reportados medem exclusivamente o processo de otimização/treinamento e inferência.", font_size=21
    )], jc="both", first_line=708, space_after=120, line_spacing=260))

    # 4 RESULTADOS E DISCUSSÕES
    body_elements.append(make_heading_1("4 RESULTADOS E DISCUSSÕES", num=False))
    body_elements.append(make_p([make_run(
        "A Tabela 1 apresenta o desempenho dos baselines e da formulação combinatória na partição de teste para a configuração com 2 componentes "
        "PCA (6 variáveis binárias). O SVM linear clássico obteve 100,00% de acurácia em 0,0010 s, enquanto o VQC simulado atingiu 83,33% em "
        "12,8098 s. Tanto o solver exato por busca exaustiva quanto o QAOA convergiram rigorosamente para o mesmo valor ótimo da função objetivo "
        "no treino (f", font_size=21
    ), make_run("val", font_size=21, vert_align="subscript"), make_run(
        " = 0,8736) e atingiram 90,00% de acurácia observada no teste, comprovando que a discretização proposta preserva a "
        "capacidade discriminativa essencial do modelo linear, com o QAOA concluindo a otimização em 3,6997 s.", font_size=21
    )], jc="both", first_line=708, space_after=80, line_spacing=260))

    t1_headers = ["Modelo", "Paradigma", "Vars", "f_val Treino", "Acurácia Teste", "Tempo (s)"]
    t1_rows = [
        ["SVM linear", "Clássico", "-", "-", "100,00%", "0,0010 s"],
        ["VQC simulado", "Quântico Variacional", "-", "-", "83,33%", "12,8098 s"],
        ["QUBO Solver Exato", "Clássico Exaustivo", "6", "0,8736", "90,00%", "0,0824 s"],
        ["QAOA-QUBO linear", "Quântico Combinatório", "6", "0,8736", "90,00%", "3,6997 s"]
    ]
    body_elements.append(make_table(t1_headers, t1_rows, "Tabela 1: Desempenho comparativo dos modelos no conjunto de teste (PCA = 2, N = 1)."))

    body_elements.append(make_p([make_run(
        "A Tabela 2 consolida a escalabilidade computacional variando os componentes PCA de 2 a 5. O solver exato manteve o valor ótimo da "
        "função objetivo (f", font_size=21
    ), make_run("val", font_size=21, vert_align="subscript"), make_run(
        " = 0,8736) e acurácia observada constante de 90,00% em todas as instâncias, com o tempo escalando de 0,0824 s "
        "(6 variáveis, 64 estados) até 7,1497 s (12 variáveis, 4.096 estados). No solver exato, a manutenção de f", font_size=21
    ), make_run("val", font_size=21, vert_align="subscript"), make_run(
        " = 0,8736 de 2 a 5 componentes decorre da resolução discreta adotada (w", font_size=21
    ), make_run("j", font_size=21, vert_align="subscript"), make_run(
        " ∈ {-2, 0, +2}) sob regularização L2, na qual o ótimo global atribui peso zero aos componentes adicionais de menor variância. O QAOA simulado acompanhou o ótimo global em PCA = 2 e PCA = 3 "
        "(8 variáveis, 256 estados), alcançando f", font_size=21
    ), make_run("val", font_size=21, vert_align="subscript"), make_run(
        " = 0,8736 e 90,00% de acurácia em 41,7146 s. Para PCA = 4 (10 variáveis, 1.024 estados), a "
        "restrição a 5 iterações do COBYLA levou a um tempo de 863,4231 s (~14,4 min) e resultou em uma solução subótima no treino "
        "(f", font_size=21
    ), make_run("val", font_size=21, vert_align="subscript"), make_run(
        " = 0,8764 contra 0,8736 do exato). A configuração com 5 componentes não foi executada via QAOA devido ao limite de tempo imposto pelo ambiente.", font_size=21
    )], jc="both", first_line=708, space_after=80, line_spacing=260))

    t2_headers = ["PCA", "Vars", "Espaço (2^n)", "Solver Exato (Tempo / f_val / Ac.)", "QAOA Simulado (Tempo / f_val / Ac.)"]
    t2_rows = [
        ["2", "6", "64 estados (2⁶)", "0,0824 s  /  0,8736  /  90,00%", "3,6997 s  /  0,8736  /  90,00%"],
        ["3", "8", "256 estados (2⁸)", "0,4580 s  /  0,8736  /  90,00%", "41,7146 s  /  0,8736  /  90,00%"],
        ["4", "10", "1.024 estados (2¹⁰)", "1,2578 s  /  0,8736  /  90,00%", "863,4231 s* / 0,8764 / 96,67%"],
        ["5", "12", "4.096 estados (2¹²)", "7,1497 s  /  0,8736  /  90,00%", "Não executado (limite de recurso)"]
    ]
    body_elements.append(make_table(t2_headers, t2_rows, "Tabela 2: Escalabilidade computacional da formulação QUBO sob variação de componentes PCA."))
    body_elements.append(make_p([make_run("Nota: * COBYLA limitado a 5 iterações; tempos reportados para uma única execução (N = 1).", italic=True, font_size=18)], jc="both", first_line=0, space_before=40, space_after=100, line_spacing=200))

    body_elements.append(make_p([make_run(
        "Na instância com 4 componentes, o QAOA registrou acurácia nominal de 96,67% (29 acertos em 30 amostras), superando a taxa de 90,00% "
        "obtida pela solução matematicamente ótima do solver exato. Atribui-se essa elevação pontual à hipótese de flutuação amostral decorrente "
        "da partição de teste reduzida (30 instâncias): ao interromper a busca em uma solução ligeiramente subótima no treino (f", font_size=21
    ), make_run("val", font_size=21, vert_align="subscript"), make_run(
        " = 0,8764), o deslocamento marginal do hiperplano classificou corretamente duas instâncias limítrofes adicionais. "
        "Os dados evidenciam a adequação da modelagem QUBO e demonstram que o custo de simulação clássica de vetores de estado em 2", font_size=21
    ), make_run("n", font_size=21, vert_align="superscript"), make_run(
        " amplitudes constitui o fator limitante para a expansão do QAOA a dimensões superiores em computadores tradicionais.", font_size=21
    )], jc="both", first_line=708, space_after=120, line_spacing=260))

    # 5 CONCLUSÃO
    body_elements.append(make_heading_1("5 CONCLUSÃO", num=False, space_before=200, space_after=100))
    body_elements.append(make_p([make_run(
        "Este trabalho avaliou a modelagem de tarefas de classificação supervisionada binária no paradigma combinatório QUBO resolvidas por "
        "QAOA em simuladores quânticos analíticos. Os resultados observados confirmaram a viabilidade da discretização de hiperplanos lineares, "
        "alcançando o mesmo valor ótimo de função objetivo (0,8736) e 90,00% de acurácia em instâncias de 2 e 3 componentes PCA, com o solver "
        "exato assegurando a estabilidade da formulação até 5 componentes.", font_size=21
    )], jc="both", first_line=708, space_after=80, line_spacing=260))

    body_elements.append(make_p([make_run(
        "A investigação empírica caracterizou os limites operacionais da abordagem: o QAOA foi avaliado de 2 a 4 componentes, "
        "registrando aumento substancial de tempo de 3,70 s para 863,42 s, enquanto a dimensão com 5 componentes foi restrita ao solver exato. "
        "Conclui-se que a formulação QUBO representa fielmente tarefas de classificação linear sem vazamento de dados, mas o escalonamento "
        "prático do QAOA em instâncias maiores dependerá de execuções em processadores quânticos físicos ou do emprego de simuladores por "
        "tensores e amostragem aproximada em trabalhos futuros.", font_size=21
    )], jc="both", first_line=708, space_after=120, line_spacing=260))

    # REFERÊNCIAS
    body_elements.append(make_heading_1("REFERÊNCIAS", num=False, space_before=160, space_after=80))
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
        body_elements.append(make_p([make_run(ref, font_size=19)], jc="both", first_line=0, space_after=40, line_spacing=210))

    # AGRADECIMENTOS
    body_elements.append(make_heading_1("AGRADECIMENTOS", num=False, space_before=160, space_after=80))
    body_elements.append(make_p([make_run(
        "Agradece-se à Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior pelo suporte institucional e de infraestrutura concedido ao desenvolvimento desta pesquisa.", font_size=21
    )], jc="both", first_line=708, space_after=120, line_spacing=260))

    # SOBRE OS AUTORES
    body_elements.append(make_heading_1("SOBRE O(S) AUTOR(ES)", num=False, space_before=160, space_after=80))
    body_elements.append(make_p([make_run("Sobre os autores:", bold=True, font_size=20)], jc="both", first_line=0, space_before=60, space_after=35, line_spacing=210))
    body_elements.append(make_p([make_run("_________________", bold=True, font_size=20)], jc="both", first_line=0, space_after=60, line_spacing=210))

    body_elements.append(make_p([make_run("i Julio Coronetti Regino (Autor)", bold=True, font_size=20)], jc="both", first_line=0, space_before=60, space_after=35, line_spacing=210, pStyle="Textodenotadefim"))
    body_elements.append(make_p([make_run("Discente do curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas na Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior. Desenvolve pesquisa de Iniciação Científica focada em algoritmos variacionais quânticos (QAOA, VQC) e otimização combinatória (QUBO) aplicados a machine learning. E-mail: julio.regino2@senaisp.edu.br.", font_size=19)], jc="both", first_line=0, space_after=80, line_spacing=230))

    body_elements.append(make_p([make_run("ii Cainã Antunes (Orientador)", bold=True, font_size=20)], jc="both", first_line=0, space_before=60, space_after=35, line_spacing=210, pStyle="Textodenotadefim"))
    body_elements.append(make_p([make_run("Docente e pesquisador na Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, atuando como orientador de projetos de iniciação científica e desenvolvimento tecnológico em inteligência artificial e computação avançada. E-mail: caina.silva@sp.senai.br.", font_size=19)], jc="both", first_line=0, space_after=60, line_spacing=230))

    sectPr = '<w:sectPr w:rsidR="0046777C" w:rsidRPr="00FF5642" w:rsidSect="00A223E8"><w:headerReference w:type="default" r:id="rId7"/><w:footerReference w:type="default" r:id="rId8"/><w:type w:val="continuous"/><w:pgSz w:w="11910" w:h="16840"/><w:pgMar w:top="1701" w:right="1134" w:bottom="1134" w:left="1701" w:header="720" w:footer="906" w:gutter="0"/><w:cols w:space="720"/></w:sectPr>'
    body_elements.append(sectPr)

    doc_header = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" xmlns:cx="http://schemas.microsoft.com/office/drawing/2014/chartex" xmlns:cx1="http://schemas.microsoft.com/office/drawing/2015/9/8/chartex" xmlns:cx2="http://schemas.microsoft.com/office/drawing/2015/10/21/chartex" xmlns:cx3="http://schemas.microsoft.com/office/drawing/2016/5/9/chartex" xmlns:cx4="http://schemas.microsoft.com/office/drawing/2016/5/10/chartex" xmlns:cx5="http://schemas.microsoft.com/office/drawing/2016/5/11/chartex" xmlns:cx6="http://schemas.microsoft.com/office/drawing/2016/5/12/chartex" xmlns:cx7="http://schemas.microsoft.com/office/drawing/2016/5/13/chartex" xmlns:cx8="http://schemas.microsoft.com/office/drawing/2016/5/14/chartex" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:aink="http://schemas.microsoft.com/office/drawing/2016/ink" xmlns:am3d="http://schemas.microsoft.com/office/drawing/2017/model3d" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid" xmlns:w16se="http://schemas.microsoft.com/office/word/2015/wordml/symex" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 w15 w16se w16cid wp14">
<w:body>'''

    doc_footer = '''</w:body></w:document>'''

    return doc_header + ''.join(body_elements) + doc_footer

def convert():
    print("Atualizando Resumo_Expandido_Julio_Regino_2026.docx com as correções refinadas do Advisor...")
    new_doc_xml = build_document_xml()
    new_footnotes_xml = build_footnotes_xml()
    
    for target in [OUTPUT_PATH, DIST_PATH]:
        with zipfile.ZipFile(TEMPLATE_PATH, 'r') as zin:
            with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    if item.filename == 'word/document.xml':
                        zout.writestr(item, new_doc_xml.encode('utf-8'))
                    elif item.filename == 'word/footnotes.xml':
                        zout.writestr(item, new_footnotes_xml.encode('utf-8'))
                    else:
                        zout.writestr(item, zin.read(item.filename))
        print(f"Sucesso! Arquivo .docx gerado em: {target}")

if __name__ == '__main__':
    convert()
