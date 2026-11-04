import zlib
import struct
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PDF = str(BASE_DIR / "dist" / "Resumo_Expandido_Julio_Regino_2026.pdf")
DIST_PDF = str(BASE_DIR / "revisao" / "Resumo_Expandido_Julio_Regino_2026_Revisado.pdf")
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
    text = (text.replace('č', 'c').replace('Č', 'C').replace('ě', 'e').replace('Ě', 'E')
                .replace('∑', 'sum').replace('∈', 'in').replace('·', '*').replace('⁶', '^6')
                .replace('⁸', '^8').replace('¹²', '^12').replace('¹⁰', '^10').replace('λ', 'lambda'))
    table = HELVETICA_BOLD_WIDTHS if bold else HELVETICA_WIDTHS
    w = sum(table.get(c, 556) for c in text)
    return (w / 1000.0) * font_size

def escape_pdf_str(text):
    text = (text.replace('č', 'c').replace('Č', 'C').replace('ě', 'e').replace('Ě', 'E')
                .replace('∑', 'sum').replace('∈', 'in').replace('·', '*').replace('⁶', '^6')
                .replace('⁸', '^8').replace('¹²', '^12').replace('¹⁰', '^10').replace('λ', 'lambda'))
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
        bot = 75.0 if self.page_number == 1 else PRINT_BOTTOM
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

    def add_heading_1(self, text, keep_with_next_lines=3, space_before=12.0, space_after=6.0):
        sb = 0.0 if self.current_y >= PRINT_TOP - 1.0 else space_before
        needed = sb + 14.0 + (keep_with_next_lines * 13.0) + space_after
        self.check_space(needed)
        sb = 0.0 if self.current_y >= PRINT_TOP - 1.0 else space_before
        self.current_y -= sb
        self.draw_text(text, MARGIN_LEFT, self.current_y, font="F2", size=11.0, bold=True)
        self.current_y -= (13.0 + space_after)

    def add_equation_box(self, eq_text, space_before=8.0, space_after=8.0):
        self.check_space(space_before + 20.0 + space_after)
        self.current_y -= space_before
        w = string_width(eq_text, 9.5, bold=False)
        cx = MARGIN_LEFT + (PRINT_W - w) / 2.0
        self.draw_text(eq_text, cx, self.current_y, font="F3", size=9.5, italic=True)
        self.current_y -= (13.0 + space_after)

    def add_table(self, caption, headers, rows, col_widths, space_before=8.0, space_after=6.0):
        needed = space_before + 28.0 + len(rows) * 13.5 + space_after
        self.check_space(needed)
        self.current_y -= space_before
        self.draw_text(caption, MARGIN_LEFT, self.current_y, font="F2", size=8.5, bold=True)
        self.current_y -= 12.0

        tbl_w = sum(col_widths)
        x_start = MARGIN_LEFT + (PRINT_W - tbl_w) / 2.0

        y_top = self.current_y + 3.0
        self.add_command(f"0.8 w 0 0 0 RG {x_start:.2f} {y_top:.2f} m {(x_start + tbl_w):.2f} {y_top:.2f} l S")

        x_curr = x_start
        for idx, h in enumerate(headers):
            hw = string_width(h, 8.0, bold=True)
            hx = x_curr + (col_widths[idx] - hw) / 2.0
            self.draw_text(h, hx, self.current_y - 6.5, font="F2", size=8.0, bold=True)
            x_curr += col_widths[idx]
        self.current_y -= 12.0

        y_hbot = self.current_y + 2.0
        self.add_command(f"0.5 w 0 0 0 RG {x_start:.2f} {y_hbot:.2f} m {(x_start + tbl_w):.2f} {y_hbot:.2f} l S")

        for r in rows:
            x_curr = x_start
            for idx, c in enumerate(r):
                cw = string_width(c, 7.5, bold=False)
                cx = x_curr + 4.0 if (idx == 0 and len(c) > 4) else x_curr + (col_widths[idx] - cw) / 2.0
                self.draw_text(c, cx, self.current_y - 6.5, font="F1", size=7.5, bold=False)
                x_curr += col_widths[idx]
            self.current_y -= 12.0

        y_bot = self.current_y + 2.0
        self.add_command(f"0.8 w 0 0 0 RG {x_start:.2f} {y_bot:.2f} m {(x_start + tbl_w):.2f} {y_bot:.2f} l S")
        self.current_y -= space_after

    def add_author_bio(self, num_str, name, bio):
        self.check_space(45.0)
        self.draw_text(f"{num_str} {name}", MARGIN_LEFT, self.current_y, font="F2", size=9.5, bold=True)
        self.current_y -= 12.0
        self.add_paragraph(bio, size=8.5, align="justify", first_line_indent=0, line_pitch=11.2, space_after=5.0)

    def finalize(self):
        if self.current_page_stream:
            self.pages.append(self.current_page_stream)

