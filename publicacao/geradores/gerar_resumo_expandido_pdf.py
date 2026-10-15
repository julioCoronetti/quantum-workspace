import zlib
import struct
import os

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_PDF = str(BASE_DIR / "dist" / "Resumo_Expandido_Julio_Regino_2026.pdf")
CROPPED_LOGO_BIN = str(BASE_DIR / "templates" / "senai_cropped_logo.bin")
CROP_W = 133
CROP_H = 66

PAGE_W = 595.28
PAGE_H = 841.89

MARGIN_LEFT = 85.04
MARGIN_RIGHT = 56.70
MARGIN_TOP = 85.04
MARGIN_BOTTOM = 56.70

PRINT_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
PRINT_TOP = PAGE_H - MARGIN_TOP
PRINT_BOTTOM = MARGIN_BOTTOM + 25.0

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
    text = text.replace('č', 'c').replace('Č', 'C').replace('ě', 'e').replace('Ě', 'E').replace('∑', 'sum').replace('∈', 'in').replace('·', '*').replace('⁶', '^6').replace('⁸', '^8').replace('¹²', '^12').replace('¹⁰', '^10')
    table = HELVETICA_BOLD_WIDTHS if bold else HELVETICA_WIDTHS
    w = sum(table.get(c, 556) for c in text)
    return (w / 1000.0) * font_size

def escape_pdf_str(text):
    text = text.replace('č', 'c').replace('Č', 'C').replace('ě', 'e').replace('Ě', 'E').replace('∑', 'sum').replace('∈', 'in').replace('·', '*').replace('⁶', '^6').replace('⁸', '^8').replace('¹²', '^12').replace('¹⁰', '^10')
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

    def add_paragraph(self, text, size=11, bold=False, italic=False, align="justify", first_line_indent=35.43, line_pitch=14.5, space_after=6.0):
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

        total_h = len(lines) * line_pitch + space_after
        self.check_space(total_h)

        for idx, (line_text, first_in_p) in enumerate(lines):
            indent = (first_line_indent if first_in_p and first_line_indent else 0)
            x = MARGIN_LEFT + indent
            y = self.current_y
            line_w = PRINT_W - indent
            is_last = (idx == len(lines) - 1)

            if align == "center":
                w = string_width(line_text, size, bold=bold)
                cx = MARGIN_LEFT + (PRINT_W - w) / 2.0
                self.draw_text(line_text, cx, y, size=size, bold=bold, italic=italic)
            elif align == "justify" and not is_last and len(line_text.split(' ')) > 1:
                self.draw_justified_line(line_text, x, y, line_w, size=size, bold=bold)
            else:
                self.draw_text(line_text, x, y, size=size, bold=bold, italic=italic)

            self.current_y -= line_pitch

        self.current_y -= space_after

    def add_heading_1(self, text):
        self.check_space(55.0)
        self.current_y -= 8.0
        self.draw_text(text, MARGIN_LEFT, self.current_y, font="F2", size=12, bold=True)
        self.current_y -= 16.0

    def add_table(self, caption, headers, rows, col_widths):
        self.check_space(50.0 + len(rows) * 16.0)
        self.draw_text(caption, MARGIN_LEFT, self.current_y, font="F2", size=9.5, bold=True)
        self.current_y -= 13.0

        tbl_w = sum(col_widths)
        x_start = MARGIN_LEFT + (PRINT_W - tbl_w) / 2.0

        y_top = self.current_y + 4.0
        self.add_command(f"0.8 w 0 0 0 RG {x_start:.2f} {y_top:.2f} m {(x_start + tbl_w):.2f} {y_top:.2f} l S")

        x_curr = x_start
        for idx, h in enumerate(headers):
            hw = string_width(h, 9.0, bold=True)
            hx = x_curr + (col_widths[idx] - hw) / 2.0
            self.draw_text(h, hx, self.current_y - 8.0, font="F2", size=9.0, bold=True)
            x_curr += col_widths[idx]
        self.current_y -= 13.0

        y_hbot = self.current_y + 2.0
        self.add_command(f"0.5 w 0 0 0 RG {x_start:.2f} {y_hbot:.2f} m {(x_start + tbl_w):.2f} {y_hbot:.2f} l S")

        for r in rows:
            x_curr = x_start
            for idx, c in enumerate(r):
                cw = string_width(c, 8.5, bold=False)
                cx = x_curr + 4.0 if (idx == 0 and len(c) > 4) else x_curr + (col_widths[idx] - cw) / 2.0
                self.draw_text(c, cx, self.current_y - 8.0, font="F1", size=8.5, bold=False)
                x_curr += col_widths[idx]
            self.current_y -= 13.0

        y_bot = self.current_y + 2.0
        self.add_command(f"0.8 w 0 0 0 RG {x_start:.2f} {y_bot:.2f} m {(x_start + tbl_w):.2f} {y_bot:.2f} l S")
        self.current_y -= 10.0

    def add_author_bio(self, num_str, name, bio):
        self.check_space(60.0)
        self.draw_text(f"{num_str} {name}", MARGIN_LEFT, self.current_y, font="F2", size=10.0, bold=True)
        self.current_y -= 12.0

        tbl_w = PRINT_W
        x_start = MARGIN_LEFT
        foto_w = 65.0
        text_w = tbl_w - foto_w - 15.0

        y_box_top = self.current_y
        box_h = 50.0
        self.add_command(f"0.5 w 0 0 0 RG {x_start:.2f} {(y_box_top - box_h):.2f} {foto_w:.2f} {box_h:.2f} re S")
        self.draw_text("Foto", x_start + 24.0, y_box_top - 28.0, font="F1", size=9.0)

        words = bio.split(' ')
        cur_l = []
        cur_y = y_box_top - 10.0
        for w in words:
            test = ' '.join(cur_l + [w])
            if string_width(test, 9.0) <= text_w:
                cur_l.append(w)
            else:
                self.draw_text(' '.join(cur_l), x_start + foto_w + 12.0, cur_y, font="F1", size=9.0)
                cur_l = [w]
                cur_y -= 12.0
        if cur_l:
            self.draw_text(' '.join(cur_l), x_start + foto_w + 12.0, cur_y, font="F1", size=9.0)

        self.current_y = min(cur_y, y_box_top - box_h) - 12.0

    def finalize(self):
        if self.current_page_stream:
            self.pages.append(self.current_page_stream)

