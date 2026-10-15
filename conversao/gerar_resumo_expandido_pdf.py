import zlib
import struct
import os

OUTPUT_PDF = 'conversao/Resumo_Expandido_Julio_Regino_2026.pdf'
CROPPED_LOGO_BIN = 'conversao/senai_cropped_logo.bin'
CROP_W = 133
CROP_H = 66

# Page geometry (A4 in points: 1 pt = 1/72 in)
PAGE_W = 595.28
PAGE_H = 841.89

# ABNT margins
MARGIN_LEFT = 85.04    # 3.0 cm
MARGIN_RIGHT = 56.70   # 2.0 cm
MARGIN_TOP = 85.04     # 3.0 cm
MARGIN_BOTTOM = 56.70  # 2.0 cm

PRINT_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT # 453.54 pt
PRINT_TOP = PAGE_H - MARGIN_TOP                # 756.85 pt
PRINT_BOTTOM = MARGIN_BOTTOM + 25.0            # 81.70 pt (above footer)

# Standard Helvetica character metrics (width per 1000 units)
HELVETICA_WIDTHS = {
    ' ': 278, '!': 278, '"': 355, '#': 556, '$': 556, '%': 889, '&': 667, "'": 191,
    '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333, '.': 278, '/': 278,
    '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, '7': 556,
    '8': 556, '9': 556, ':': 278, ';': 278, '<': 584, '=': 584, '>': 584, '?': 556,
    '@': 1015, 'A': 667, 'B': 667, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778,
    'H': 722, 'I': 278, 'J': 500, 'K': 667, 'L': 556, 'M': 833, 'N': 722, 'O': 778,
    'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 278, '\\': 278, ']': 278, '^': 469, '_': 556,
    '`': 333, 'a': 556, 'b': 556, 'c': 500, 'd': 556, 'e': 556, 'f': 278, 'g': 556,
    'h': 556, 'i': 222, 'j': 222, 'k': 500, 'l': 222, 'm': 833, 'n': 556, 'o': 556,
    'p': 556, 'q': 556, 'r': 333, 's': 500, 't': 278, 'u': 556, 'v': 500, 'w': 722,
    'x': 500, 'y': 500, 'z': 500, '{': 334, '|': 260, '}': 334, '~': 584,
    'á': 556, 'é': 556, 'í': 222, 'ó': 556, 'ú': 556, 'ã': 556, 'õ': 556, 'ç': 500,
    'à': 556, 'â': 556, 'ê': 556, 'ô': 556, 'Á': 667, 'É': 667, 'Í': 278, 'Ó': 778,
    'Ú': 722, 'Ã': 667, 'Õ': 778, 'Ç': 722, '–': 556, '—': 1000, '“': 333, '”': 333,
    '²': 333, '¹': 333, '°': 400
}

HELVETICA_BOLD_WIDTHS = {
    ' ': 278, '!': 333, '"': 474, '#': 556, '$': 556, '%': 889, '&': 722, "'": 238,
    '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333, '.': 278, '/': 278,
    '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, '7': 556,
    '8': 556, '9': 556, ':': 333, ';': 333, '<': 584, '=': 584, '>': 584, '?': 611,
    '@': 975, 'A': 722, 'B': 722, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778,
    'H': 722, 'I': 278, 'J': 556, 'K': 722, 'L': 611, 'M': 833, 'N': 722, 'O': 778,
    'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 333, '\\': 278, ']': 333, '^': 584, '_': 556,
    '`': 333, 'a': 556, 'b': 611, 'c': 556, 'd': 611, 'e': 556, 'f': 333, 'g': 611,
    'h': 611, 'i': 278, 'j': 278, 'k': 556, 'l': 278, 'm': 889, 'n': 611, 'o': 611,
    'p': 611, 'q': 611, 'r': 389, 's': 556, 't': 333, 'u': 611, 'v': 556, 'w': 778,
    'x': 556, 'y': 556, 'z': 500, '{': 389, '|': 280, '}': 389, '~': 584,
    'á': 556, 'é': 556, 'í': 278, 'ó': 611, 'ú': 611, 'ã': 556, 'õ': 611, 'ç': 556,
    'à': 556, 'â': 556, 'ê': 556, 'ô': 611, 'Á': 722, 'É': 667, 'Í': 278, 'Ó': 778,
    'Ú': 722, 'Ã': 722, 'Õ': 778, 'Ç': 722, '–': 556, '—': 1000, '“': 500, '”': 500
}

def string_width(text, font_size, bold=False):
    text = text.replace('č', 'c').replace('Č', 'C').replace('ě', 'e').replace('Ě', 'E').replace('∑', 'sum').replace('∈', 'in').replace('·', '*').replace('⁶', '^6').replace('¹²', '^12').replace('¹⁰', '^10')
    table = HELVETICA_BOLD_WIDTHS if bold else HELVETICA_WIDTHS
    w = sum(table.get(c, 556) for c in text)
    return (w / 1000.0) * font_size

def escape_pdf_str(text):
    text = text.replace('č', 'c').replace('Č', 'C').replace('ě', 'e').replace('Ě', 'E').replace('∑', 'sum').replace('∈', 'in').replace('·', '*').replace('⁶', '^6').replace('¹²', '^12').replace('¹⁰', '^10')
    b = text.encode('cp1252', errors='replace')
    out = bytearray()
    for byte in b:
        if byte in (ord('\\'), ord('('), ord(')')):
            out.append(ord('\\'))
        out.append(byte)
    return bytes(out).decode('latin1')

