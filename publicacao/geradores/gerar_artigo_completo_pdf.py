import zlib
import struct
import os

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_PDF = str(BASE_DIR / "dist" / "IC_Julio_Versao_Completa_2026.pdf")
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
                .replace('∑', 'sum').replace('∈', 'in').replace('·', '*').replace('₆', '_6')
                .replace('⁸', '^8').replace('¹²', '^12').replace('¹⁰', '^10').replace('²', '^2')
                .replace('₁', '_1').replace('ᵢ', '_i').replace('ⱼ', '_j').replace('ₖ', '_k')
                .replace('λ', 'lambda'))
    table = HELVETICA_BOLD_WIDTHS if bold else HELVETICA_WIDTHS
    w = sum(table.get(c, 556) for c in text)
    return (w / 1000.0) * font_size

def escape_pdf_str(text):
    text = (text.replace('č', 'c').replace('Č', 'C').replace('ě', 'e').replace('Ě', 'E')
                .replace('∑', 'sum').replace('∈', 'in').replace('·', '*').replace('₆', '_6')
                .replace('⁸', '^8').replace('¹²', '^12').replace('¹⁰', '^10')
                .replace('₁', '_1').replace('ᵢ', '_i').replace('ⱼ', '_j').replace('ₖ', '_k')
                .replace('λ', 'lambda'))
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

    def add_heading_1(self, text, space_before=8.0, space_after=14.0, check_h=75.0):
        self.check_space(check_h)
        self.current_y -= space_before
        self.draw_text(text, MARGIN_LEFT, self.current_y, font="F2", size=12, bold=True)
        self.current_y -= space_after

    def add_heading_2(self, text):
        self.check_space(100.0)
        self.current_y -= 7.0
        self.draw_text(text, MARGIN_LEFT, self.current_y, font="F2", size=11, bold=True)
        self.current_y -= 13.0

    def add_formula(self, formula_text):
        self.check_space(32.0)
        self.current_y -= 5.0
        w = string_width(formula_text, 11, bold=False)
        x = MARGIN_LEFT + (PRINT_W - w) / 2.0
        self.draw_text(formula_text, x, self.current_y, font="F3", size=11, italic=True)
        self.current_y -= 16.0

    def add_numbered_item(self, num_str, text, size=11, line_pitch=14.0, space_after=3.5):
        indent_num = 25.0
        body_w = PRINT_W - indent_num
        words = text.split(' ')
        lines = []
        cur_line = []
        for w in words:
            test_line = ' '.join(cur_line + [w])
            if string_width(test_line, size) <= body_w:
                cur_line.append(w)
            else:
                if cur_line:
                    lines.append(' '.join(cur_line))
                    cur_line = [w]
                else:
                    lines.append(w)
                    cur_line = []
        if cur_line:
            lines.append(' '.join(cur_line))

        total_h = len(lines) * line_pitch + space_after
        self.check_space(total_h)

        y = self.current_y
        self.draw_text(num_str, MARGIN_LEFT + 8.0, y, font="F2", size=size, bold=True)
        for idx, l in enumerate(lines):
            lx = MARGIN_LEFT + indent_num
            is_last = (idx == len(lines) - 1)
            if not is_last and len(l.split(' ')) > 1:
                self.draw_justified_line(l, lx, y, body_w, size=size)
            else:
                self.draw_text(l, lx, y, size=size)
            y -= line_pitch
        self.current_y = y - space_after

    def add_table(self, caption, headers, rows, col_widths):
        self.check_space(45.0 + len(rows) * 15.0)
        self.draw_text(caption, MARGIN_LEFT, self.current_y, font="F2", size=9.5, bold=True)
        self.current_y -= 12.0

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
        self.current_y -= 12.0

        y_hbot = self.current_y + 2.0
        self.add_command(f"0.5 w 0 0 0 RG {x_start:.2f} {y_hbot:.2f} m {(x_start + tbl_w):.2f} {y_hbot:.2f} l S")

        for r in rows:
            x_curr = x_start
            for idx, c in enumerate(r):
                cw = string_width(c, 8.5, bold=False)
                cx = x_curr + 4.0 if (idx == 0 and len(c) > 4) else x_curr + (col_widths[idx] - cw) / 2.0
                self.draw_text(c, cx, self.current_y - 8.0, font="F1", size=8.5, bold=False)
                x_curr += col_widths[idx]
            self.current_y -= 12.0

        y_bot = self.current_y + 2.0
        self.add_command(f"0.8 w 0 0 0 RG {x_start:.2f} {y_bot:.2f} m {(x_start + tbl_w):.2f} {y_bot:.2f} l S")
        self.current_y -= 8.0

    def add_author_bio(self, num_str, name, bio):
        self.check_space(58.0)
        self.draw_text(f"{num_str} {name}", MARGIN_LEFT, self.current_y, font="F2", size=9.5, bold=True)
        self.current_y -= 10.0

        tbl_w = PRINT_W
        x_start = MARGIN_LEFT
        foto_w = 60.0
        text_w = tbl_w - foto_w - 14.0

        y_box_top = self.current_y
        box_h = 44.0
        self.add_command(f"0.5 w 0 0 0 RG {x_start:.2f} {(y_box_top - box_h):.2f} {foto_w:.2f} {box_h:.2f} re S")
        self.draw_text("Foto", x_start + 22.0, y_box_top - 25.0, font="F1", size=8.5)

        words = bio.split(' ')
        cur_l = []
        cur_y = y_box_top - 9.0
        for w in words:
            test = ' '.join(cur_l + [w])
            if string_width(test, 8.5) <= text_w:
                cur_l.append(w)
            else:
                self.draw_text(' '.join(cur_l), x_start + foto_w + 12.0, cur_y, font="F1", size=8.5)
                cur_l = [w]
                cur_y -= 11.5
        if cur_l:
            self.draw_text(' '.join(cur_l), x_start + foto_w + 12.0, cur_y, font="F1", size=8.5)

        self.current_y = min(cur_y, y_box_top - box_h) - 10.0

    def finalize(self):
        if self.current_page_stream:
            self.pages.append(self.current_page_stream)