def build_pdf():
    print("Iniciando compilação do Resumo Expandido Revisado (5 páginas)...")
    doc = PDFDoc()

    # Cabeçalho da Página 1
    doc.add_paragraph("EXPLORAÇÃO DO ALGORITMO QAOA PARA OTIMIZAÇÃO EM MODELOS DE CLASSIFICAÇÃO SUPERVISIONADA UTILIZANDO SIMULADORES QUÂNTICOS", size=11.5, bold=True, align="center", first_line_indent=0, line_pitch=14.5, space_after=3)
    doc.add_paragraph("EXPLORATION OF THE QAOA ALGORITHM FOR OPTIMIZATION IN SUPERVISED CLASSIFICATION MODELS USING QUANTUM SIMULATORS", size=11.5, bold=True, align="center", first_line_indent=0, line_pitch=14.5, space_after=8)

    doc.add_paragraph("Julio Coronetti Regino ¹, i,  Cainã Antunes ², ii", size=10.5, bold=True, align="left", first_line_indent=0, line_pitch=13.5, space_after=8)

    # Resumo em Português
    doc.add_paragraph("RESUMO", size=10.5, bold=True, align="left", first_line_indent=0, line_pitch=13, space_after=2)
    resumo_text = (
        "Este trabalho investiga a formulação da classificação supervisionada binária como um problema de Otimização Binária "
        "Quadrática Irrestrita (QUBO), resolvido via algoritmo QAOA em simuladores quânticos analíticos de vetores de estado. "
        "A partir de uma subamostra estratificada de 100 instâncias (37 da classe maligna e 63 da benigna) do conjunto breast cancer "
        "(scikit-learn), particionada em 70% para treino e 30% para teste, avaliou-se um classificador linear com pesos discretizados "
        "frente ao SVM linear clássico e ao classificador quântico variacional (VQC). Para prevenir rigorosamente qualquer vazamento "
        "de dados (data leakage), a padronização por escore Z, a Análise de Componentes Principais (PCA) e a normalização linear em "
        "[0, 1] foram ajustadas exclusivamente na partição de treinamento e aplicadas no teste. Enquanto o VQC treina as rotações "
        "de portas lógicas em um circuito quântico classificador, o QAOA otimiza os coeficientes discretizados de uma função de perda "
        "clássica mapeada para QUBO. Com 2 componentes PCA, tanto o solver exato quanto o QAOA convergiram para o mesmo valor ótimo "
        "de função objetivo (0,8736) no treino e registraram 90,00% de acurácia observada no teste (QAOA em 3,70 s, SVM em 0,0010 s e "
        "VQC em 12,81 s). A avaliação de escalabilidade abrangeu o QAOA de 2 a 4 componentes e o solver exato de 2 a 5 componentes. "
        "O QAOA manteve o custo ótimo em PCA = 3 (0,8736; 90,00%; 41,71 s) e obteve 96,67% em PCA = 4 (863,42 s) sobre uma solução "
        "subótima no treino (0,8764), cuja oscilação constitui hipótese de flutuação amostral decorrente da partição de teste reduzida. "
        "O solver exato alcançou 90,00% em PCA = 5 (7,15 s; 12 variáveis), confirmando a viabilidade representacional da modelagem "
        "e delimitando o gargalo de tempo na simulação clássica de amplitudes quânticas."
    )
    doc.add_paragraph(resumo_text, size=10.0, align="justify", first_line_indent=0, line_pitch=13.0, space_after=3)
    doc.add_paragraph("Palavras-chave: QAOA; QUBO; classificação supervisionada; aprendizado de máquina quântico; simuladores quânticos.", size=10.0, bold=False, align="left", first_line_indent=0, line_pitch=13.0, space_after=6)

    # Abstract em Inglês
    doc.add_paragraph("ABSTRACT", size=10.5, bold=True, align="left", first_line_indent=0, line_pitch=13, space_after=2)
    abstract_text = (
        "This study investigates the formulation of binary supervised classification as a Quadratic Unconstrained Binary "
        "Optimization (QUBO) problem solved by the QAOA algorithm on quantum statevector simulators. Using a stratified subset of "
        "100 instances (37 malignant, 63 benign) from the breast cancer dataset, partitioned into 70% training and 30% testing subsets, "
        "a discretized linear classifier was evaluated against classical linear SVM and simulated Variational Quantum Classifier "
        "(VQC) baselines. To strictly prevent data leakage, Z-score standardization, Principal Component Analysis (PCA), and [0, 1] "
        "min-max normalization were fitted exclusively on the training partition and applied to the test partition. While VQC adjusts "
        "parameterized gate rotations in a quantum circuit, QAOA optimizes the discretized coefficients of a classical quadratic loss "
        "mapped to QUBO. With 2 PCA components, both the exact solver and QAOA converged to the optimal objective function value (0.8736) "
        "on training, achieving 90.00% observed test accuracy (QAOA in 3.70 s, SVM in 0.0010 s, and VQC in 12.81 s). Scalability evaluation "
        "assessed QAOA from 2 to 4 components and the exact solver from 2 to 5 components. QAOA retained the optimal cost at PCA = 3 "
        "(0.8736; 90.00%; 41.71 s) and yielded 96.67% at PCA = 4 (863.42 s) with a suboptimal training cost (0.8764), hypothesized as "
        "a sample fluctuation on the small test partition. The exact solver reached 90.00% at PCA = 5 (7.15 s; 12 variables), demonstrating "
        "representational viability while highlighting the exponential runtime bottleneck of classical statevector simulation."
    )
    doc.add_paragraph(abstract_text, size=10.0, align="justify", first_line_indent=0, line_pitch=13.0, space_after=3)
    doc.add_paragraph("Keywords: QAOA; QUBO; supervised classification; quantum machine learning; quantum simulators.", size=10.0, bold=False, align="left", first_line_indent=0, line_pitch=13.0, space_after=8)

    # 1 INTRODUÇÃO
    doc.add_heading_1("1 INTRODUÇÃO")
    doc.add_paragraph(
        "A computação quântica baseada em circuitos variacionais híbridos tem sido amplamente investigada para explorar novos paradigmas "
        "de otimização sob as restrições da era NISQ (Noisy Intermediate-Scale Quantum), caracterizada por conectividade limitada e presença "
        "de ruído (Bharti et al., 2022). Embora o aprendizado supervisionado convencional opere tradicionalmente em espaços contínuos por "
        "meio de otimização convexa, a representação de tarefas de classificação sob formalismos combinatórios discretos viabiliza sua "
        "resolução em arquiteturas quânticas através de matrizes de interação quadrática (Grange; Poss; Bourreau, 2024).",
        size=10.0, line_pitch=13.0, space_after=4.5
    )
    doc.add_paragraph(
        "Nesse contexto, cabe distinguir duas vertentes fundamentais do aprendizado de máquina quântico: enquanto classificadores "
        "quânticos variacionais (VQC) ajustam os parâmetros contínuos de rotação de um circuito quântico classificador atuando sobre "
        "espaços de Hilbert (Havlíček et al., 2019; Schuld; Killoran, 2019), a abordagem baseada no algoritmo QAOA (Quantum Approximate "
        "Optimization Algorithm) utiliza circuitos quânticos parametrizados para encontrar as configurações binárias que minimizam uma "
        "função de custo combinatória mapeada para QUBO (Quadratic Unconstrained Binary Optimization) (Farhi; Goldstone; Gutmann, 2014; "
        "Glover; Kochenberger; Du, 2019). Em simuladores clássicos por vetores de estado, contudo, a representação exata de 2^n amplitudes "
        "impõe um crescimento exponencial no tempo de processamento conforme o registrador de qubits se expande, exigindo a caracterização "
        "empírica de sua escalabilidade perante métodos consolidados.",
        size=10.0, line_pitch=13.0, space_after=4.5
    )
    doc.add_paragraph(
        "O objetivo deste estudo é avaliar o desempenho do algoritmo QAOA na resolução de tarefas de classificação binária formuladas "
        "como QUBO, analisando a acurácia de generalização observada e o tempo computacional em simuladores quânticos frente ao SVM linear "
        "clássico e ao VQC simulado. O escopo compreende: 1) mapear a perda de um classificador linear discretizado para uma matriz QUBO com "
        "penalidades quadráticas; 2) verificar o impacto da prevenção rigorosa de vazamento de dados (data leakage) no fluxo de "
        "pré-processamento via Análise de Componentes Principais (PCA, do inglês Principal Component Analysis); 3) comparar o desempenho "
        "observado e os valores de custo atingidos pelo QAOA e por um solver combinatorial exato; e 4) delimitar a escalabilidade da "
        "simulação clássica, avaliando o QAOA em instâncias de 2 a 4 componentes PCA e o solver exato até 5 componentes.",
        size=10.0, line_pitch=13.0, space_after=4.5
    )

    # 2 REVISÃO DE LITERATURA
    doc.add_heading_1("2 REVISÃO DE LITERATURA")
    doc.add_paragraph(
        "Algoritmos quânticos variacionais (VQAs) utilizam circuitos parametrizados cuja energia esperada é mensurada e otimizada "
        "iterativamente por rotinas clássicas (Cerezo et al., 2021). O algoritmo QAOA, proposto por Farhi, Goldstone e Gutmann (2014), "
        "alterna operadores Hamiltonianos de custo e de mistura para guiar o estado quântico em direção à solução ótima de problemas "
        "combinatórios discretos. Em classificação, o paradigma dominante explora mapas de características quânticos (Havlíček et al., "
        "2019; Schuld; Killoran, 2019). Todavia, a modelagem de fronteiras de decisão como problemas quadráticos irrestritos viabiliza o "
        "emprego direto de otimizadores combinatórios quânticos (Grange; Poss; Bourreau, 2024).",
        size=10.0, line_pitch=13.0, space_after=4.5
    )
    doc.add_paragraph(
        "O formalismo QUBO mapeia problemas de otimização combinatória sobre vetores booleanos, mantendo equivalência direta com o modelo "
        "físico de Ising (Glover; Kochenberger; Du, 2019; Lucas, 2014). Mapeamentos de classificadores do tipo Support Vector Machine para "
        "QUBO permitem explorar o espaço discreto de parâmetros (Guddanti et al., 2024). Em plataformas clássicas de simulação quântica, a "
        "redução prévia de dimensionalidade por PCA é indispensável para conter a dimensão do registrador de qubits e viabilizar a "
        "convergência das rotinas de otimização (Mancilla; Pere, 2022; Qi et al., 2025). Ademais, a seleção e a tolerância de otimizadores "
        "clássicos como COBYLA e SPSA governam a estabilidade da convergência em circuitos variacionais (AL Ajmi; Shoaib, 2025; Spall, 1992).",
        size=10.0, line_pitch=13.0, space_after=4.5
    )

    # 3 METODOLOGIA
    doc.add_heading_1("3 METODOLOGIA")
    doc.add_paragraph(
        "O protocolo experimental utilizou o conjunto de dados breast cancer da biblioteca scikit-learn (569 instâncias, 30 atributos). "
        "Extraiu-se uma subamostra estratificada de 100 instâncias, preservando a proporção de 37 amostras da classe 0 (maligno) e 63 da "
        "classe 1 (benigno). Essa amostra foi particionada com estratificação em 70% para treinamento (N = 70: 26 classe 0 e 44 classe 1) "
        "e 30% para teste (30 instâncias: 11 classe 0 e 19 classe 1), fixando a semente pseudoaleatória controlada (random_state = 42). "
        "Para evitar estritamente qualquer vazamento de dados (data leakage), o fluxo de pré-processamento foi ajustado exclusivamente "
        "no conjunto de treino: a padronização por escore Z (StandardScaler), a redução dimensional por PCA e o reescalonamento no "
        "intervalo [0, 1] (MinMaxScaler) foram calibrados no treino e subsequentemente aplicados à partição de teste.",
        size=10.0, line_pitch=13.2, space_after=6.0
    )
    doc.add_paragraph(
        "Na formulação combinatória, o hiperplano de separação linear foi discretizado representando cada coeficiente de peso w_j "
        "(j in {1, ..., d}) e o viés b por variáveis binárias booleanas que codificam magnitudes positivas e negativas: "
        "w_j = s * (b_j^(+) - b_j^(-)) e b = s * (b_0^(+) - b_0^(-)), onde b_k^(+), b_k^(-) in {0, 1}, com escala s = 2,0 e 1 bit por sinal, "
        "totalizando n_bin = 2(d + 1) variáveis binárias para d componentes PCA. A função objetivo minimizada adotou o critério de erro quadrático de "
        "margem com penalização L2 e exclusão mútua de polaridade, conforme apresentado na Equação (1):",
        size=10.0, line_pitch=13.2, space_after=6.0
    )

    doc.add_equation_box(
        "H(b, w) = (1/N) * sum_{i=1}^N (b + sum_{j=1}^d x_{ij} w_j - y_i)^2 + lambda_reg * (b^2 + sum_{j=1}^d w_j^2) + lambda_mut * sum_{k=0}^d b_k^(+) b_k^(-)   (1)",
        space_after=6.0
    )

    doc.add_paragraph(
        "onde N = 70 é o número de amostras de treino, y_i in {-1, +1} denota o rótulo de classe, lambda_reg = 0,05 é a regularização L2 aplicada a todos "
        "os coeficientes (incluindo o intercepto) e lambda_mut = 0,25 penaliza a ativação concorrente de bits opostos do mesmo coeficiente. A classe prevista "
        "para uma amostra de teste é obtida pelo sinal do score linear: y_hat = 1 se (b + sum_{j=1}^d x_{ij} w_j) >= 0,0, e y_hat = 0 caso contrário, "
        "mapeando formalmente o limiar zero para a classe 1.",
        size=10.0, line_pitch=13.2, space_after=6.0
    )
    doc.add_paragraph(
        "O protocolo computacional foi executado em ambiente Linux x86_64 dual-core (2 vCPUs @ 2,8 GHz, 8 GB RAM) sob Python 3.10+, "
        "empregando scikit-learn v1.4, qiskit v1.0, qiskit-algorithms v0.3.0, qiskit-optimization v0.6.1 e qiskit-machine-learning v0.7.2. "
        "O classificador clássico utilizou SVC(kernel='linear', C=1.0). O modelo VQC simulado adotou ZZFeatureMap(reps=1), ansatz "
        "RealAmplitudes(reps=1) (profundidade total de 6 camadas lógicas) e otimizador SPSA (maxiter=100, inicialização em 0,1, semente 42). "
        "O QAOA foi configurado com 1 camada (p = 1), ponto inicial dos ângulos (gamma, beta) fixado em 0,1, e simulador analítico "
        "StatevectorSampler(seed=42) operando no regime ideal exato (sem ruído e shots analíticos). O otimizador clássico COBYLA foi configurado "
        "com os limites: 20 iterações em PCA = 2, 20 iterações em PCA = 3 e 5 iterações em PCA = 4; a instância com PCA = 5 não foi submetida "
        "ao QAOA devido à projeção temporal. A solução binária retornada pelo QAOA é selecionada pelo MinimumEigenOptimizer, que extrai o "
        "autoestado de menor energia da função objetivo. Cada configuração empírica foi avaliada em uma única execução experimental (N = 1); "
        "os tempos reportados medem exclusivamente o processo de otimização/treinamento e inferência.",
        size=10.0, line_pitch=13.2, space_after=6.0
    )

    # 4 RESULTADOS E DISCUSSÕES
    doc.start_new_page()
    doc.add_heading_1("4 RESULTADOS E DISCUSSÕES")
    doc.add_paragraph(
        "A Tabela 1 apresenta o desempenho dos baselines e da formulação combinatória na partição de teste para a configuração com 2 componentes "
        "PCA (6 variáveis binárias). O SVM linear clássico obteve 100,00% de acurácia em 0,0010 s, enquanto o VQC simulado atingiu 83,33% em "
        "12,8098 s. Tanto o solver exato por busca exaustiva quanto o QAOA convergiram rigorosamente para o mesmo valor ótimo da função objetivo "
        "no treino (f_val = 0,8736) e atingiram 90,00% de acurácia observada no teste, comprovando que a discretização proposta preserva a "
        "capacidade discriminativa essencial do modelo linear, com o QAOA concluindo a otimização em 3,6997 s.",
        size=10.0, line_pitch=13.2, space_after=6.0
    )

    doc.add_table(
        "Tabela 1: Desempenho comparativo dos modelos no conjunto de teste (PCA = 2, N = 1).",
        ["Modelo", "Paradigma", "Vars", "f_val Treino", "Acurácia Teste", "Tempo (s)"],
        [["SVM linear", "Clássico", "-", "-", "100,00%", "0,0010 s"],
         ["VQC simulado", "Quântico Variacional", "-", "-", "83,33%", "12,8098 s"],
         ["QUBO Solver Exato", "Clássico Exaustivo", "6", "0,8736", "90,00%", "0,0824 s"],
         ["QAOA-QUBO linear", "Quântico Combinatório", "6", "0,8736", "90,00%", "3,6997 s"]],
        [110.0, 110.0, 40.0, 65.0, 70.0, 58.0],
        space_after=5.0
    )

    doc.add_paragraph(
        "A Tabela 2 consolida a escalabilidade computacional variando os componentes PCA de 2 a 5. O solver exato manteve o valor ótimo da "
        "função objetivo (f_val = 0,8736) e acurácia observada constante de 90,00% em todas as instâncias, com o tempo escalando de 0,0824 s "
        "(6 variáveis, 64 estados) até 7,1497 s (12 variáveis, 4.096 estados). No solver exato, a manutenção de f_val = 0,8736 de 2 a 5 componentes "
        "decorre da resolução discreta adotada (w_j in {-2, 0, +2}) sob regularização L2, na qual o ótimo global atribui peso zero aos componentes "
        "adicionais de menor variância. O QAOA simulado acompanhou o ótimo global em PCA = 2 e PCA = 3 (8 variáveis, 256 estados), alcançando "
        "f_val = 0,8736 e 90,00% de acurácia em 41,7146 s. Para PCA = 4 (10 variáveis, 1.024 estados), a restrição a 5 iterações do COBYLA levou a um "
        "tempo de 863,4231 s (~14,4 min) e resultou em uma solução subótima no treino (f_val = 0,8764 contra 0,8736 do exato). A configuração com 5 "
        "componentes não foi executada via QAOA devido ao limite de tempo imposto pelo ambiente.",
        size=10.0, line_pitch=13.2, space_after=6.0
    )

    doc.add_table(
        "Tabela 2: Escalabilidade computacional da formulação QUBO sob variação de componentes PCA.",
        ["PCA", "Vars", "Espaço (2^n)", "Solver Exato (Tempo / f_val / Ac.)", "QAOA Simulado (Tempo / f_val / Ac.)"],
        [["2", "6", "64 estados (2^6)", "0,0824 s  /  0,8736  /  90,00%", "3,6997 s  /  0,8736  /  90,00%"],
         ["3", "8", "256 estados (2^8)", "0,4580 s  /  0,8736  /  90,00%", "41,7146 s  /  0,8736  /  90,00%"],
         ["4", "10", "1.024 estados (2^10)", "1,2578 s  /  0,8736  /  90,00%", "863,4231 s* / 0,8764 / 96,67%"],
         ["5", "12", "4.096 estados (2^12)", "7,1497 s  /  0,8736  /  90,00%", "Não executado (limite de recurso)"]],
        [30.0, 32.0, 105.0, 143.0, 143.0],
        space_after=6.0
    )
    doc.add_paragraph("Nota: * COBYLA limitado a 5 iterações; tempos reportados para uma única execução (N = 1).", size=8.0, italic=True, align="left", first_line_indent=0, line_pitch=10.0, space_after=5.0)

    doc.add_paragraph(
        "Na instância com 4 componentes, o QAOA registrou acurácia nominal de 96,67% (29 acertos em 30 amostras), superando a taxa de 90,00% "
        "obtida pela solução matematicamente ótima do solver exato. Atribui-se essa elevação pontual à hipótese de flutuação amostral decorrente "
        "da partição de teste reduzida (30 instâncias): ao interromper a busca em uma solução ligeiramente subótima no treino (f_val = 0,8764), o "
        "deslocamento marginal do hiperplano classificou corretamente duas instâncias limítrofes adicionais. Os dados evidenciam a adequação da "
        "modelagem QUBO e demonstram que o custo de simulação clássica de vetores de estado em 2^n amplitudes constitui o fator limitante para a "
        "expansão do QAOA a dimensões superiores em computadores tradicionais.",
        size=10.0, line_pitch=13.2, space_after=6.0
    )

    # 5 CONCLUSÃO
    doc.start_new_page()
    doc.add_heading_1("5 CONCLUSÃO")
    doc.add_paragraph(
        "Este trabalho avaliou a modelagem de tarefas de classificação supervisionada binária no paradigma combinatório QUBO resolvidas por "
        "QAOA em simuladores quânticos analíticos. Os resultados observados confirmaram a viabilidade da discretização de hiperplanos lineares, "
        "alcançando o mesmo valor ótimo de função objetivo (0,8736) e 90,00% de acurácia em instâncias de 2 e 3 componentes PCA, com o solver "
        "exato assegurando a estabilidade da formulação até 5 componentes.",
        size=10.0, line_pitch=13.2, space_after=6.0
    )
    doc.add_paragraph(
        "A investigação empírica caracterizou os limites operacionais da abordagem: o QAOA foi avaliado de 2 a 4 componentes, "
        "registrando aumento substancial de tempo de 3,70 s para 863,42 s, enquanto a dimensão com 5 componentes foi restrita ao solver exato. "
        "Conclui-se que a formulação QUBO representa fielmente tarefas de classificação linear sem vazamento de dados, mas o escalonamento "
        "prático do QAOA em instâncias maiores dependerá de execuções em processadores quânticos físicos ou do emprego de simuladores por "
        "tensores e amostragem aproximada em trabalhos futuros.",
        size=10.0, line_pitch=13.2, space_after=6.0
    )

    # REFERÊNCIAS
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
        doc.add_paragraph(r, size=8.0, align="justify", first_line_indent=0, line_pitch=10.5, space_after=2.0)

    # AGRADECIMENTOS
    doc.add_heading_1("AGRADECIMENTOS", space_before=7.0, space_after=3.0)
    doc.add_paragraph(
        "Agradece-se à Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior pelo suporte institucional e de infraestrutura concedido ao desenvolvimento desta pesquisa.",
        size=9.5, line_pitch=12.0, space_after=6.0
    )

    # SOBRE OS AUTORES
    doc.add_heading_1("SOBRE O(S) AUTOR(ES)", space_before=7.0, space_after=3.0)
    doc.add_author_bio(
        "i", "Julio Coronetti Regino (Autor)",
        "Discente do curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas na Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior. Desenvolve pesquisa de Iniciação Científica focada em algoritmos variacionais quânticos (QAOA, VQC) e otimização combinatória (QUBO) aplicados a machine learning. E-mail: julio.regino2@senaisp.edu.br."
    )
    doc.add_author_bio(
        "ii", "Cainã Antunes (Orientador)",
        "Docente e pesquisador na Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, atuando como orientador de projetos de iniciação científica e desenvolvimento tecnológico em inteligência artificial e computação avançada. E-mail: caina.silva@sp.senai.br."
    )

    doc.finalize()

    print(f"Total de páginas geradas: {len(doc.pages)}")

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
        # Cunha vermelha UniSENAI
        decorations.append(f"q 0.976 0.075 0.118 rg {PAGE_W - 56.70:.2f} {PAGE_H:.2f} m {PAGE_W:.2f} {PAGE_H:.2f} l {PAGE_W:.2f} {PAGE_H - 56.70:.2f} l f Q\n")
        # Faixa cinza UniSENAI
        decorations.append(f"q 0.922 0.922 0.922 rg 0 0 m {PAGE_W:.2f} 0 l {PAGE_W:.2f} 42.52 l 0 42.52 l f Q\n")
        # Número da página
        p_str = escape_pdf_str(str(p_num))
        decorations.append(f"BT /F1 10 Tf {MARGIN_LEFT:.2f} 22.00 Td ({p_str}) Tj ET\n")
        # Logo SENAI
        decorations.append(f"q {disp_img_w:.2f} 0 0 {disp_img_h:.2f} {img_x:.2f} {img_y:.2f} cm /Im1 Do Q\n")

        # Rodapé na página 1 (notas de rodapé institucionais)
        if p_num == 1:
            fn1 = escape_pdf_str("¹ Discente, Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, julio.regino2@senaisp.edu.br.")
            fn2 = escape_pdf_str("² Docente, Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior, caina.silva@sp.senai.br.")
            decorations.append(f"BT /F1 8.5 Tf {MARGIN_LEFT:.2f} 60.00 Td ({fn1}) Tj ET\n")
            decorations.append(f"BT /F1 8.5 Tf {MARGIN_LEFT:.2f} 48.00 Td ({fn2}) Tj ET\n")

        stream_body = "".join(decorations) + "\n".join(p_stream)
        stream_bytes = stream_body.encode('latin1')
        comp_stream = zlib.compress(stream_bytes)

        stream_obj = f"<< /Length {len(comp_stream)} /Filter /FlateDecode >>\nstream\n".encode('latin1') + comp_stream + b"\nendstream"
        s_idx = add_obj(stream_obj)

        page_dict = f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W:.2f} {PAGE_H:.2f}] /Resources << /Font << /F1 {f1_idx} 0 R /F2 {f2_idx} 0 R /F3 {f3_idx} 0 R >> /XObject << /Im1 {img_idx} 0 R >> >> /Contents {s_idx} 0 R >>"
        p_idx = add_obj(page_dict.encode('latin1'))
        page_obj_indices.append(p_idx)

    kids_str = " ".join(f"{idx} 0 R" for idx in page_obj_indices)
    pages_obj = f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_obj_indices)} >>"
    objects[1] = pages_obj.encode('latin1')

    catalog_obj = b"<< /Type /Catalog /Pages 2 0 R >>"
    objects[0] = catalog_obj

    pdf_parts = [b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"]
    xref_offsets = [0]
    curr_offset = len(pdf_parts[0])

    for i, obj in enumerate(objects, start=1):
        xref_offsets.append(curr_offset)
        header = f"{i} 0 obj\n".encode('latin1')
        footer = b"\nendobj\n"
        pdf_parts.extend([header, obj, footer])
        curr_offset += len(header) + len(obj) + len(footer)

    xref_start = curr_offset
    xref_header = f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n"
    pdf_parts.append(xref_header.encode('latin1'))

    for off in xref_offsets[1:]:
        pdf_parts.append(f"{off:010d} 00000 n \n".encode('latin1'))

    trailer = f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n"
    pdf_parts.append(trailer.encode('latin1'))

    final_pdf_bytes = b"".join(pdf_parts)

    for out_path in [OUTPUT_PDF, DIST_PDF]:
        with open(out_path, 'wb') as f:
            f.write(final_pdf_bytes)
        print(f"Sucesso! PDF compilado em: {out_path} ({len(doc.pages)} páginas)")

if __name__ == '__main__':
    build_pdf()