class PDFDoc:
    def __init__(self):
        self.pages = []
        self.current_page_stream = []
        self.current_y = PRINT_TOP
        self.page_number = 1
        self.start_new_page()

    def start_new_page(self):
        if self.current_page_stream:
            self.pages.append(self.current_page_stream)
            self.page_number += 1
        self.current_page_stream = []
        self.current_y = PRINT_TOP

    def check_space(self, height_needed):
        bot = (PRINT_BOTTOM + 45.0) if self.page_number == 1 else PRINT_BOTTOM
        if self.current_y - height_needed < bot:
            self.start_new_page()
            return True
        return False

    def add_command(self, cmd):
        self.current_page_stream.append(cmd)

    def draw_text(self, text, x, y, font="F1", size=11, bold=False, italic=False):
        f = "F2" if bold else ("F3" if italic else "F1")
        escaped = escape_pdf_str(text)
        cmd = f"BT /{f} {size} Tf {x:.2f} {y:.2f} Td ({escaped}) Tj ET"
        self.add_command(cmd)

    def draw_justified_line(self, text, x, y, width, font="F1", size=11, bold=False):
        f = "F2" if bold else "F1"
        escaped = escape_pdf_str(text)
        actual_w = string_width(text, size, bold=bold)
        num_spaces = text.count(' ')
        if num_spaces > 0 and actual_w < width:
            word_spacing = (width - actual_w) / num_spaces
            cmd = f"BT /{f} {size} Tf {word_spacing:.2f} Tw {x:.2f} {y:.2f} Td ({escaped}) Tj 0 Tw ET"
        else:
            cmd = f"BT /{f} {size} Tf {x:.2f} {y:.2f} Td ({escaped}) Tj ET"
        self.add_command(cmd)

    def add_paragraph(self, text, size=11, bold=False, italic=False, align="justify", first_line_indent=35.43, line_pitch=16.0, space_after=10.0):
        words = text.split(' ')
        lines = []
        cur_line = []
        is_first = True
        avail_w = PRINT_W - (first_line_indent if first_line_indent else 0)

        for w in words:
            test_line = ' '.join(cur_line + [w])
            test_w = string_width(test_line, size, bold=bold)
            if test_w <= avail_w:
                cur_line.append(w)
            else:
                if cur_line:
                    lines.append((' '.join(cur_line), is_first))
                    is_first = False
                    avail_w = PRINT_W
                    cur_line = [w]
                else:
                    lines.append((w, is_first))
                    is_first = False
                    avail_w = PRINT_W
                    cur_line = []
        if cur_line:
            lines.append((' '.join(cur_line), is_first))

        for idx, (line_text, first) in enumerate(lines):
            is_last = (idx == len(lines) - 1)
            self.check_space(line_pitch)
            indent = first_line_indent if first else 0
            x = MARGIN_LEFT + indent
            y = self.current_y

            if align == "center":
                w = string_width(line_text, size, bold=bold)
                x = MARGIN_LEFT + (PRINT_W - w) / 2.0
                self.draw_text(line_text, x, y, size=size, bold=bold, italic=italic)
            elif align == "justify" and not is_last:
                self.draw_justified_line(line_text, x, y, PRINT_W - indent, size=size, bold=bold)
            else:
                self.draw_text(line_text, x, y, size=size, bold=bold, italic=italic)

            self.current_y -= line_pitch

        self.current_y -= space_after

    def add_heading_1(self, text):
        self.check_space(35.0)
        self.current_y -= 8.0
        self.draw_text(text, MARGIN_LEFT, self.current_y, font="F2", size=12, bold=True)
        self.current_y -= 18.0

    def add_heading_2(self, text):
        self.check_space(30.0)
        self.current_y -= 6.0
        self.draw_text(text, MARGIN_LEFT, self.current_y, font="F2", size=11, bold=True)
        self.current_y -= 16.0

    def add_table(self, caption, headers, rows, col_widths):
        self.check_space(50.0 + len(rows) * 16.0)
        self.draw_text(caption, MARGIN_LEFT, self.current_y, font="F2", size=10, bold=True)
        self.current_y -= 14.0

        tbl_w = sum(col_widths)
        x_start = MARGIN_LEFT + (PRINT_W - tbl_w) / 2.0

        # Top border
        y_top = self.current_y + 4.0
        self.add_command(f"0.8 w 0 0 0 RG {x_start:.2f} {y_top:.2f} m {(x_start + tbl_w):.2f} {y_top:.2f} l S")

        # Header row
        x_curr = x_start
        for idx, h in enumerate(headers):
            hw = string_width(h, 9.5, bold=True)
            hx = x_curr + (col_widths[idx] - hw) / 2.0
            self.draw_text(h, hx, self.current_y - 8.0, font="F2", size=9.5, bold=True)
            x_curr += col_widths[idx]
        self.current_y -= 14.0

        # Header bottom border
        y_hbot = self.current_y + 2.0
        self.add_command(f"0.5 w 0 0 0 RG {x_start:.2f} {y_hbot:.2f} m {(x_start + tbl_w):.2f} {y_hbot:.2f} l S")

        # Rows
        for r in rows:
            x_curr = x_start
            for idx, c in enumerate(r):
                cw = string_width(c, 9.0, bold=False)
                cx = x_curr + 4.0 if (idx == 0 and len(c) > 4) else x_curr + (col_widths[idx] - cw) / 2.0
                self.draw_text(c, cx, self.current_y - 8.0, font="F1", size=9.0, bold=False)
                x_curr += col_widths[idx]
            self.current_y -= 14.0

        # Table bottom border
        y_bot = self.current_y + 2.0
        self.add_command(f"0.8 w 0 0 0 RG {x_start:.2f} {y_bot:.2f} m {(x_start + tbl_w):.2f} {y_bot:.2f} l S")
        self.current_y -= 12.0

    def add_author_bio(self, num_str, name, bio):
        self.check_space(65.0)
        self.draw_text(f"{num_str} {name}", MARGIN_LEFT, self.current_y, font="F2", size=10.5, bold=True)
        self.current_y -= 14.0

        tbl_w = PRINT_W
        x_start = MARGIN_LEFT
        foto_w = 70.0
        text_w = tbl_w - foto_w - 15.0

        # Photo placeholder box
        y_box_top = self.current_y
        box_h = 55.0
        self.add_command(f"0.5 w 0 0 0 RG {x_start:.2f} {(y_box_top - box_h):.2f} {foto_w:.2f} {box_h:.2f} re S")
        self.draw_text("Foto", x_start + 25.0, y_box_top - 32.0, font="F1", size=9.0)

        # Bio text
        words = bio.split(' ')
        cur_l = []
        cur_y = y_box_top - 10.0
        for w in words:
            test = ' '.join(cur_l + [w])
            if string_width(test, 9.5) <= text_w:
                cur_l.append(w)
            else:
                self.draw_text(' '.join(cur_l), x_start + foto_w + 12.0, cur_y, font="F1", size=9.5)
                cur_l = [w]
                cur_y -= 12.5
        if cur_l:
            self.draw_text(' '.join(cur_l), x_start + foto_w + 12.0, cur_y, font="F1", size=9.5)

        self.current_y = min(cur_y, y_box_top - box_h) - 15.0

    def finalize(self):
        if self.current_page_stream:
            self.pages.append(self.current_page_stream)

