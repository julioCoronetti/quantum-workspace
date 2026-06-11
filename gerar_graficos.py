import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


RESULTS_DIR = Path("resultados")


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def load_rows() -> List[Dict[str, str]]:
    paths = [
        RESULTS_DIR / "resultados_qubo_exato_pca.csv",
        RESULTS_DIR / "resultados_qaoa_pca_2.csv",
        RESULTS_DIR / "resultados_qaoa_pca_3.csv",
        RESULTS_DIR / "resultados_qaoa_pca_4.csv",
    ]
    rows: List[Dict[str, str]] = []
    for path in paths:
        if path.exists():
            rows.extend(read_csv(path))
    return rows


def collect_series(rows: Iterable[Dict[str, str]], model_name: str, metric: str) -> List[Tuple[int, float]]:
    points = []
    seen = set()
    for row in rows:
        if row["modelo"] != model_name:
            continue
        x = int(row["n_components"])
        key = (model_name, metric, x)
        if key in seen:
            continue
        seen.add(key)
        value = float(row[metric])
        points.append((x, value))
    return sorted(points)


def scale(value: float, src_min: float, src_max: float, dst_min: float, dst_max: float) -> float:
    if src_max == src_min:
        return (dst_min + dst_max) / 2
    return dst_min + (value - src_min) * (dst_max - dst_min) / (src_max - src_min)


def polyline(points: List[Tuple[int, float]], x_values: List[int], y_min: float, y_max: float, plot: Dict[str, int]) -> str:
    coords = []
    for x, y in points:
        px = scale(x, min(x_values), max(x_values), plot["left"], plot["right"])
        py = scale(y, y_min, y_max, plot["bottom"], plot["top"])
        coords.append(f"{px:.1f},{py:.1f}")
    return " ".join(coords)


def draw_chart(
    title: str,
    ylabel: str,
    series: Dict[str, List[Tuple[int, float]]],
    output: Path,
    y_min: float,
    y_max: float,
    y_labels: List[Tuple[float, str]],
) -> None:
    width = 920
    height = 560
    plot = {"left": 90, "right": 820, "top": 70, "bottom": 460}
    x_values = [2, 3, 4, 5]
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<text x="{width / 2}" y="35" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700">{title}</text>',
        f'<line x1="{plot["left"]}" y1="{plot["bottom"]}" x2="{plot["right"]}" y2="{plot["bottom"]}" stroke="#222" stroke-width="2"/>',
        f'<line x1="{plot["left"]}" y1="{plot["bottom"]}" x2="{plot["left"]}" y2="{plot["top"]}" stroke="#222" stroke-width="2"/>',
    ]

    for x in x_values:
        px = scale(x, min(x_values), max(x_values), plot["left"], plot["right"])
        parts.append(f'<line x1="{px:.1f}" y1="{plot["bottom"]}" x2="{px:.1f}" y2="{plot["bottom"] + 8}" stroke="#222"/>')
        parts.append(f'<text x="{px:.1f}" y="{plot["bottom"] + 32}" text-anchor="middle" font-family="Arial" font-size="15">{x}</text>')

    for y, label in y_labels:
        py = scale(y, y_min, y_max, plot["bottom"], plot["top"])
        parts.append(f'<line x1="{plot["left"] - 6}" y1="{py:.1f}" x2="{plot["right"]}" y2="{py:.1f}" stroke="#e6e6e6"/>')
        parts.append(f'<text x="{plot["left"] - 12}" y="{py + 5:.1f}" text-anchor="end" font-family="Arial" font-size="14">{label}</text>')

    parts.append(f'<text x="{(plot["left"] + plot["right"]) / 2}" y="{height - 28}" text-anchor="middle" font-family="Arial" font-size="16">Componentes PCA</text>')
    parts.append(f'<text x="28" y="{(plot["top"] + plot["bottom"]) / 2}" transform="rotate(-90 28 {(plot["top"] + plot["bottom"]) / 2})" text-anchor="middle" font-family="Arial" font-size="16">{ylabel}</text>')

    legend_y = 500
    for idx, (name, points) in enumerate(series.items()):
        color = colors[idx % len(colors)]
        if points:
            parts.append(f'<polyline points="{polyline(points, x_values, y_min, y_max, plot)}" fill="none" stroke="{color}" stroke-width="3"/>')
            for x, y in points:
                px = scale(x, min(x_values), max(x_values), plot["left"], plot["right"])
                py = scale(y, y_min, y_max, plot["bottom"], plot["top"])
                parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{color}"/>')
        legend_x = 90 + idx * 210
        parts.append(f'<rect x="{legend_x}" y="{legend_y}" width="18" height="18" fill="{color}"/>')
        parts.append(f'<text x="{legend_x + 26}" y="{legend_y + 14}" font-family="Arial" font-size="15">{name}</text>')

    parts.append("</svg>")
    output.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    rows = load_rows()
    RESULTS_DIR.mkdir(exist_ok=True)

    svm_acc = [(x, value * 100) for x, value in collect_series(rows, "SVM linear", "accuracy")]
    exact_acc = [(x, value * 100) for x, value in collect_series(rows, "Exact-QUBO linear", "accuracy")]
    qaoa_acc = [(x, value * 100) for x, value in collect_series(rows, "QAOA-QUBO linear", "accuracy")]
    draw_chart(
        "Acuracia por PCA",
        "Acuracia (%)",
        {"SVM": svm_acc, "QUBO exato": exact_acc, "QAOA": qaoa_acc},
        RESULTS_DIR / "grafico_acuracia_pca.svg",
        80,
        102,
        [(80, "80"), (85, "85"), (90, "90"), (95, "95"), (100, "100")],
    )

    exact_time = collect_series(rows, "Exact-QUBO linear", "train_time_seconds")
    draw_chart(
        "Tempo do QUBO exato por PCA",
        "Tempo (s)",
        {"QUBO exato": exact_time},
        RESULTS_DIR / "grafico_tempo_qubo_exato_pca.svg",
        0,
        8,
        [(0, "0"), (2, "2"), (4, "4"), (6, "6"), (8, "8")],
    )

    qaoa_time_raw = collect_series(rows, "QAOA-QUBO linear", "train_time_seconds")
    qaoa_time_log = [(x, math.log10(value)) for x, value in qaoa_time_raw]
    draw_chart(
        "Tempo do QAOA por PCA (escala log10)",
        "log10(tempo em s)",
        {"QAOA": qaoa_time_log},
        RESULTS_DIR / "grafico_tempo_qaoa_pca.svg",
        0,
        3,
        [(0, "1s"), (1, "10s"), (2, "100s"), (3, "1000s")],
    )

    print("Graficos gerados em resultados/*.svg")


if __name__ == "__main__":
    main()