def build_pdf():
    print("Iniciando compilação do Resumo Expandido em PDF com layout oficial UniSENAI 2026...")
    doc = PDFDoc()

    doc.add_paragraph("EXPLORAÇÃO DO ALGORITMO QAOA PARA OTIMIZAÇÃO EM MODELOS DE CLASSIFICAÇÃO SUPERVISIONADA UTILIZANDO SIMULADORES QUÂNTICOS", size=12, bold=True, align="center", first_line_indent=0, line_pitch=15, space_after=4)
    doc.add_paragraph("EXPLORATION OF THE QAOA ALGORITHM FOR OPTIMIZATION IN SUPERVISED CLASSIFICATION MODELS USING QUANTUM SIMULATORS", size=12, bold=True, align="center", first_line_indent=0, line_pitch=15, space_after=10)

    doc.add_paragraph("Julio Coronetti Regino ¹, i,  Cainã Antunes ², ii", size=11, bold=True, align="left", first_line_indent=0, line_pitch=14, space_after=10)

    doc.add_paragraph("RESUMO", size=11, bold=True, align="left", first_line_indent=0, line_pitch=13, space_after=3)
    resumo_text = ("Este trabalho avalia a formulação de tarefas de classificação supervisionada binária como problemas de Otimização Binária Quadrática Irrestrita (QUBO) e sua resolução pelo algoritmo QAOA em simuladores quânticos. O conjunto de dados breast cancer da biblioteca scikit-learn foi padronizado por escore Z, reduzido via PCA e reescalado para [0, 1], particionado com estratificação em 70% para treino e 30% para teste (seed 42). O classificador linear discretizado em variáveis binárias com penalização de norma e exclusão mútua de sinal foi confrontado com o SVM clássico e com o classificador variacional (VQC). Em instâncias com 2 componentes principais, o QAOA alcançou 90,00% de acurácia de teste em 3,70 s, contra 100,00% do SVM (0,0009 s) e 83,33% do VQC (12,81 s). A avaliação de escalabilidade até 5 componentes comprovou a estabilidade preditiva do modelo QUBO (90,00% exato), delimitando a barreira computacional da simulação clássica pelo crescimento exponencial do tempo de execução do QAOA.")
    doc.add_paragraph(resumo_text, size=10.5, align="justify", first_line_indent=0, line_pitch=13.5, space_after=3)
    doc.add_paragraph("Palavras-chave: QAOA; QUBO; classificação supervisionada; aprendizado de máquina quântico; simuladores quânticos.", size=10.5, bold=False, align="left", first_line_indent=0, line_pitch=13.5, space_after=8)

    doc.add_paragraph("ABSTRACT", size=11, bold=True, align="left", first_line_indent=0, line_pitch=13, space_after=3)
    abstract_text = ("This study evaluates the formulation of binary supervised classification tasks as Quadratic Unconstrained Binary Optimization (QUBO) problems solved by the QAOA algorithm on quantum simulators. The breast cancer dataset was standardized, reduced via PCA, scaled to [0, 1], and partitioned with stratification into 70% training and 30% testing subsets. A discretized linear classifier with regularized binary weights and mutual sign exclusion was compared against classical SVM and simulated VQC baselines. For instances with 2 principal components, QAOA achieved 90.00% test accuracy in 3.70 s, compared to 100.00% for SVM (0.0009 s) and 83.33% for VQC (12.81 s). Scalability tests across 2 to 5 components confirmed the functional stability of the QUBO formulation while highlighting the computational bottleneck of classical state-vector simulation, which scales exponentially with the number of qubits.")
    doc.add_paragraph(abstract_text, size=10.5, align="justify", first_line_indent=0, line_pitch=13.5, space_after=3)
    doc.add_paragraph("Keywords: QAOA; QUBO; supervised classification; quantum machine learning; quantum simulators.", size=10.5, bold=False, align="left", first_line_indent=0, line_pitch=13.5, space_after=10)

    doc.add_heading_1("1 INTRODUÇÃO")
    doc.add_paragraph("A computação quântica baseada em circuitos variacionais híbridos tem sido investigada para explorar novos modelos de otimização no regime de processadores com ruído e conectividade limitada (era NISQ). Embora modelos tradicionais de aprendizado supervisionado operem em espaços contínuos por otimização convexa, a representação de tarefas de classificação sob formalismos combinatórios discretos viabiliza sua execução em computadores quânticos através de matrizes de interação quadrática. Contudo, em plataformas clássicas de simulação por vetores de estado, a emulação das operações quânticas impõe custo de memória e tempo exponencialmente proporcional ao número de qubits, exigindo a caracterização empírica de sua viabilidade técnica frente a métodos consolidados.", size=11, line_pitch=14.5, space_after=6)

    doc.add_paragraph("O objetivo deste trabalho é avaliar o desempenho do algoritmo QAOA (Quantum Approximate Optimization Algorithm) na resolução de problemas de classificação binária formulados como QUBO (Quadratic Unconstrained Binary Optimization), analisando a acurácia de generalização e o tempo computacional em simuladores quânticos. Especificamente, busca-se: 1) mapear a função de custo de um classificador linear discretizado para uma matriz QUBO com penalidades quadráticas; 2) contrastar as métricas de convergência do QAOA com o classificador SVM clássico e com o classificador quântico variacional (VQC); e 3) quantificar a escalabilidade temporal da abordagem frente ao incremento da dimensionalidade de entrada via componentes principais (PCA).", size=11, line_pitch=14.5, space_after=6)

    doc.add_paragraph("Essa abordagem fundamenta a investigação empírica do QAOA frente a baselines consolidados: postula-se que a formulação QUBO preserva a capacidade discriminativa em instâncias controladas, embora o custo de simulação clássica limite a profundidade e a dimensionalidade operacional perante algoritmos tradicionais.", size=11, line_pitch=14.5, space_after=10)

    doc.add_heading_1("2 REVISÃO DE LITERATURA")
    doc.add_paragraph("Algoritmos quânticos variacionais (VQAs) empregam circuitos parametrizados cuja energia esperada é avaliada em processadores quânticos e atualizada iterativamente por rotinas clássicas de otimização (Bharti et al., 2022; Cerezo et al., 2021). O algoritmo QAOA, formulado originalmente por Farhi, Goldstone e Gutmann (2014), alterna a aplicação de operadores Hamiltonianos de custo e de mistura para conduzir o estado inicial a uma configuração que aproxima o mínimo de uma função combinatorial. Em tarefas de classificação, o aprendizado quântico tradicional explora espaços de Hilbert através de mapas de características e ansätze variacionais (Havlíček et al., 2019; Schuld; Killoran, 2019). No entanto, a modelagem direta da perda de classificação como uma função quadrática binária viabiliza a aplicação de amostradores e solvers quânticos combinatórios (Grange; Poss; Bourreau, 2024).", size=11, line_pitch=14.5, space_after=6)

    doc.add_paragraph("O paradigma QUBO expressa problemas de otimização discreta como formas quadráticas sobre vetores binários, equivalendo à representação do modelo de Ising (Glover; Kochenberger; Du, 2019; Lucas, 2014). Mapeamentos de Support Vector Machines para QUBO permitem explorar o espaço de parâmetros por meio de relaxações discretas (Guddanti et al., 2024). Em simulações clássicas de circuitos quânticos, a compressão dimensional prévia via PCA é indispensável para conter o dimensionamento do registrador de qubits e evitar a degradação temporal das rotinas de otimização (Mancilla; Pere, 2022; Qi et al., 2025). A escolha de otimizadores clássicos como COBYLA e SPSA determina a eficiência da convergência sob diferentes superfícies de custo e perturbações de amostragem (AL Ajmi; Shoaib, 2025; Spall, 1992).", size=11, line_pitch=14.5, space_after=10)

    doc.add_heading_1("3 METODOLOGIA")
    doc.add_paragraph("O protocolo experimental foi implementado em Python utilizando as bibliotecas scikit-learn (v1.4) e Qiskit (Qiskit v1.0, Qiskit Algorithms e Qiskit Optimization). Empregou-se o conjunto de dados breast cancer, extraindo-se uma amostra estratificada de 100 instâncias particionada em 70% para treinamento e 30% para teste com semente pseudoaleatória controlada (random_state = 42). O fluxo de pré-processamento consistiu em padronização por escore Z (StandardScaler ajustado no treino), redução de dimensionalidade por PCA e normalização linear no intervalo [0, 1] com MinMaxScaler.", size=11, line_pitch=14.5, space_after=6)

    doc.add_paragraph("Para o baseline de referência, utilizou-se um SVM linear clássico e um modelo VQC composto pelo mapa de características ZZFeatureMap, ansatz variacional RealAmplitudes e otimizador SPSA com 100 iterações. Na formulação combinatória, o hiperplano de separação linear foi discretizado representando cada coeficiente w_j e o viés b por um par de variáveis binárias que codificam magnitudes positivas e negativas: c_k = s * (b_k^(+) - b_k^(-)), com escala s = 2,0 e 1 bit de resolução por sinal, totalizando n_bin = 2(d + 1) variáveis booleanas para d componentes PCA.", size=11, line_pitch=14.5, space_after=6)

    doc.add_paragraph("A função objetivo minimizada adotou o critério de erro quadrático de margem com termos de regularização e penalidade de exclusão mútua de sinal: H = (1 / N) * sum((b + sum(x_ij * w_j) - y_i)^2) + lambda_reg * sum(w_j^2) + lambda_mut * sum(b_k^(+) * b_k^(-)), onde y_i em {-1, +1} é o rótulo da classe, lambda_reg = 0,05 é a regularização L2 de pesos e lambda_mut = 0,25 é a penalidade que impede a ativação simultânea de bits de polaridade oposta do mesmo coeficiente. A matriz resultante foi solucionada pelo QAOA com uma repetição (p = 1), operador StatevectorSampler e otimizador COBYLA, contrastando-se com um solver exato por enumeração completa de 2^6 a 2^12 estados.", size=11, line_pitch=14.5, space_after=10)

    doc.add_heading_1("4 RESULTADOS E DISCUSSÕES")
    doc.add_paragraph("A Tabela 1 consolida os resultados dos baselines e da formulação combinatória para a instância com 2 componentes PCA (6 variáveis binárias). O SVM linear clássico alcançou acurácia de 100,00% em 0,0009 segundos, enquanto o VQC simulado obteve 83,33% em 12,8098 segundos. Tanto o solver exato quanto o QAOA convergiram para 90,00% de acurácia de teste, demonstrando que a discretização de parâmetros preserva a fronteira de decisão essencial, com o QAOA executando em 3,6997 segundos no simulador.", size=11, line_pitch=14.5, space_after=6)

    doc.add_table(
        "Tabela 1: Desempenho comparativo dos modelos no conjunto de teste (PCA = 2).",
        ["Modelo", "Paradigma", "Vars Binárias", "Acurácia", "Tempo (s)"],
        [["SVM linear", "Clássico", "-", "100,00%", "0,0009 s"],
         ["VQC simulado", "Quântico Variacional", "-", "83,33%", "12,8098 s"],
         ["QUBO Solver Exato", "Clássico Exaustivo", "6", "90,00%", "0,0824 s"],
         ["QAOA-QUBO linear", "Quântico Combinatório", "6", "90,00%", "3,6997 s"]],
        [130.0, 125.0, 75.0, 60.0, 63.0]
    )

    doc.add_paragraph("A Tabela 2 apresenta a escalabilidade computacional variando o número de componentes PCA de 2 a 5. O solver exato manteve acurácia invariante de 90,00% em todas as configurações, com tempo de busca escalando de 0,0824 s (6 variáveis, 64 estados) a 7,1497 s (12 variáveis, 4.096 estados). Em contrapartida, a emulação do QAOA apresentou acentuada sensibilidade dimensional: o tempo elevou-se para 41,7146 s em PCA = 3 (8 variáveis) e para 863,4231 s em PCA = 4 (10 variáveis, 1.024 estados quânticos), forçando a redução do COBYLA para 5 iterações para viabilizar a conclusão do experimento.", size=11, line_pitch=14.5, space_after=6)

    doc.add_table(
        "Tabela 2: Escalabilidade computacional da formulação QUBO sob variação de componentes PCA.",
        ["PCA", "Vars", "Espaço de Estados", "Solver Exato (Tempo / Ac.)", "QAOA Simulado (Tempo / Ac.)"],
        [["2", "6", "64 estados (2^6)", "0,0824 s  /  90,00%", "3,6997 s  /  90,00%"],
         ["3", "8", "256 estados (2^8)", "0,4580 s  /  90,00%", "41,7146 s  /  90,00%"],
         ["4", "10", "1.024 estados (2^10)", "1,2578 s  /  90,00%", "863,4231 s* / 96,67%"],
         ["5", "12", "4.096 estados (2^12)", "7,1497 s  /  90,00%", "-  (limite de simulação)"]],
        [35.0, 35.0, 115.0, 134.0, 134.0]
    )
    doc.add_paragraph("Nota: * Otimizador COBYLA limitado a 5 iterações por restrição de tempo de simulação.", size=8.5, italic=True, align="left", first_line_indent=0, line_pitch=11.0, space_after=8.0)

    doc.add_paragraph("Na instância com 4 componentes, o QAOA registrou acurácia nominal de 96,67% (29 acertos em 30 amostras), superando a taxa de 90,00% do solver exato. Esse desvio resulta da aproximação estocástica do QAOA sobre o conjunto de treino que, pela discretização em passos de 2,0, produziu um ligeiro deslocamento do limiar do hiperplano que coincidiu com a classificação correta de duas instâncias limítrofes na partição de teste reduzida (flutuação amostral). Os resultados confirmam a convergência funcional do modelo QUBO e evidenciam que o gargalo operacional reside na multiplicação matricial clássica exigida para emular processadores quânticos.", size=11, line_pitch=14.5, space_after=10)

    doc.add_heading_1("5 CONCLUSÃO")
    doc.add_paragraph("Este trabalho avaliou a transposição de modelos de classificação binária supervisionada para o paradigma combinatório QUBO resolvido por QAOA em simuladores quânticos. Os experimentos confirmaram a viabilidade funcional da formulação discreta, atingindo acurácia de 90,00% com 2 componentes PCA e mantendo a estabilidade preditiva no solver exato em todas as dimensões analisadas.", size=11, line_pitch=14.5, space_after=6)

    doc.add_paragraph("O confronto com o SVM clássico confirmou a hipótese norteadora: enquanto o classificador tradicional treina em milissegundos, o QAOA simulado enfrenta severa restrição de escalabilidade decorrente do custo exponencial de cálculo de vetores de estado em CPUs clássicas. Conclui-se que a formulação QUBO proposta preserva as propriedades discriminativas da classificação linear, mas sua aplicabilidade prática em problemas de maior escala dependerá da execução nativa em hardware quântico da era NISQ.", size=11, line_pitch=14.5, space_after=10)

    doc.add_heading_1("REFERÊNCIAS")
    refs = [
        "AL AJMI, N. A.; SHOAIB, M. Optimization Strategies in Quantum Machine Learning: A Performance Analysis. Applied Sciences, v. 15, n. 8, p. 4493, 2025.",
        "BHARTI, K. et al. Noisy intermediate-scale quantum algorithms. Reviews of Modern Physics, v. 94, n. 1, p. 015004, 2022.",
        "CEREZO, M. et al. Variational quantum algorithms. Nature Reviews Physics, v. 3, p. 625-644, 2021.",
        "FARHI, E.; GOLDSTONE, J.; GUTMANN, S. A Quantum Approximate Optimization Algorithm. arXiv:1411.4028, 2014.",
        "GLOVER, F.; KOCHENBERGER, G.; DU, Y. A Tutorial on Formulating and Using QUBO Models. arXiv:1811.11538, 2019.",
        "GRANGE, C.; POSS, M.; BOURREAU, E. An introduction to variational quantum algorithms for combinatorial optimization problems. Annals of Operations Research, v. 343, p. 847-884, 2024.",
        "GUDDANTI, S. S. et al. Pneumonia detection by binary classification: classical, quantum, and hybrid approaches for SVM. Frontiers in Computer Science, v. 5, 2024.",
        "HAVLÍČEK, V. et al. Supervised learning with quantum-enhanced feature spaces. Nature, v. 567, p. 209-212, 2019.",
        "LUCAS, A. Ising formulations of many NP problems. Frontiers in Physics, v. 2, p. 5, 2014.",
        "MANCILLA, J.; PERE, C. A Preprocessing Perspective for Quantum Machine Learning Classification Advantage Using NISQ Algorithms. Entropy, v. 24, p. 1656, 2022.",
        "QI, H. et al. A high-efficiency variational quantum classifier for high-dimensional data. Journal of Supercomputing, v. 81, p. 1-20, 2025.",
        "SCHULD, M.; KILLORAN, N. Quantum Machine Learning in Feature Hilbert Spaces. Physical Review Letters, v. 122, p. 040504, 2019.",
        "SPALL, J. C. Multivariate stochastic approximation using a simultaneous perturbation gradient approximation. IEEE Transactions on Automatic Control, v. 37, n. 3, p. 332-341, 1992."
    ]
    for r in refs:
        doc.add_paragraph(r, size=9.0, align="justify", first_line_indent=0, line_pitch=12.0, space_after=3.5)

    doc.add_heading_1("AGRADECIMENTOS")
    doc.add_paragraph("Agradece-se à Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior pelo suporte institucional e de infraestrutura concedido ao desenvolvimento desta pesquisa.", size=10.5, line_pitch=13.5, space_after=10)

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

    with open(CROPPED_LOGO_BIN, 'rb') as f:
        img_zlib = f.read()

    disp_img_w = 60.0
    disp_img_h = (CROP_H / CROP_W) * disp_img_w
    img_x = MARGIN_LEFT + PRINT_W - disp_img_w
    img_y = 18.0

    objects = []
    
    def add_obj(content):
        objects.append(content)
        return len(objects)

    objects.append(b"")
    objects.append(b"")
    
    f1_idx = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    f2_idx = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
    f3_idx = add_obj(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique /Encoding /WinAnsiEncoding >>")
    
    img_dict = f"<< /Type /XObject /Subtype /Image /Width {CROP_W} /Height {CROP_H} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode /Length {len(img_zlib)} >>\nstream\n".encode('latin1') + img_zlib + b"\nendstream"
    img_idx = add_obj(img_dict)

    page_obj_indices = []

    for p_num, p_stream in enumerate(doc.pages, start=1):
        decorations = []

        decorations.append("q")
        decorations.append("0.976 0.075 0.118 rg")
        decorations.append("482.55 841.89 m 595.28 841.89 l 595.28 770.99 l 523.45 770.99 l f")
        decorations.append("Q")

        decorations.append("BT /F2 10 Tf 0 0 0 rg 562.00 812.00 Td (" + str(p_num) + ") Tj ET")

        decorations.append("q")
        decorations.append("0.922 0.922 0.922 rg")
        decorations.append("0.00 0.00 m 595.28 0.00 l 595.28 50.00 l 0.00 40.00 l f")
        decorations.append("Q")

        decorations.append("q")
        decorations.append(f"{disp_img_w:.2f} 0 0 {disp_img_h:.2f} {img_x:.2f} {img_y:.2f} cm")
        decorations.append("/Im1 Do")
        decorations.append("Q")

        if p_num == 1:
            fn_y = PRINT_BOTTOM + 25.0
            decorations.append(f"0.5 w 0 0 0 RG {MARGIN_LEFT:.2f} {(fn_y + 16.0):.2f} m {(MARGIN_LEFT + 140.0):.2f} {(fn_y + 16.0):.2f} l S")
            fn1 = escape_pdf_str("¹ Discente, Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, julio.regino2@senaisp.edu.br.")
            decorations.append(f"BT /F1 8.5 Tf {MARGIN_LEFT:.2f} {(fn_y + 4.0):.2f} Td ({fn1}) Tj ET")
            fn2 = escape_pdf_str("² Docente, Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, caina.silva@sp.senai.br.")
            decorations.append(f"BT /F1 8.5 Tf {MARGIN_LEFT:.2f} {(fn_y - 8.0):.2f} Td ({fn2}) Tj ET")

        full_stream_text = "\n".join(decorations + p_stream)
        compressed_stream = zlib.compress(full_stream_text.encode('latin1'))

        stream_obj = f"<< /Length {len(compressed_stream)} /Filter /FlateDecode >>\nstream\n".encode('latin1') + compressed_stream + b"\nendstream"
        stream_idx = add_obj(stream_obj)

        page_dict = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] "
            f"/Resources << /Font << /F1 {f1_idx} 0 R /F2 {f2_idx} 0 R /F3 {f3_idx} 0 R >> "
            f"/XObject << /Im1 {img_idx} 0 R >> >> "
            f"/Contents {stream_idx} 0 R >>"
        ).encode('latin1')
        page_idx = add_obj(page_dict)
        page_obj_indices.append(page_idx)

    catalog_obj = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects[0] = catalog_obj

    kids_str = " ".join(f"{idx} 0 R" for idx in page_obj_indices)
    pages_obj = f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_obj_indices)} >>".encode('latin1')
    objects[1] = pages_obj

    with open(OUTPUT_PDF, 'wb') as f:
        f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = []
        for idx, obj in enumerate(objects, start=1):
            offsets.append(f.tell())
            f.write(f"{idx} 0 obj\n".encode('latin1'))
            f.write(obj)
            f.write(b"\nendobj\n")

        xref_start = f.tell()
        f.write(b"xref\n")
        f.write(f"0 {len(objects) + 1}\n".encode('latin1'))
        f.write(b"0000000000 65535 f \n")
        for off in offsets:
            f.write(f"{off:010d} 00000 n \n".encode('latin1'))

        f.write(b"trailer\n")
        f.write(f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode('latin1'))
        f.write(b"startxref\n")
        f.write(f"{xref_start}\n".encode('latin1'))
        f.write(b"%%EOF\n")

    print(f"Sucesso! PDF compilado em: {OUTPUT_PDF} com {len(doc.pages)} páginas.")

if __name__ == '__main__':
    build_pdf()