def build_pdf():
    print("Iniciando compilação de alta fidelidade para PDF seguindo rigorosamente o template original...")
    doc = PDFDoc()

    # Title PT (Bold, centered, Arial)
    doc.add_paragraph("EXPLORAÇÃO DO ALGORITMO QAOA PARA OTIMIZAÇÃO EM MODELOS DE CLASSIFICAÇÃO SUPERVISIONADA UTILIZANDO SIMULADORES QUÂNTICOS", size=12, bold=True, align="center", first_line_indent=0, line_pitch=16, space_after=6)

    # Title EN (Bold, centered, Arial)
    doc.add_paragraph("EXPLORATION OF THE QAOA ALGORITHM FOR OPTIMIZATION IN SUPERVISED CLASSIFICATION MODELS USING QUANTUM SIMULATORS", size=12, bold=True, align="center", first_line_indent=0, line_pitch=16, space_after=14)

    # Authors with footnote indices
    doc.add_paragraph("Julio Coronetti Regino ¹, i,  Cainã Antunes ², ii", size=12, bold=True, align="left", first_line_indent=0, line_pitch=16, space_after=14)

    # RESUMO
    doc.add_paragraph("RESUMO", size=12, bold=True, align="left", first_line_indent=0, line_pitch=14, space_after=4)
    resumo_text = ("Este estudo investiga a viabilidade de formulações de otimização combinatória quadrática associadas ao algoritmo QAOA em tarefas de classificação supervisionada binária, utilizando simuladores quânticos e confronto com métodos clássicos. O procedimento experimental empregou a base breast cancer da biblioteca scikit-learn, dividida de forma estratificada em treino (70%) e teste (30%). O pré-processamento consistiu em padronização por escore Z, redução dimensional por PCA e normalização linear no intervalo [0, 1]. Inicialmente, estabeleceu-se um controle comparativo formado por um classificador SVM linear clássico e um modelo VQC simulado. Em seguida, implementou-se uma formulação QUBO de classificador linear discretizado, resolvida via QAOA em instâncias de 2 a 4 componentes principais e por solver exato até 5 componentes. O baseline clássico SVM alcançou 100,00% de acurácia em 0,0009 s, enquanto o VQC obteve 83,33% em 12,81 s. Na abordagem QUBO resolvida com QAOA, a instância com 2 componentes atingiu 90,00% de acurácia em 3,70 s, e a instância com 4 componentes obteve 96,67% em 863,42 s, decorrente de flutuação amostral no limiar de decisão sobre o teste. Os resultados confirmam a convergência funcional do modelo em pequena escala e evidenciam o crescimento exponencial do tempo de simulação frente ao espaço combinatório de busca.")
    doc.add_paragraph(resumo_text, size=11, align="justify", first_line_indent=0, line_pitch=15.0, space_after=4)
    doc.add_paragraph("Palavras-chave: QAOA; QUBO; classificação supervisionada; aprendizado de máquina quântico; simuladores quânticos.", size=11, bold=False, align="left", first_line_indent=0, line_pitch=14, space_after=10)

    # ABSTRACT
    doc.add_paragraph("ABSTRACT", size=12, bold=True, align="left", first_line_indent=0, line_pitch=14, space_after=4)
    abstract_text = ("This study investigates the feasibility of quadratic combinatorial optimization formulations combined with the QAOA algorithm in binary supervised classification tasks, using quantum simulators and comparison with classical baselines. The experimental procedure employed the breast cancer dataset from scikit-learn, split with stratification into training (70%) and testing (30%) subsets. Preprocessing consisted of Z-score standardization, PCA dimensionality reduction, and linear min-max scaling to the [0, 1] interval. Initially, a comparative baseline was established with a classical linear SVM and a simulated VQC. Subsequently, a discretized linear classifier was formulated as a QUBO problem, solved via QAOA for instances with 2 to 4 principal components and via an exact solver up to 5 components. The classical SVM achieved 100.00% accuracy in 0.0009 s, while VQC achieved 83.33% in 12.81 s. In the QUBO formulation solved by QAOA, the 2-component instance reached 90.00% accuracy in 3.70 s, and the 4-component instance reached 96.67% in 863.42 s due to sampling boundary fluctuations on the test split. The findings confirm functional convergence in small instances and highlight exponential simulation overhead across the combinatorial search space.")
    doc.add_paragraph(abstract_text, size=11, italic=False, align="justify", first_line_indent=0, line_pitch=15.0, space_after=4)
    doc.add_paragraph("Keywords: QAOA; QUBO; supervised classification; quantum machine learning; quantum simulators.", size=11, italic=False, align="left", first_line_indent=0, line_pitch=14, space_after=14)

    # 1 INTRODUÇÃO (matching template)
    doc.add_heading_1("1 INTRODUÇÃO")
    doc.add_paragraph("A computação quântica possibilita novas abordagens para a modelagem de problemas de otimização combinatória e aprendizado de máquina. No estágio atual do desenvolvimento de hardware, denominado era NISQ (Noisy Intermediate-Scale Quantum), os dispositivos físicos possuem número limitado de qubits suscetíveis a ruído e decoerência, restringindo a profundidade viável dos circuitos (Preskill, 2018; Bharti et al., 2022). Diante dessas características físicas, os algoritmos híbridos variacionais clássico-quânticos consolidaram-se como metodologia prática para investigação empírica, distribuindo as etapas computacionais entre processadores quânticos parametrizados e rotinas clássicas de otimização (Cerezo et al., 2021; Grange; Poss; Bourreau, 2024).")

    doc.add_heading_2("1.1 Problema de pesquisa")
    doc.add_paragraph("A transposição de algoritmos de aprendizado supervisionado para ambientes quânticos requer o mapeamento de funções de custo em operadores Hamiltonianos tratáveis. Em simulações clássicas de circuitos quânticos, a exigência de memória e processamento cresce exponencialmente com o número de variáveis de estado. O problema investigado consiste em determinar a viabilidade técnica e os custos operacionais da modelagem de tarefas de classificação supervisionada sob a estrutura de Otimização Binária Quadrática Irrestrita (QUBO), avaliada por meio do algoritmo QAOA em simuladores de vetores de estado.")

    doc.add_heading_2("1.2 Objetivo(s)")
    doc.add_paragraph("O objetivo geral deste trabalho é avaliar o desempenho do algoritmo QAOA na resolução de tarefas de classificação supervisionada binária formuladas como QUBO, confrontando acurácia e tempo de processamento com modelos clássicos (SVM) e variacionais (VQC). Especificamente, busca-se: 1) Formular a tarefa de classificação binária como um problema de otimização quadrática discreta; 2) Avaliar a convergência do QAOA em instâncias de baixa dimensionalidade; 3) Medir comparativamente métricas de acurácia e tempo de execução; 4) Analisar a escalabilidade computacional frente ao acréscimo de atributos gerados por PCA.")

    doc.add_heading_2("1.3 Justificativa")
    doc.add_paragraph("O algoritmo QAOA (Quantum Approximate Optimization Algorithm) foi concebido para aproximar soluções em problemas combinatórios discretos (Farhi; Goldstone; Gutmann, 2014). Embora a classificação linear convencional seja solucionada por programação matemática contínua, a conversão para formulações QUBO permite investigar o comportamento de amostradores quânticos aplicados à minimização de erros de predição (Glover; Kochenberger; Du, 2019; Lucas, 2014). O foco da investigação reside em caracterizar a acurácia alcançável e a dinâmica de custo computacional dessa abordagem em cenários reduzidos, estabelecendo parâmetros empíricos sobre a viabilidade de execução em plataformas de simulação clássica.")

    # 2 REVISÃO DE LITERATURA (continuous flow as in template)
    doc.add_heading_1("2 REVISÃO DE LITERATURA")
    doc.add_paragraph("O paradigma variacional constitui a base operacional dos algoritmos para sistemas quânticos intermediários, estruturando a avaliação do estado quântico em circuitos parametrizados e o ajuste de ângulos por algoritmos de otimização clássicos (Preskill, 2018; Bharti et al., 2022; Cerezo et al., 2021). Investigações empíricas recentes sobre processadores físicos e simulados mostram que a fidelidade das portas lógicas e a conectividade física entre qubits condicionam a estabilidade dos modelos, demandando circuitos de baixa profundidade e controle rigoroso de ruídos de amostragem (Singh; Vishwakarma, 2026; Park; Son, 2026). Nesse contexto, Grange, Poss e Bourreau (2024) sistematizam o emprego de algoritmos variacionais na resolução de problemas combinatórios mapeados para matrizes de interação de spin.")
    doc.add_paragraph("O funcionamento do QAOA fundamenta-se na aplicação alternada de operadores de custo e operadores de mistura sobre uma superposição homogênea de estados (Farhi; Goldstone; Gutmann, 2014). O operador de custo reflete os termos da função objetivo booleana no circuito, enquanto o operador de mistura promove a transição entre estados da base computacional. O número de camadas do circuito controla a precisão da aproximação assintótica, sendo adotada a configuração unitária de uma camada em experimentos de simulação para limitar a complexidade temporal e atenuar a dispersão do gradiente durante o ajuste numérico.")
    doc.add_paragraph("No aprendizado de máquina quântico, a classificação baseia-se no mapeamento de vetores de atributos para espaços de Hilbert de alta dimensionalidade por meio de portas unitárias parametrizadas (Schuld; Killoran, 2019; Havlíček et al., 2019). Em revisão sistemática, Sood e Agrewal (2024) documentam que as abordagens predominantes envolvem classificadores variacionais e métodos de kernel quântico inspirados em Support Vector Machines (Rebentrost; Mohseni; Lloyd, 2014). A adaptação dessas arquiteturas para o domínio combinatório requer a discretização dos pesos do modelo, transpondo os coeficientes contínuos para um conjunto finito de variáveis binárias.")
    doc.add_paragraph("A compressão prévia dos atributos é apontada pela literatura como condição para viabilizar simulações quânticas com contagem controlada de qubits. Mancilla e Pere (2022) demonstram que a redução dimensional por Análise de Componentes Principais (PCA) atenua o custo de amostragem em rotinas de classificação quântica. De forma convergente, Qi et al. (2025) reportam que a elevação no número de atributos demanda acréscimo proporcional de qubits e sobrecarrega a convergência em modelos variacionais. Adicionalmente, a literatura reporta que o comportamento dos algoritmos variacionais depende diretamente do otimizador clássico selecionado (AL Ajmi; Shoaib, 2025). O método SPSA (Simultaneous Perturbation Stochastic Approximation), desenvolvido por Spall (1992), destaca-se em ambientes sujeitos a ruído por estimar o gradiente com número constante de avaliações da função objetivo, enquanto rotinas determinísticas baseadas em simplex, como o COBYLA, apresentam bom desempenho em superfícies suaves de baixa dimensão.")
    doc.add_paragraph("O modelo QUBO consiste na minimização irrestrita de funções quadráticas sobre vetores binários, correspondendo diretamente à formulação do vidro de spin de Ising (Glover; Kochenberger; Du, 2019; Lucas, 2014). Trabalhos recentes investigam o mapeamento de classificadores SVM para QUBO como mecanismo de exploração híbrida (Guddanti et al., 2024). Essa modelagem discretiza os parâmetros do hiperplano de separação e permite submeter a matriz de penalidades resultante a algoritmos quânticos de busca aproximada.")

    # 3 METODOLOGIA (matching template)
    doc.add_heading_1("3 METODOLOGIA")
    doc.add_paragraph("O experimento foi desenvolvido em linguagem Python, com base nos pacotes scikit-learn, Qiskit, Qiskit Machine Learning e Qiskit Optimization. A infraestrutura de testes foi estruturada em dois módulos analíticos: o módulo de calibração de baselines, composto por SVM linear clássico e classificador variacional quântico (VQC) simulado, e o módulo de otimização combinatória, responsável pela formulação QUBO e execuções via QAOA e solver exato.")
    doc.add_paragraph("Utilizou-se o conjunto de dados breast cancer da biblioteca scikit-learn. Extraiu-se uma amostra estratificada de 100 registros, preservando a proporção original das classes. A amostra foi segmentada em 70% para treinamento e 30% para teste com semente pseudoaleatória controlada. O protocolo de pré-processamento compreendeu três etapas encadeadas: 1) Padronização por escore Z via StandardScaler, com parâmetros ajustados estritamente sobre a partição de treino; 2) Redução dimensional por PCA, calculando as direções principais apenas com dados de treino; 3) Normalização linear no intervalo [0, 1] através do operador MinMaxScaler. Esse fluxo impediu vazamento de dados de teste para a etapa de ajuste dos modelos.")
    doc.add_paragraph("O modelo clássico de referência consistiu em um SVM com kernel linear. Em paralelo, implementou-se um circuito VQC simulado composto pelo mapa de características ZZFeatureMap, ansatz variacional RealAmplitudes e otimizador SPSA configurado com 100 iterações. Esse modelo forneceu o referencial quântico variacional inicial antes da transição para a abordagem combinatória.")
    doc.add_paragraph("No módulo de otimização combinatória, a tarefa de classificação binária foi modelada como um classificador linear discretizado. Os coeficientes angulares de cada componente e o termo independente de viés foram representados por pares de variáveis binárias que refletem contribuições positivas e negativas. Para uma dimensão de d componentes principais, o sistema resultou em n_bin = 2(d + 1) variáveis booleanas. A função objetivo minimizada adotou o critério de erro quadrático de margem: (1 / n) * sum (b + x_i * w - y_i)², onde b representa o viés discretizado, w é o vetor de pesos binários, x_i denota o vetor de atributos normalizados e y_i em {-1, +1} o rótulo de classe. Incorporou-se à matriz termos de regularização quadrática sobre a amplitude dos pesos e penalidades diagonais cruzadas para impedir a ativação simultânea de bits positivos e negativos pertencentes ao mesmo coeficiente.")
    doc.add_paragraph("O problema QUBO foi solucionado pelo QAOA com o operador StatevectorSampler, uma repetição (p = 1) e otimizador COBYLA. Para fins de controle da formulação matemática, desenvolveu-se também um resolvedor exato por enumeração exaustiva de estados, aplicado às instâncias de 2 a 5 componentes principais (2^6 a 2^12 estados). Registraram-se as variáveis de acurácia no conjunto de teste independente, tempo de execução em segundos, quantidade de componentes PCA e número de variáveis binárias.")

    # 4 RESULTADOS E DISCUSSÕES
    doc.add_heading_1("4 RESULTADOS E DISCUSSÕES")
    doc.add_paragraph("A Tabela 1 apresenta os resultados obtidos na etapa de calibração dos baselines. O SVM clássico linear atingiu 100,00% de acurácia no conjunto de teste em 0,0009 segundos. O classificador VQC simulado alcançou acurácia de 83,33% em 12,8098 segundos. Esse índice confirmou a capacidade do circuito variacional com emaranhamento em ajustar uma fronteira de separação eficaz, embora exigindo tempo computacional expressivamente superior ao método clássico.")

    doc.add_table(
        "Tabela 1: Resultado comparativo do baseline experimental.",
        ["Modelo", "Acurácia", "Tempo"],
        [["SVM linear", "100,00%", "0,0009 s"],
         ["VQC simulado", "83,33%", "12,8098 s"]],
        [150.0, 100.0, 100.0]
    )

    doc.add_paragraph("Na formulação QUBO com 2 componentes de PCA (Tabela 2), totalizando 6 variáveis binárias, o algoritmo QAOA convergiu em 3,6997 segundos com acurácia de 90,00% no conjunto de teste, enquanto o SVM linear manteve 100,00%. O resultado atesta que a discretização de parâmetros em variáveis booleanas preserva a capacidade discriminativa essencial da fronteira de classificação em dimensões reduzidas.")

    doc.add_table(
        "Tabela 2: Desempenho do QAOA em formulação QUBO com 2 componentes principais.",
        ["Modelo", "Variáveis binárias", "Acurácia", "Tempo"],
        [["SVM linear", "0", "100,00%", "0,0013 s"],
         ["QAOA-QUBO linear", "6", "90,00%", "3,6997 s"]],
        [140.0, 100.0, 80.0, 80.0]
    )

    doc.add_paragraph("A Tabela 3 consolida a avaliação da formulação QUBO utilizando o solver exato em instâncias de 2 a 5 componentes PCA. A acurácia manteve-se constante em 90,00% em todas as configurações testadas. O tempo necessário para a busca global aumentou progressivamente de 0,0824 segundos (6 variáveis, 64 estados) para 7,1497 segundos (12 variáveis, 4096 estados). A estabilidade do índice de acerto evidencia que a formulação quadrática discreta retém a consistência da solução, transferindo o gargalo operacional para o custo combinatório do espaço de busca.")

    doc.add_table(
        "Tabela 3: Avaliação por solver exato da formulação QUBO sob variação de componentes PCA.",
        ["PCA", "Variáveis binárias", "Acurácia QUBO", "Tempo QUBO"],
        [["2", "6", "90,00%", "0,0824 s"],
         ["3", "8", "90,00%", "0,4580 s"],
         ["4", "10", "90,00%", "1,2578 s"],
         ["5", "12", "90,00%", "7,1497 s"]],
        [70.0, 110.0, 110.0, 110.0]
    )

    doc.add_paragraph("A Tabela 4 detalha as execuções do algoritmo QAOA conforme o aumento da dimensão de entrada. O tempo de emulação quântica elevou-se para 41,7146 segundos com 3 componentes (8 variáveis) e alcançou 863,4231 segundos com 4 componentes (10 variáveis binárias, correspondendo a 1024 estados quânticos). Na instância com 4 componentes, a latência de cálculo impôs a redução do parâmetro de iterações do COBYLA de 20 para 5 iterações.")

    doc.add_table(
        "Tabela 4: Desempenho do algoritmo QAOA sob escalonamento de componentes PCA.",
        ["PCA", "Variáveis binárias", "Maxiter", "Acurácia QAOA", "Tempo QAOA"],
        [["2", "6", "20", "90,00%", "3,6997 s"],
         ["3", "8", "20", "90,00%", "41,7146 s"],
         ["4", "10", "5", "96,67%", "863,4231 s"]],
        [60.0, 100.0, 70.0, 100.0, 90.0]
    )

    doc.add_paragraph("Observa-se que na configuração com 4 componentes PCA, a acurácia no conjunto de teste alcançou 96,67% (29 acertos em 30 amostras), superando a taxa de 90,00% obtida pelo solver exato. Esse comportamento decorre da discretização dos pesos em um conjunto finito de valores e da sensibilidade do hiperplano de separação na partição de teste reduzida (30 instâncias): enquanto o solver exato minimizou estritamente a função de perda quadrática global sobre os dados de treino, a solução aproximada encontrada pelo QAOA gerou um deslocamento pontual do limiar de decisão que, fortuitamente, classificou corretamente duas amostras limítrofes adicionais no teste, caracterizando flutuação amostral.")

    doc.add_paragraph("A correlação entre as séries de teste reflete a distinção entre convergência funcional e escalabilidade computacional em simuladores de vetor de estado. Embora o QAOA tenha demonstrado capacidade de convergência em pequenas dimensões, a multiplicação matricial emulada em processadores clássicos sofre rápido decaimento de desempenho à medida que o número de variáveis cresce. O índice de 100,00% obtido pelo SVM clássico associa-se à separabilidade linear favorável proporcionada pelo PCA na amostra de 100 dados, indicando a conveniência de validações cruzadas adicionais em bases maiores. Esses padrões corroboram as análises de Qi et al. (2025), Park e Son (2026) e Singh e Vishwakarma (2026) quanto ao custo de profundidade e dimensionamento de variáveis quânticas.")

    # 5 Conclusão (matching template title case)
    doc.add_heading_1("5 Conclusão")
    doc.add_paragraph("Este trabalho avaliou a aplicação do algoritmo QAOA na otimização de modelos de classificação supervisionada binária sob modelagem QUBO em ambientes de simulação quântica. Os resultados obtidos confirmam a viabilidade funcional da formulação em pequenas instâncias, alcançando taxas de acurácia de 90,00% com 2 componentes principais e 96,67% com 4 componentes no conjunto de teste.")
    doc.add_paragraph("A contribuição da pesquisa reside na caracterização prática do pipeline de discretização de classificadores lineares em sistemas quadráticos binários e na mensuração empírica do tempo de execução emulado. A comparação com baselines clássicos evidencia que o SVM linear permanece como solução significativamente mais rápida em infraestruturas tradicionais. A rápida elevação temporal do QAOA sob emulação clássica delimita o gargalo de simulação frente à expansão do espaço combinatório.")
    doc.add_paragraph("Trabalhos futuros devem aprofundar formulações baseadas no problema dual exato do SVM, investigar técnicas de relaxação contínua para discretização e avaliar a execução dos circuitos em processadores quânticos físicos ou ambientes simulados com perfis específicos de ruído.")

    # Referências (matching template title case, unnumbered)
    doc.add_heading_1("Referências")
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
    for r in refs:
        doc.add_paragraph(r, size=9.5, align="justify", first_line_indent=0, line_pitch=13.0, space_after=5.0)

    # AGRADECIMENTOS (matching template exact naming)
    doc.add_heading_1("AGRADECIMENTOS")
    doc.add_paragraph("Agradece-se ao SENAI pelo apoio institucional ao desenvolvimento desta iniciação científica.")

    # SOBRE O(S)AUTOR(ES) (matching template exact naming)
    doc.add_heading_1("SOBRE O(S)AUTOR(ES)")
    doc.add_author_bio(
        "i", "Julio Coronetti Regino (Autor)",
        "Discente do curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas na Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior. Desenvolve pesquisa de Iniciação Científica focada em algoritmos variacionais quânticos (QAOA, VQC) e otimização combinatória (QUBO) aplicados a machine learning. E-mail: julio.regino2@senaisp.edu.br."
    )
    doc.add_author_bio(
        "ii", "Cainã Antunes (Orientador)",
        "Docente e pesquisador na Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, atuando como orientador de projetos de iniciação científica e desenvolvimento tecnológico em inteligência artificial e computação avançada. E-mail: caina.silva@sp.senai.br."
    )

    doc.finalize()

    # Read cropped image data
    with open(CROPPED_LOGO_BIN, 'rb') as f:
        img_zlib = f.read()

    # Logo display dimensions: cropped aspect ratio is 133 / 66 = 2.015:1
    disp_img_w = 60.0
    disp_img_h = (CROP_H / CROP_W) * disp_img_w # 29.77 pt
    img_x = MARGIN_LEFT + PRINT_W - disp_img_w   # 478.58 pt
    img_y = 18.0

    objects = []
    
    def add_obj(content):
        objects.append(content)
        return len(objects)

    objects.append(b"") # placeholder for 1: Catalog
    objects.append(b"") # placeholder for 2: Pages
    
    # 3: F1 Helvetica
    f1_idx = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    # 4: F2 Helvetica-Bold
    f2_idx = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    # 5: F3 Helvetica-Oblique
    f3_idx = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>")
    
    # 6: Image XObject (cropped SENAI logo)
    img_dict = f"<< /Type /XObject /Subtype /Image /Width {CROP_W} /Height {CROP_H} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode /Length {len(img_zlib)} >>\nstream\n".encode('latin1') + img_zlib + b"\nendstream"
    img_idx = add_obj(img_dict)

    page_obj_indices = []

    for p_num, p_stream in enumerate(doc.pages, start=1):
        decorations = []

        # 1. Red Header Wedge on top-right:
        # Path: 482.55 841.89 m 595.28 841.89 l 595.28 770.99 l 523.45 770.99 l f
        # Color: #F9131E -> 0.976 0.075 0.118 rg
        decorations.append("q")
        decorations.append("0.976 0.075 0.118 rg")
        decorations.append("482.55 841.89 m 595.28 841.89 l 595.28 770.99 l 523.45 770.99 l f")
        decorations.append("Q")

        # Page number inside red wedge (in black text)
        p_str = str(p_num)
        pw = string_width(p_str, 11)
        px = 556.0 - (pw / 2.0)
        decorations.append(f"BT /F1 11 Tf 0 0 0 rg {px:.2f} 800.00 Td ({p_str}) Tj ET")

        # 2. Gray Footer Trapezoid on bottom-left:
        # Path: 0 0 m 0 64.50 l 168.40 64.50 l 208.50 0 l f
        # Color: #EBEBEB -> 0.922 0.922 0.922 rg
        decorations.append("q")
        decorations.append("0.922 0.922 0.922 rg")
        decorations.append("0 0 m 0 64.50 l 168.40 64.50 l 208.50 0 l f")
        decorations.append("Q")

        # 3. Cropped SENAI Logo on bottom-right:
        decorations.append(f"q {disp_img_w:.2f} 0 0 {disp_img_h:.2f} {img_x:.2f} {img_y:.2f} cm /Im1 Do Q")

        # 4. Footnotes on Page 1:
        if p_num == 1:
            decorations.append(f"0.5 w 0 0 0 RG {MARGIN_LEFT:.2f} 80.00 m {(MARGIN_LEFT + 180.0):.2f} 80.00 l S")
            decorations.append(f"BT /F2 8 Tf 0 0 0 rg {MARGIN_LEFT:.2f} 68.00 Td (1) Tj ET")
            escaped_fn1 = escape_pdf_str(" Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, julio.regino2@senaisp.edu.br.")
            decorations.append(f"BT /F1 8.5 Tf 0 0 0 rg {(MARGIN_LEFT + 7.0):.2f} 68.00 Td ({escaped_fn1}) Tj ET")
            decorations.append(f"BT /F2 8 Tf 0 0 0 rg {MARGIN_LEFT:.2f} 56.00 Td (2) Tj ET")
            escaped_fn2 = escape_pdf_str(" Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, caina.silva@sp.senai.br.")
            decorations.append(f"BT /F1 8.5 Tf 0 0 0 rg {(MARGIN_LEFT + 7.0):.2f} 56.00 Td ({escaped_fn2}) Tj ET")

        # Reset text color to black for document stream
        full_stream_text = '\n'.join(decorations + ["0 0 0 rg 0 0 0 RG"] + p_stream)
        stream_bytes = full_stream_text.encode('latin1')
        comp_stream = zlib.compress(stream_bytes)

        stream_obj_dict = f"<< /Length {len(comp_stream)} /Filter /FlateDecode >>\nstream\n".encode('latin1') + comp_stream + b"\nendstream"
        stream_idx = add_obj(stream_obj_dict)

        page_idx = add_obj(b"") # placeholder
        page_obj_indices.append((page_idx, stream_idx))

    # Fill Page objects
    for page_idx, stream_idx in page_obj_indices:
        page_content = f"<< /Type /Page /Parent 2 0 R /MediaBox [ 0 0 {PAGE_W} {PAGE_H} ] /Contents {stream_idx} 0 R /Resources << /Font << /F1 {f1_idx} 0 R /F2 {f2_idx} 0 R /F3 {f3_idx} 0 R >> /XObject << /Im1 {img_idx} 0 R >> >> >>".encode('latin1')
        objects[page_idx - 1] = page_content

    # Fill Catalog (Obj 1) and Pages (Obj 2)
    objects[0] = b"<< /Type /Catalog /Pages 2 0 R >>"
    kids_str = ' '.join(f"{p_idx} 0 R" for p_idx, _ in page_obj_indices)
    objects[1] = f"<< /Type /Pages /Kids [ {kids_str} ] /Count {len(page_obj_indices)} >>".encode('latin1')

    # Assemble PDF with cross-reference table
    pdf_out = bytearray()
    pdf_out.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []

    for i, obj_data in enumerate(objects, start=1):
        offsets.append(len(pdf_out))
        pdf_out.extend(f"{i} 0 obj\n".encode('latin1'))
        pdf_out.extend(obj_data)
        pdf_out.extend(b"\nendobj\n")

    xref_offset = len(pdf_out)
    pdf_out.extend(f"xref\n0 {len(objects) + 1}\n".encode('latin1'))
    pdf_out.extend(b"0000000000 65535 f \n")
    for off in offsets:
        pdf_out.extend(f"{off:010d} 00000 n \n".encode('latin1'))

    pdf_out.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode('latin1'))

    with open(OUTPUT_PDF, 'wb') as f:
        f.write(pdf_out)

    print(f"Sucesso! PDF compilado em: {OUTPUT_PDF} com {len(page_obj_indices)} páginas.")

if __name__ == '__main__':
    build_pdf()