def build_pdf():
    doc = PDFDoc()

    doc.add_paragraph("EXPLORAÇÃO DO ALGORITMO QAOA PARA OTIMIZAÇÃO EM MODELOS DE CLASSIFICAÇÃO SUPERVISIONADA UTILIZANDO SIMULADORES QUÂNTICOS", size=12, bold=True, align="center", first_line_indent=0, line_pitch=15, space_after=4)
    doc.add_paragraph("EXPLORATION OF THE QAOA ALGORITHM FOR OPTIMIZATION IN SUPERVISED CLASSIFICATION MODELS USING QUANTUM SIMULATORS", size=12, bold=True, align="center", first_line_indent=0, line_pitch=15, space_after=10)

    doc.add_paragraph("Julio Coronetti Regino ¹, Cainã Antunes ²", size=11, bold=True, align="left", first_line_indent=0, line_pitch=14, space_after=10)

    doc.add_paragraph("RESUMO", size=11, bold=True, align="left", first_line_indent=0, line_pitch=13, space_after=3)
    resumo_text = ("Este estudo avalia a viabilidade de formulações de otimização discreta associadas ao algoritmo QAOA em tarefas de classificação supervisionada, utilizando simuladores quânticos e comparação com métodos clássicos. A metodologia adotou o conjunto de dados breast cancer da biblioteca scikit-learn, com separação estratificada entre treino e teste, normalização, redução de dimensionalidade por PCA e avaliação por acurácia e tempo de execução. Inicialmente, foi estabelecido um baseline com SVM linear e VQC simulado. Em seguida, foi implementada uma formulação QUBO simplificada de classificador linear discretizado, resolvida por QAOA em instâncias pequenas e por solução exata em uma análise preliminar de escalabilidade. Os resultados indicaram que o baseline VQC atingiu 83,33% de acurácia, enquanto o SVM clássico atingiu 100,00%. Na etapa QUBO/QAOA, a instância com 2 componentes PCA obteve 90,00% de acurácia com QAOA, porém com tempo superior ao SVM.")
    doc.add_paragraph(resumo_text, size=10.5, align="justify", first_line_indent=0, line_pitch=13.5, space_after=3)
    doc.add_paragraph("Palavras-chave: QAOA; QUBO; classificação supervisionada; aprendizado de máquina quântico; simuladores quânticos.", size=10.5, bold=False, align="left", first_line_indent=0, line_pitch=13.5, space_after=8)

    doc.add_paragraph("ABSTRACT", size=11, bold=True, align="left", first_line_indent=0, line_pitch=13, space_after=3)
    abstract_text = ("This study evaluates the feasibility of discrete optimization formulations associated with the QAOA algorithm in supervised classification tasks, using quantum simulators and comparison with classical methods. The methodology used the breast cancer dataset from scikit-learn, with stratified train-test split, normalization, dimensionality reduction through PCA, and evaluation by accuracy and execution time. First, a baseline was established with a linear SVM and a simulated VQC. Then, a simplified QUBO formulation of a discretized linear classifier was implemented and solved with QAOA in small instances and with an exact solver in a preliminary scalability analysis. The results indicated that the VQC baseline reached 83.33% accuracy, while the classical SVM reached 100.00%. In the QUBO/QAOA stage, the instance with 2 PCA components achieved 90.00% accuracy with QAOA, although with higher execution time than SVM.")
    doc.add_paragraph(abstract_text, size=10.5, align="justify", first_line_indent=0, line_pitch=13.5, space_after=3)
    doc.add_paragraph("Keywords: QAOA; QUBO; supervised classification; quantum machine learning; quantum simulators.", size=10.5, bold=False, align="left", first_line_indent=0, line_pitch=13.5, space_after=10)

    doc.add_heading_1("1 INTRODUÇÃO")
    doc.add_paragraph("A computação quântica ainda não substitui os métodos clássicos de aprendizado de máquina, mas já permite investigar novas formas de formular problemas de otimização. Esse recorte é especialmente importante na era NISQ, em que os dispositivos possuem número limitado de qubits, ruído e restrições de profundidade de circuito (Preskill, 2018; Bharti et al., 2022). Por isso, algoritmos híbridos variacionais, que combinam circuitos quânticos parametrizados com rotinas clássicas de otimização, tornaram-se uma alternativa prática para estudos exploratórios (Cerezo et al., 2021; Grange; Poss; Bourreau, 2024).", size=11, line_pitch=14.5, space_after=6)
    doc.add_paragraph("Entre esses algoritmos, o QAOA (Quantum Approximate Optimization Algorithm) se destaca por lidar diretamente com problemas de otimização combinatória (Farhi; Goldstone; Gutmann, 2014). A classificação supervisionada, embora normalmente tratada por modelos estatísticos ou geométricos, também pode ser interpretada como um problema de busca por parâmetros que minimizam uma função de erro. A partir dessa ligação, este trabalho converte uma tarefa de classificação binária em uma formulação QUBO (Quadratic Unconstrained Binary Optimization) e avalia sua resolução por simulação quântica (Glover; Kochenberger; Du, 2019; Lucas, 2014).", size=11, line_pitch=14.5, space_after=6)
    doc.add_paragraph("A questão central não é demonstrar vantagem quântica, mas verificar até onde uma formulação QUBO associada ao QAOA consegue produzir resultados utilizáveis em uma tarefa pequena de classificação. Para isso, a abordagem foi comparada com SVM linear e VQC simulado, considerando acurácia, tempo de execução e crescimento do número de variáveis binárias após a variação de componentes PCA.", size=11, line_pitch=14.5, space_after=10)

    doc.add_heading_1("2 REVISÃO DE LITERATURA")
    doc.add_paragraph("Esta seção organiza os conceitos que orientaram o experimento. As referências foram usadas para justificar três decisões principais: trabalhar em escala compatível com a era NISQ, reduzir dimensionalidade antes dos circuitos e tratar a formulação QUBO como uma ponte experimental entre classificação e otimização combinatória.", size=11, line_pitch=14.5, space_after=8)

    doc.add_heading_2("2.1 Computação quântica na era NISQ")
    doc.add_paragraph("A era NISQ descreve um estágio em que processadores quânticos possuem quantidade limitada de qubits, conectividade restrita e presença de ruído. Essa limitação ajuda a explicar por que este trabalho adota simulação e instâncias pequenas, em vez de propor uma solução quântica em larga escala. Algoritmos híbridos, que distribuem o processo entre circuitos quânticos e otimizadores clássicos, tornam-se uma alternativa prática para esse tipo de investigação (Preskill, 2018; Bharti et al., 2022). Estudos recentes com processadores reais e VQCs reforçam a mesma cautela: ruído, orçamento de medições, profundidade de circuito e condições de hardware afetam diretamente a estabilidade dos resultados (Singh; Vishwakarma, 2026; Park; Son, 2026).", size=11, line_pitch=14.5, space_after=8)

    doc.add_heading_2("2.2 Algoritmos variacionais e QAOA")
    doc.add_paragraph("O QAOA é um algoritmo variacional voltado a problemas de otimização combinatória. Seu funcionamento alterna operadores associados ao custo do problema e operadores de mistura, enquanto os parâmetros são ajustados por um otimizador clássico (Farhi; Goldstone; Gutmann, 2014). Essa estrutura torna o QAOA adequado para este estudo porque um problema QUBO pode ser convertido em Hamiltoniano de custo e avaliado por circuitos parametrizados, seguindo o paradigma mais amplo dos algoritmos quânticos variacionais (Cerezo et al., 2021; Grange; Poss; Bourreau, 2024).", size=11, line_pitch=14.5, space_after=8)

    doc.add_heading_2("2.3 Aprendizado de máquina quântico e classificação")
    doc.add_paragraph("No aprendizado de máquina quântico, modelos de classificação podem usar circuitos quânticos para mapear dados clássicos em espaços de maior dimensionalidade ou para resolver formulações de otimização ligadas ao treinamento de classificadores (Schuld; Killoran, 2019; Havlíček et al., 2019). Revisões recentes indicam que QML ainda é um campo em consolidação, com aplicações recorrentes em classificadores, redes neurais quânticas e métodos de kernel (Sood; Agrewal, 2024). Neste trabalho, o SVM cumpre dois papéis: serve como baseline clássico forte e também como referência conceitual, já que aparece na literatura de aprendizado de máquina quântico aplicada à classificação (Rebentrost; Mohseni; Lloyd, 2014).", size=11, line_pitch=14.5, space_after=8)

    doc.add_heading_2("2.4 Pré-processamento, dimensionalidade e otimizadores")
    doc.add_paragraph("O pré-processamento dos dados é uma etapa crítica em modelos quânticos de classificação. Estudos sobre QML indicam que técnicas clássicas de codificação e redução de dimensionalidade influenciam diretamente o desempenho de modelos variacionais em ambientes NISQ (Mancilla; Pere, 2022). Esse ponto justifica o uso de PCA no experimento: reduzir atributos diminui a quantidade de variáveis e torna a simulação viável. A mesma preocupação aparece em estudos sobre VQCs aplicados a dados de alta dimensionalidade, nos quais o aumento do número de atributos demanda mais qubits, eleva o tempo de treinamento e dificulta a convergência (Qi et al., 2025). Além disso, a seleção do otimizador clássico pode alterar tanto a acurácia quanto o tempo de treinamento em modelos de QML, o que justifica o uso de SPSA e COBYLA em etapas diferentes do estudo (AL Ajmi; Shoaib, 2025).", size=11, line_pitch=14.5, space_after=8)

    doc.add_heading_2("2.5 Formulações QUBO")
    doc.add_paragraph("Um problema QUBO consiste em minimizar uma função quadrática sem restrições explícitas sobre variáveis binárias. Essa formulação é útil por permitir a representação de problemas combinatórios e sua posterior conversão para modelos compatíveis com algoritmos quânticos de otimização (Glover; Kochenberger; Du, 2019; Lucas, 2014). Em classificação, há trabalhos recentes que exploram a representação de SVM como problema QUBO e comparam abordagens clássicas, quânticas e híbridas (Guddanti et al., 2024). Neste estudo, a formulação QUBO foi usada de forma mais restrita: ela funciona como uma aproximação experimental de classificador linear discretizado, suficiente para avaliar o comportamento inicial do QAOA, mas sem substituir uma formulação completa do SVM.", size=11, line_pitch=14.5, space_after=10)

    doc.add_heading_1("3 METODOLOGIA")
    doc.add_paragraph("O experimento foi desenvolvido em Python, utilizando as bibliotecas scikit-learn, Qiskit, Qiskit Machine Learning, Qiskit Optimization e Qiskit Algorithms. A implementação foi organizada em dois scripts principais: script.py, responsável pelo baseline clássico e VQC, e script_qaoa.py, responsável pela formulação QUBO e pelas execuções com QAOA.", size=11, line_pitch=14.5, space_after=8)

    doc.add_heading_2("3.1 Base de dados e pré-processamento")
    doc.add_paragraph("Foi utilizado o conjunto de dados breast cancer, disponibilizado pela biblioteca scikit-learn. A amostra utilizada nos experimentos possui 100 registros selecionados de forma estratificada, mantendo a proporção entre as classes. Em seguida, os dados foram divididos em 70% para treino e 30% para teste, também com estratificação.", size=11, line_pitch=14.5, space_after=6)
    doc.add_paragraph("O pré-processamento seguiu as seguintes etapas:", size=11, line_pitch=14.5, space_after=6)
    doc.add_numbered_item("1.", "Padronização dos atributos com StandardScaler, ajustado apenas no conjunto de treino.", size=11, line_pitch=14.5, space_after=4.0)
    doc.add_numbered_item("2.", "Redução de dimensionalidade com PCA, também ajustado apenas no treino.", size=11, line_pitch=14.5, space_after=4.0)
    doc.add_numbered_item("3.", "Reescala dos componentes para o intervalo [0, 1] com MinMaxScaler.", size=11, line_pitch=14.5, space_after=6.0)
    doc.add_paragraph("Essa organização evita vazamento de informação do conjunto de teste para o treinamento.", size=11, line_pitch=14.5, space_after=8)

    doc.add_heading_2("3.2 Baseline clássico e baseline quântico variacional")
    doc.add_paragraph("O primeiro baseline foi um SVM linear, usado como referência clássica. Em seguida, foi implementado um classificador variacional quântico simulado (VQC), com mapa de características ZZFeatureMap, ansatz RealAmplitudes e otimizador SPSA com maxiter=100. O SPSA foi escolhido por ser um método de aproximação estocástica com perturbações simultâneas, frequentemente associado a cenários de otimização com ruído (Spall, 1992). Essa etapa teve como objetivo estabilizar um modelo quântico inicial antes da formulação QUBO/QAOA.", size=11, line_pitch=14.5, space_after=8)

    doc.add_heading_2("3.3 Formulação QUBO")
    doc.add_paragraph("Na etapa principal, a classificação foi representada como um classificador linear discretizado. Cada coeficiente do modelo, incluindo o viés, foi codificado por variáveis binárias de contribuição positiva e negativa. Para d componentes PCA, o número de variáveis binárias foi definido como:", size=11, line_pitch=14.5, space_after=6)
    doc.add_formula("n_bin = 2(d + 1)")
    doc.add_paragraph("A função objetivo minimizada foi uma perda quadrática de margem:", size=11, line_pitch=14.5, space_after=6)
    doc.add_formula("L(w, b) = (1 / n) * sum_{i=1}^n (b + x_i * w - y_i)^2")
    doc.add_paragraph("em que b representa o viés, w os pesos discretizados, x_i os atributos após PCA e y_i in {-1, 1} a classe transformada. Também foram adicionadas regularização quadrática dos coeficientes e penalização para evitar ativação simultânea de bits positivos e negativos do mesmo coeficiente.", size=11, line_pitch=14.5, space_after=6)
    doc.add_paragraph("É importante destacar que esta formulação é uma aproximação experimental de classificador linear discretizado em QUBO, e não uma implementação completa do SVM dual.", size=11, line_pitch=14.5, space_after=8)

    doc.add_heading_2("3.4 Execução com QAOA e solver exato")
    doc.add_paragraph("O QUBO foi resolvido por QAOA em instâncias pequenas, usando StatevectorSampler, QAOA com reps=1 e otimizador COBYLA. Para avaliar a escalabilidade da formulação sem sobrecarregar o ambiente de execução, também foi implementado um solver exato por força bruta para os QUBOs pequenos. Esse solver foi utilizado na análise preliminar com PCA variando de 2 a 5 componentes.", size=11, line_pitch=14.5, space_after=6)
    doc.add_paragraph("As métricas coletadas foram acurácia, tempo de execução, número de componentes PCA e número de variáveis binárias.", size=11, line_pitch=14.5, space_after=10)

    doc.add_heading_1("4 RESULTADOS E DISCUSSÕES")
    doc.add_heading_2("4.1 Baseline da Fase 1")
    doc.add_paragraph("O primeiro resultado funciona como controle para as etapas seguintes. O baseline clássico com SVM atingiu 100,00% de acurácia no conjunto de teste, enquanto o VQC simulado atingiu 83,33%. Assim, o modelo quântico variacional superou o critério prático de 80% estabelecido para a Fase 1, mas ainda com tempo de execução superior ao SVM.", size=11, line_pitch=14.5, space_after=6)
    doc.add_table(
        "Tabela 1: Resultado do baseline da Fase 1.",
        ["Modelo", "Acurácia", "Tempo"],
        [["SVM linear", "100,00%", "0,0009 s"],
         ["VQC simulado", "83,33%", "12,8098 s"]],
        [180.0, 130.0, 143.54]
    )

    doc.add_heading_2("4.2 Execução inicial QUBO/QAOA")
    doc.add_paragraph("Na etapa QUBO/QAOA inicial, foi executada uma instância com 2 componentes PCA, totalizando 6 variáveis binárias. O QAOA obteve 90,00% de acurácia, enquanto o SVM linear manteve 100,00%. Esse resultado não indica superioridade do método quântico, mas mostra que a formulação proposta consegue gerar uma fronteira de decisão utilizável em escala pequena.", size=11, line_pitch=14.5, space_after=6)
    doc.add_table(
        "Tabela 2: Execução inicial QAOA/QUBO com 2 componentes PCA.",
        ["Modelo", "Variáveis binárias", "Acurácia", "Tempo"],
        [["SVM linear", "0", "100,00%", "0,0013 s"],
         ["QAOA-QUBO linear", "6", "90,00%", "3,6997 s"]],
        [160.0, 110.0, 90.0, 93.54]
    )

    doc.add_heading_2("4.3 Análise preliminar de escalabilidade")
    doc.add_paragraph("Para observar o impacto do aumento de dimensionalidade, foi utilizado o solver exato em QUBOs com PCA variando de 2 a 5 componentes. A acurácia permaneceu em 90,00%, mas o tempo de solução aumentou conforme o número de variáveis binárias cresceu. Essa etapa separa dois aspectos do problema: a qualidade da formulação de classificação e o custo de busca no espaço binário.", size=11, line_pitch=14.5, space_after=6)
    doc.add_table(
        "Tabela 3: Resultado preliminar do QUBO exato por número de componentes PCA.",
        ["PCA", "Variáveis binárias", "Acurácia QUBO", "Tempo QUBO"],
        [["2", "6", "90,00%", "0,0824 s"],
         ["3", "8", "90,00%", "0,4580 s"],
         ["4", "10", "90,00%", "1,2578 s"],
         ["5", "12", "90,00%", "7,1497 s"]],
        [70.0, 130.0, 120.0, 133.54]
    )

    doc.add_paragraph("Com QAOA, o custo de execução cresceu de forma mais acentuada. A instância com 3 componentes PCA levou 41,7146 segundos, enquanto a instância com 4 componentes PCA, mesmo com maxiter=5, levou 863,4231 segundos.", size=11, line_pitch=14.5, space_after=6)
    doc.add_table(
        "Tabela 4: Resultado preliminar das execuções QAOA por número de componentes PCA.",
        ["PCA", "Variáveis binárias", "Maxiter", "Acurácia QAOA", "Tempo QAOA"],
        [["2", "6", "20", "90,00%", "3,6997 s"],
         ["3", "8", "20", "90,00%", "41,7146 s"],
         ["4", "10", "5", "96,67%*", "863,4231 s"]],
        [60.0, 110.0, 70.0, 105.0, 108.54]
    )
    doc.add_paragraph("Nota: * Otimizador COBYLA limitado a 5 iterações por restrição de tempo de simulação.", size=8.5, italic=True, align="left", first_line_indent=0, line_pitch=11.0, space_after=8.0)

    doc.add_paragraph("Em conjunto, os resultados mostram uma diferença importante entre funcionar e escalar. A formulação QUBO/QAOA produziu classificações coerentes em instâncias pequenas, mas o custo de simulação cresceu rapidamente. A comparação com o SVM deixa claro que a viabilidade da abordagem não pode ser avaliada apenas pela acurácia: tempo de execução, número de variáveis binárias e escalabilidade são parte central da análise. Essa interpretação é consistente com estudos recentes sobre VQCs e dispositivos NISQ, que indicam sensibilidade a codificação, profundidade de circuito, ruído e dimensionalidade dos dados (Qi et al., 2025; Park; Son, 2026; Singh; Vishwakarma, 2026).", size=11, line_pitch=14.5, space_after=10)

    doc.add_heading_1("5 CONCLUSÃO")
    doc.add_paragraph("Este trabalho analisou, em caráter exploratório, o uso de QAOA e formulações QUBO em uma tarefa de classificação supervisionada. O SVM clássico manteve o melhor desempenho geral em acurácia e tempo, enquanto o VQC e a formulação QAOA/QUBO demonstraram viabilidade apenas em instâncias pequenas.", size=11, line_pitch=14.5, space_after=6)
    doc.add_paragraph("A principal contribuição do estudo está na formulação e na análise de seus limites, não na defesa de superioridade quântica. A classificação foi convertida em um problema de otimização discreta, resolvido por QAOA em cenários controlados. A instância com 2 componentes PCA atingiu 90,00% de acurácia, demonstrando que a abordagem pode produzir uma solução competitiva em pequena escala. No entanto, o aumento do número de variáveis binárias elevou significativamente o tempo de execução, especialmente nas simulações com QAOA.", size=11, line_pitch=14.5, space_after=6)
    doc.add_paragraph("Como próximos passos, recomenda-se investigar formulações QUBO mais próximas do SVM dual, testar diferentes discretizações dos pesos, avaliar outros otimizadores clássicos e executar experimentos em ambientes com maior capacidade computacional. Também seria relevante comparar os resultados com simulações ruidosas ou hardware quântico real, para aproximar o estudo das limitações observadas em dispositivos NISQ.", size=11, line_pitch=14.5, space_after=10)

    doc.add_heading_1("AGRADECIMENTOS")
    doc.add_paragraph("Agradece-se à Faculdade de Tecnologia SENAI Gaspar Ricardo Júnior pelo suporte institucional e de infraestrutura concedido ao desenvolvimento desta pesquisa.", size=10.5, line_pitch=13.5, space_after=10)

    doc.add_heading_1("REFERÊNCIAS")
    refs = [
        "AL AJMI, N. A.; SHOAIB, M. Optimization Strategies in Quantum Machine Learning: A Performance Analysis. Applied Sciences, v. 15, n. 8, p. 4493, 2025.",
        "BHARTI, K. et al. Noisy intermediate-scale quantum algorithms. Reviews of Modern Physics, v. 94, n. 1, p. 015004, 2022.",
        "CEREZO, M. et al. Variational quantum algorithms. Nature Reviews Physics, v. 3, p. 625-644, 2021.",
        "FARHI, E.; GOLDSTONE, J.; GUTMANN, S. A Quantum Approximate Optimization Algorithm. arXiv:1411.4028, 2014.",
        "GLOVER, F.; KOCHENBERGER, G.; DU, Y. A Tutorial on Formulating and Using QUBO Models. arXiv:1811.11538, 2019.",
        "GRANGE, C.; POSS, M.; BOURREAU, E. An introduction to variational quantum algorithms for combinatorial optimization problems. Annals of Operations Research, v. 343, n. 2, p. 847-884, 2024.",
        "GUDDANTI, S. S. et al. Pneumonia detection by binary classification: classical, quantum, and hybrid approaches for support vector machine (SVM). Frontiers in Computer Science, v. 5, 2024.",
        "HAVLÍČEK, V. et al. Supervised learning with quantum-enhanced feature spaces. Nature, v. 567, p. 209-212, 2019.",
        "LUCAS, A. Ising formulations of many NP problems. Frontiers in Physics, v. 2, p. 5, 2014.",
        "MANCILLA, J.; PERE, C. A Preprocessing Perspective for Quantum Machine Learning Classification Advantage in Finance Using NISQ Algorithms. Entropy, v. 24, n. 11, p. 1656, 2022.",
        "PARK, S.; SON, Y. Sensitivity Analysis of Variational Quantum Classifiers for Identifying Dummy Power Traces in Side-Channel Analysis. Applied Sciences, v. 16, n. 7, p. 3243, 2026.",
        "PRESKILL, J. Quantum Computing in the NISQ era and beyond. Quantum, v. 2, p. 79, 2018.",
        "QI, H. et al. A high-efficiency variational quantum classifier for high-dimensional data. Journal of Supercomputing, v. 81, n. 1, p. 1-20, 2025.",
        "REBENTROST, P.; MOHSENI, M.; LLOYD, S. Quantum support vector machine for big data classification. Physical Review Letters, v. 113, p. 130503, 2014.",
        "SCHULD, M.; KILLORAN, N. Quantum Machine Learning in Feature Hilbert Spaces. Physical Review Letters, v. 122, p. 040504, 2019.",
        "SINGH, S.; VISHWAKARMA, D. K. Performance Analysis of Quantum Arithmetic Circuits on IBM Eagle Processor. Defence Science Journal, v. 76, n. 2, p. 233-241, 2026.",
        "SOOD, S. K.; AGREWAL, M. Quantum Machine Learning for Computational Methods in Engineering: A Systematic Review. Archives of Computational Methods in Engineering, v. 31, n. 3, p. 1555-1577, 2024.",
        "SPALL, J. C. Multivariate stochastic approximation using a simultaneous perturbation gradient approximation. IEEE Transactions on Automatic Control, v. 37, n. 3, p. 332-341, 1992."
    ]
    for r in refs:
        doc.add_paragraph(r, size=8.5, align="justify", first_line_indent=0, line_pitch=11.5, space_after=2.5)

    doc.add_heading_1("SOBRE O(S) AUTOR(ES)")
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

if __name__ == '__main__':
    build_pdf()
