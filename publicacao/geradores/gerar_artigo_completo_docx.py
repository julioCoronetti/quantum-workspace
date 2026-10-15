import zipfile
import xml.etree.ElementTree as ET
import os

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_PATH = str(BASE_DIR / "templates" / "Template_ResumoExpandido2026.docx")
OUTPUT_PATH = str(BASE_DIR / "dist" / "IC_Julio_Versao_Completa_2026.docx")

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

def make_heading_2(text):
    r = make_run(text, bold=True, font_size=22, font_name="Arial")
    return make_p([r], jc="both", first_line=0, space_after=100, line_spacing=280, pStyle="Ttulo2", keepNext=True)

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
      <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve"> Autor. Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, julio.regino2@senaisp.edu.br.</w:t></w:r>
    </w:p>
  </w:footnote>
  <w:footnote w:id="2">
    <w:p>
      <w:pPr><w:pStyle w:val="Textodenotaderodap"/></w:pPr>
      <w:r><w:rPr><w:rStyle w:val="Refdenotaderodap"/><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/></w:rPr><w:footnoteRef/></w:r>
      <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve"> Orientador. Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, caina.silva@sp.senai.br.</w:t></w:r>
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
    resumo_text = ("Este estudo avalia a viabilidade de formulações de otimização discreta associadas ao algoritmo QAOA em tarefas de classificação supervisionada, utilizando simuladores quânticos e comparação com métodos clássicos. A metodologia adotou o conjunto de dados breast cancer da biblioteca scikit-learn, com separação estratificada entre treino e teste, normalização, redução de dimensionalidade por PCA e avaliação por acurácia e tempo de execução. Inicialmente, foi estabelecido um baseline com SVM linear e VQC simulado. Em seguida, foi implementada uma formulação QUBO simplificada de classificador linear discretizado, resolvida por QAOA em instâncias pequenas e por solução exata em uma análise preliminar de escalabilidade. Os resultados indicaram que o baseline VQC atingiu 83,33% de acurácia, enquanto o SVM clássico atingiu 100,00%. Na etapa QUBO/QAOA, a instância com 2 componentes PCA obteve 90,00% de acurácia com QAOA, porém com tempo superior ao SVM.")
    body_elements.append(make_p([make_run(resumo_text, font_size=23)], jc="both", first_line=0, space_after=60, line_spacing=260))
    
    kw_pt = [make_run("Palavras-chave: ", bold=True, font_size=23), make_run("QAOA; QUBO; classificação supervisionada; aprendizado de máquina quântico; simuladores quânticos.", font_size=23)]
    body_elements.append(make_p(kw_pt, jc="both", first_line=0, space_after=140, line_spacing=260))

    body_elements.append(make_p([make_run("ABSTRACT", bold=True, font_size=24)], jc="both", first_line=0, space_after=60, line_spacing=260))
    abstract_text = ("This study evaluates the feasibility of discrete optimization formulations associated with the QAOA algorithm in supervised classification tasks, using quantum simulators and comparison with classical methods. The methodology used the breast cancer dataset from scikit-learn, with stratified train-test split, normalization, dimensionality reduction through PCA, and evaluation by accuracy and execution time. First, a baseline was established with a linear SVM and a simulated VQC. Then, a simplified QUBO formulation of a discretized linear classifier was implemented and solved with QAOA in small instances and with an exact solver in a preliminary scalability analysis. The results indicated that the VQC baseline reached 83.33% accuracy, while the classical SVM reached 100.00%. In the QUBO/QAOA stage, the instance with 2 PCA components achieved 90.00% accuracy with QAOA, although with higher execution time than SVM.")
    body_elements.append(make_p([make_run(abstract_text, italic=False, font_size=23)], jc="both", first_line=0, space_after=60, line_spacing=260))

    kw_en = [make_run("Keywords: ", bold=True, font_size=23), make_run("QAOA; QUBO; supervised classification; quantum machine learning; quantum simulators.", italic=False, font_size=23)]
    body_elements.append(make_p(kw_en, jc="both", first_line=0, space_after=180, line_spacing=260))

    body_elements.append(make_heading_1("1 INTRODUÇÃO", num=False))
    body_elements.append(make_p([make_run(
        "A computação quântica ainda não substitui os métodos clássicos de aprendizado de máquina, mas já permite investigar novas formas de formular problemas de otimização. Esse recorte é especialmente importante na era NISQ, em que os dispositivos possuem número limitado de qubits, ruído e restrições de profundidade de circuito (Preskill, 2018; Bharti et al., 2022). Por isso, algoritmos híbridos variacionais, que combinam circuitos quânticos parametrizados com rotinas clássicas de otimização, tornaram-se uma alternativa prática para estudos exploratórios (Cerezo et al., 2021; Grange; Poss; Bourreau, 2024)."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    body_elements.append(make_p([make_run(
        "Entre esses algoritmos, o QAOA (Quantum Approximate Optimization Algorithm) se destaca por lidar diretamente com problemas de otimização combinatória (Farhi; Goldstone; Gutmann, 2014). A classificação supervisionada, embora normalmente tratada por modelos estatísticos ou geométricos, também pode ser interpretada como um problema de busca por parâmetros que minimizam uma função de erro. A partir dessa ligação, este trabalho converte uma tarefa de classificação binária em uma formulação QUBO (Quadratic Unconstrained Binary Optimization) e avalia sua resolução por simulação quântica (Glover; Kochenberger; Du, 2019; Lucas, 2014)."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    body_elements.append(make_p([make_run(
        "A questão central não é demonstrar vantagem quântica, mas verificar até onde uma formulação QUBO associada ao QAOA consegue produzir resultados utilizáveis em uma tarefa pequena de classificação. Para isso, a abordagem foi comparada com SVM linear e VQC simulado, considerando acurácia, tempo de execução e crescimento do número de variáveis binárias após a variação de componentes PCA."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("2 REVISÃO DE LITERATURA", num=False))
    body_elements.append(make_p([make_run(
        "Esta seção organiza os conceitos que orientaram o experimento. As referências foram usadas para justificar três decisões principais: trabalhar em escala compatível com a era NISQ, reduzir dimensionalidade antes dos circuitos e tratar a formulação QUBO como uma ponte experimental entre classificação e otimização combinatória."
    )], jc="both", first_line=708, space_after=100, line_spacing=300))

    body_elements.append(make_heading_2("2.1 Computação quântica na era NISQ"))
    body_elements.append(make_p([make_run(
        "A era NISQ descreve um estágio em que processadores quânticos possuem quantidade limitada de qubits, conectividade restrita e presença de ruído. Essa limitação ajuda a explicar por que este trabalho adota simulação e instâncias pequenas, em vez de propor uma solução quântica em larga escala. Algoritmos híbridos, que distribuem o processo entre circuitos quânticos e otimizadores clássicos, tornam-se uma alternativa prática para esse tipo de investigação (Preskill, 2018; Bharti et al., 2022). Estudos recentes com processadores reais e VQCs reforçam a mesma cautela: ruído, orçamento de medições, profundidade de circuito e condições de hardware afetam diretamente a estabilidade dos resultados (Singh; Vishwakarma, 2026; Park; Son, 2026)."
    )], jc="both", first_line=708, space_after=100, line_spacing=300))

    body_elements.append(make_heading_2("2.2 Algoritmos variacionais e QAOA"))
    body_elements.append(make_p([make_run(
        "O QAOA é um algoritmo variacional voltado a problemas de otimização combinatória. Seu funcionamento alterna operadores associados ao custo do problema e operadores de mistura, enquanto os parâmetros são ajustados por um otimizador clássico (Farhi; Goldstone; Gutmann, 2014). Essa estrutura torna o QAOA adequado para este estudo porque um problema QUBO pode ser convertido em Hamiltoniano de custo e avaliado por circuitos parametrizados, seguindo o paradigma mais amplo dos algoritmos quânticos variacionais (Cerezo et al., 2021; Grange; Poss; Bourreau, 2024)."
    )], jc="both", first_line=708, space_after=100, line_spacing=300))

    body_elements.append(make_heading_2("2.3 Aprendizado de máquina quântico e classificação"))
    body_elements.append(make_p([make_run(
        "No aprendizado de máquina quântico, modelos de classificação podem usar circuitos quânticos para mapear dados clássicos em espaços de maior dimensionalidade ou para resolver formulações de otimização ligadas ao treinamento de classificadores (Schuld; Killoran, 2019; Havlíček et al., 2019). Revisões recentes indicam que QML ainda é um campo em consolidação, com aplicações recorrentes em classificadores, redes neurais quânticas e métodos de kernel (Sood; Agrewal, 2024). Neste trabalho, o SVM cumpre dois papéis: serve como baseline clássico forte e também como referência conceitual, já que aparece na literatura de aprendizado de máquina quântico aplicada à classificação (Rebentrost; Mohseni; Lloyd, 2014)."
    )], jc="both", first_line=708, space_after=100, line_spacing=300))

    body_elements.append(make_heading_2("2.4 Pré-processamento, dimensionalidade e otimizadores"))
    body_elements.append(make_p([make_run(
        "O pré-processamento dos dados é uma etapa crítica em modelos quânticos de classificação. Estudos sobre QML indicam que técnicas clássicas de codificação e redução de dimensionalidade influenciam diretamente o desempenho de modelos variacionais em ambientes NISQ (Mancilla; Pere, 2022). Esse ponto justifica o uso de PCA no experimento: reduzir atributos diminui a quantidade de variáveis e torna a simulação viável. A mesma preocupação aparece em estudos sobre VQCs aplicados a dados de alta dimensionalidade, nos quais o aumento do número de atributos demanda mais qubits, eleva o tempo de treinamento e dificulta a convergência (Qi et al., 2025). Além disso, a seleção do otimizador clássico pode alterar tanto a acurácia quanto o tempo de treinamento em modelos de QML, o que justifica o uso de SPSA e COBYLA em etapas diferentes do estudo (AL Ajmi; Shoaib, 2025)."
    )], jc="both", first_line=708, space_after=100, line_spacing=300))

    body_elements.append(make_heading_2("2.5 Formulações QUBO"))
    body_elements.append(make_p([make_run(
        "Um problema QUBO consiste em minimizar uma função quadrática sem restrições explícitas sobre variáveis binárias. Essa formulação é útil por permitir a representação de problemas combinatórios e sua posterior conversão para modelos compatíveis com algoritmos quânticos de otimização (Glover; Kochenberger; Du, 2019; Lucas, 2014). Em classificação, há trabalhos recentes que exploram a representação de SVM como problema QUBO e comparam abordagens clássicas, quânticas e híbridas (Guddanti et al., 2024). Neste estudo, a formulação QUBO foi usada de forma mais restrita: ela funciona como uma aproximação experimental de classificador linear discretizado, suficiente para avaliar o comportamento inicial do QAOA, mas sem substituir uma formulação completa do SVM."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("3 METODOLOGIA", num=False))
    body_elements.append(make_p([make_run(
        "O experimento foi desenvolvido em Python, utilizando as bibliotecas scikit-learn, Qiskit, Qiskit Machine Learning, Qiskit Optimization e Qiskit Algorithms. A implementação foi organizada em dois scripts principais: script.py, responsável pelo baseline clássico e VQC, e script_qaoa.py, responsável pela formulação QUBO e pelas execuções com QAOA."
    )], jc="both", first_line=708, space_after=100, line_spacing=300))

    body_elements.append(make_heading_2("3.1 Base de dados e pré-processamento"))
    body_elements.append(make_p([make_run(
        "Foi utilizado o conjunto de dados breast cancer, disponibilizado pela biblioteca scikit-learn. A amostra utilizada nos experimentos possui 100 registros selecionados de forma estratificada, mantendo a proporção entre as classes. Em seguida, os dados foram divididos em 70% para treino e 30% para teste, também com estratificação."
    )], jc="both", first_line=708, space_after=80, line_spacing=300))

    body_elements.append(make_p([make_run(
        "O pré-processamento seguiu as seguintes etapas:"
    )], jc="both", first_line=708, space_after=60, line_spacing=300))

    body_elements.append(make_p([
        make_run("1. ", bold=True),
        make_run("Padronização dos atributos com StandardScaler, ajustado apenas no conjunto de treino.")
    ], jc="both", first_line=354, space_after=40, line_spacing=260))

    body_elements.append(make_p([
        make_run("2. ", bold=True),
        make_run("Redução de dimensionalidade com PCA, também ajustado apenas no treino.")
    ], jc="both", first_line=354, space_after=40, line_spacing=260))

    body_elements.append(make_p([
        make_run("3. ", bold=True),
        make_run("Reescala dos componentes para o intervalo [0, 1] com MinMaxScaler.")
    ], jc="both", first_line=354, space_after=60, line_spacing=260))

    body_elements.append(make_p([make_run(
        "Essa organização evita vazamento de informação do conjunto de teste para o treinamento."
    )], jc="both", first_line=708, space_after=100, line_spacing=300))

    body_elements.append(make_heading_2("3.2 Baseline clássico e baseline quântico variacional"))
    body_elements.append(make_p([make_run(
        "O primeiro baseline foi um SVM linear, usado como referência clássica. Em seguida, foi implementado um classificador variacional quântico simulado (VQC), com mapa de características ZZFeatureMap, ansatz RealAmplitudes e otimizador SPSA com maxiter=100. O SPSA foi escolhido por ser um método de aproximação estocástica com perturbações simultâneas, frequentemente associado a cenários de otimização com ruído (Spall, 1992). Essa etapa teve como objetivo estabilizar um modelo quântico inicial antes da formulação QUBO/QAOA."
    )], jc="both", first_line=708, space_after=100, line_spacing=300))

    body_elements.append(make_heading_2("3.3 Formulação QUBO"))
    body_elements.append(make_p([make_run(
        "Na etapa principal, a classificação foi representada como um classificador linear discretizado. Cada coeficiente do modelo, incluindo o viés, foi codificado por variáveis binárias de contribuição positiva e negativa. Para d componentes PCA, o número de variáveis binárias foi definido como:"
    )], jc="both", first_line=708, space_after=60, line_spacing=300))

    body_elements.append(make_p([make_run("n_bin = 2(d + 1)", italic=True, font_size=24)], jc="center", first_line=0, space_after=60, line_spacing=260))

    body_elements.append(make_p([make_run(
        "A função objetivo minimizada foi uma perda quadrática de margem:"
    )], jc="both", first_line=708, space_after=60, line_spacing=300))

    body_elements.append(make_p([make_run("L(w, b) = (1 / n) * ∑ (b + x_i · w - y_i)²", italic=True, font_size=24)], jc="center", first_line=0, space_after=60, line_spacing=260))

    body_elements.append(make_p([make_run(
        "em que b representa o viés, w os pesos discretizados, x_i os atributos após PCA e y_i ∈ {-1, 1} a classe transformada. Também foram adicionadas regularização quadrática dos coeficientes e penalização para evitar ativação simultânea de bits positivos e negativos do mesmo coeficiente."
    )], jc="both", first_line=708, space_after=80, line_spacing=300))

    body_elements.append(make_p([make_run(
        "É importante destacar que esta formulação é uma aproximação experimental de classificador linear discretizado em QUBO, e não uma implementação completa do SVM dual."
    )], jc="both", first_line=708, space_after=100, line_spacing=300))

    body_elements.append(make_heading_2("3.4 Execução com QAOA e solver exato"))
    body_elements.append(make_p([make_run(
        "O QUBO foi resolvido por QAOA em instâncias pequenas, usando StatevectorSampler, QAOA com reps=1 e otimizador COBYLA. Para avaliar a escalabilidade da formulação sem sobrecarregar o ambiente de execução, também foi implementado um solver exato por força bruta para os QUBOs pequenos. Esse solver foi utilizado na análise preliminar com PCA variando de 2 a 5 componentes."
    )], jc="both", first_line=708, space_after=80, line_spacing=300))

    body_elements.append(make_p([make_run(
        "As métricas coletadas foram acurácia, tempo de execução, número de componentes PCA e número de variáveis binárias."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("4 RESULTADOS E DISCUSSÕES", num=False))
    body_elements.append(make_heading_2("4.1 Baseline da Fase 1"))
    body_elements.append(make_p([make_run(
        "O primeiro resultado funciona como controle para as etapas seguintes. O baseline clássico com SVM atingiu 100,00% de acurácia no conjunto de teste, enquanto o VQC simulado atingiu 83,33%. Assim, o modelo quântico variacional superou o critério prático de 80% estabelecido para a Fase 1, mas ainda com tempo de execução superior ao SVM."
    )], jc="both", first_line=708, space_after=80, line_spacing=300))

    t1_headers = ["Modelo", "Acurácia", "Tempo"]
    t1_rows = [
        ["SVM linear", "100,00%", "0,0009 s"],
        ["VQC simulado", "83,33%", "12,8098 s"]
    ]
    body_elements.append(make_table(t1_headers, t1_rows, "Tabela 1: Resultado do baseline da Fase 1."))

    body_elements.append(make_heading_2("4.2 Execução inicial QUBO/QAOA"))
    body_elements.append(make_p([make_run(
        "Na etapa QUBO/QAOA inicial, foi executada uma instância com 2 componentes PCA, totalizando 6 variáveis binárias. O QAOA obteve 90,00% de acurácia, enquanto o SVM linear manteve 100,00%. Esse resultado não indica superioridade do método quântico, mas mostra que a formulação proposta consegue gerar uma fronteira de decisão utilizável em escala pequena."
    )], jc="both", first_line=708, space_after=80, line_spacing=300))

    t2_headers = ["Modelo", "Variáveis binárias", "Acurácia", "Tempo"]
    t2_rows = [
        ["SVM linear", "0", "100,00%", "0,0013 s"],
        ["QAOA-QUBO linear", "6", "90,00%", "3,6997 s"]
    ]
    body_elements.append(make_table(t2_headers, t2_rows, "Tabela 2: Execução inicial QAOA/QUBO com 2 componentes PCA."))

    body_elements.append(make_heading_2("4.3 Análise preliminar de escalabilidade"))
    body_elements.append(make_p([make_run(
        "Para observar o impacto do aumento de dimensionalidade, foi utilizado o solver exato em QUBOs com PCA variando de 2 a 5 componentes. A acurácia permaneceu em 90,00%, mas o tempo de solução aumentou conforme o número de variáveis binárias cresceu. Essa etapa separa dois aspectos do problema: a qualidade da formulação de classificação e o custo de busca no espaço binário."
    )], jc="both", first_line=708, space_after=80, line_spacing=300))

    t3_headers = ["PCA", "Variáveis binárias", "Acurácia QUBO", "Tempo QUBO"]
    t3_rows = [
        ["2", "6", "90,00%", "0,0824 s"],
        ["3", "8", "90,00%", "0,4580 s"],
        ["4", "10", "90,00%", "1,2578 s"],
        ["5", "12", "90,00%", "7,1497 s"]
    ]
    body_elements.append(make_table(t3_headers, t3_rows, "Tabela 3: Resultado preliminar do QUBO exato por número de componentes PCA."))

    body_elements.append(make_p([make_run(
        "Com QAOA, o custo de execução cresceu de forma mais acentuada. A instância com 3 componentes PCA levou 41,7146 segundos, enquanto a instância com 4 componentes PCA, mesmo com maxiter=5, levou 863,4231 segundos."
    )], jc="both", first_line=708, space_after=80, line_spacing=300))

    t4_headers = ["PCA", "Variáveis binárias", "Maxiter", "Acurácia QAOA", "Tempo QAOA"]
    t4_rows = [
        ["2", "6", "20", "90,00%", "3,6997 s"],
        ["3", "8", "20", "90,00%", "41,7146 s"],
        ["4", "10", "5", "96,67%*", "863,4231 s"]
    ]
    body_elements.append(make_table(t4_headers, t4_rows, "Tabela 4: Resultado preliminar das execuções QAOA por número de componentes PCA."))
    body_elements.append(make_p([make_run("Nota: * Otimizador COBYLA limitado a 5 iterações por restrição de tempo de simulação.", italic=True, font_size=18)], jc="both", first_line=0, space_after=80, line_spacing=200))

    body_elements.append(make_p([make_run(
        "Em conjunto, os resultados mostram uma diferença importante entre funcionar e escalar. A formulação QUBO/QAOA produziu classificações coerentes em instâncias pequenas, mas o custo de simulação cresceu rapidamente. A comparação com o SVM deixa claro que a viabilidade da abordagem não pode ser avaliada apenas pela acurácia: tempo de execução, número de variáveis binárias e escalabilidade são parte central da análise. Essa interpretação é consistente com estudos recentes sobre VQCs e dispositivos NISQ, que indicam sensibilidade a codificação, profundidade de circuito, ruído e dimensionalidade dos dados (Qi et al., 2025; Park; Son, 2026; Singh; Vishwakarma, 2026)."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("5 CONCLUSÃO", num=False))
    body_elements.append(make_p([make_run(
        "Este trabalho analisou, em caráter exploratório, o uso de QAOA e formulações QUBO em uma tarefa de classificação supervisionada. O SVM clássico manteve o melhor desempenho geral em acurácia e tempo, enquanto o VQC e a formulação QAOA/QUBO demonstraram viabilidade apenas em instâncias pequenas."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    body_elements.append(make_p([make_run(
        "A principal contribuição do estudo está na formulação e na análise de seus limites, não na defesa de superioridade quântica. A classificação foi convertida em um problema de otimização discreta, resolvido por QAOA em cenários controlados. A instância com 2 componentes PCA atingiu 90,00% de acurácia, demonstrando que a abordagem pode produzir uma solução competitiva em pequena escala. No entanto, o aumento do número de variáveis binárias elevou significativamente o tempo de execução, especialmente nas simulações com QAOA."
    )], jc="both", first_line=708, space_after=90, line_spacing=300))

    body_elements.append(make_p([make_run(
        "Como próximos passos, recomenda-se investigar formulações QUBO mais próximas do SVM dual, testar diferentes discretizações dos pesos, avaliar outros otimizadores clássicos e executar experimentos em ambientes com maior capacidade computacional. Também seria relevante comparar os resultados com simulações ruidosas ou hardware quântico real, para aproximar o estudo das limitações observadas em dispositivos NISQ."
    )], jc="both", first_line=708, space_after=140, line_spacing=300))

    body_elements.append(make_heading_1("AGRADECIMENTOS", num=False))
    body_elements.append(make_p([make_run(
        "Agradece-se à Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior pelo suporte institucional e de infraestrutura concedido ao desenvolvimento desta pesquisa."
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
        "PARK, S.; SON, Y. Sensitivity Analysis of Variational Quantum Classifiers for Identifying Dummy Power Traces in Side-Channel Analysis. Applied Sciences, v. 16, n. 7, p. 3243, 2026.",
        "PRESKILL, J. Quantum Computing in the NISQ era and beyond. Quantum, v. 2, p. 79, 2018.",
        "QI, H. et al. A high-efficiency variational quantum classifier for high-dimensional data. Journal of Supercomputing, v. 81, p. 1–20, 2025.",
        "REBENTROST, P.; MOHSENI, M.; LLOYD, S. Quantum support vector machine for big data classification. Physical Review Letters, v. 113, p. 130503, 2014.",
        "SCHULD, M.; KILLORAN, N. Quantum Machine Learning in Feature Hilbert Spaces. Physical Review Letters, v. 122, p. 040504, 2019.",
        "SINGH, S.; VISHWAKARMA, D. K. Performance Analysis of Quantum Arithmetic Circuits on IBM Eagle Processor. Defence Science Journal, v. 76, n. 2, p. 233-241, 2026.",
        "SOOD, S. K.; AGREWAL, M. Quantum Machine Learning for Computational Methods in Engineering: A Systematic Review. Archives of Computational Methods in Engineering, v. 31, n. 3, p. 1555–1577, 2024.",
        "SPALL, J. C. Multivariate stochastic approximation using a simultaneous perturbation gradient approximation. IEEE Transactions on Automatic Control, v. 37, n. 3, p. 332–341, 1992."
    ]
    for ref in refs:
        body_elements.append(make_p([make_run(ref, font_size=20)], jc="both", first_line=0, space_after=50, line_spacing=220))

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

if __name__ == '__main__':
    convert()
