import argparse
import csv
import time
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from sklearn.metrics import accuracy_score

from script import load_and_preprocess, set_qiskit_seed, train_classic


DEFAULT_OUTPUT = "resultados/resultados_qaoa_pca.csv"


@dataclass
class QaoaConfig:
    n_samples: int = 100
    n_components: int = 2
    random_state: int = 42
    bits_per_sign: int = 1
    coefficient_scale: float = 2.0
    regularization: float = 0.05
    mutual_exclusion: float = 0.25
    qaoa_reps: int = 1
    optimizer_name: str = "COBYLA"
    maxiter: int = 60
    solver_name: str = "qaoa"


TermMap = Dict[str, float]
CoefficientTerms = List[List[Tuple[str, float]]]


def signed_labels(y: np.ndarray) -> np.ndarray:
    return np.where(y == 1, 1.0, -1.0)


def create_optimizer(name: str, maxiter: int):
    name_norm = name.strip().upper()
    if name_norm == "COBYLA":
        return COBYLA(maxiter=maxiter)
    if name_norm == "SPSA":
        return SPSA(maxiter=maxiter)
    raise ValueError(f"Otimizador nao suportado para QAOA: {name}")


def create_coefficient_terms(config: QaoaConfig) -> CoefficientTerms:
    terms: CoefficientTerms = []
    for coef_idx in range(config.n_components + 1):
        coef_terms: List[Tuple[str, float]] = []
        for bit_idx in range(config.bits_per_sign):
            magnitude = config.coefficient_scale * (2**bit_idx)
            coef_terms.append((f"c{coef_idx}_neg_b{bit_idx}", -magnitude))
            coef_terms.append((f"c{coef_idx}_pos_b{bit_idx}", magnitude))
        terms.append(coef_terms)
    return terms


def sample_terms(x_row: np.ndarray, coefficient_terms: CoefficientTerms) -> TermMap:
    terms: TermMap = {}
    for coef_idx, coef_terms in enumerate(coefficient_terms):
        multiplier = 1.0 if coef_idx == 0 else float(x_row[coef_idx - 1])
        for variable_name, weight in coef_terms:
            terms[variable_name] = weight * multiplier
    return terms


def add_squared_expression(
    linear: Dict[str, float],
    quadratic: Dict[Tuple[str, str], float],
    constant: List[float],
    terms: TermMap,
    target: float,
    weight: float,
) -> None:
    variable_names = sorted(terms)
    constant[0] += weight * target * target

    for var_name in variable_names:
        coef = terms[var_name]
        linear[var_name] += weight * (-2.0 * target * coef + coef * coef)

    for idx, left_name in enumerate(variable_names):
        for right_name in variable_names[idx + 1 :]:
            left_coef = terms[left_name]
            right_coef = terms[right_name]
            quadratic[(left_name, right_name)] += weight * 2.0 * left_coef * right_coef


def build_qubo(
    X_train: np.ndarray,
    y_train: np.ndarray,
    config: QaoaConfig,
) -> Tuple[QuadraticProgram, CoefficientTerms]:
    coefficient_terms = create_coefficient_terms(config)
    qp = QuadraticProgram("discrete_linear_classifier")

    for coef_terms in coefficient_terms:
        for variable_name, _ in coef_terms:
            qp.binary_var(variable_name)

    linear: Dict[str, float] = defaultdict(float)
    quadratic: Dict[Tuple[str, str], float] = defaultdict(float)
    constant = [0.0]
    y_signed = signed_labels(y_train)
    sample_weight = 1.0 / len(X_train)

    for x_row, target in zip(X_train, y_signed):
        terms = sample_terms(x_row, coefficient_terms)
        add_squared_expression(linear, quadratic, constant, terms, target, sample_weight)

    for coef_terms in coefficient_terms:
        reg_terms = {variable_name: weight for variable_name, weight in coef_terms}
        add_squared_expression(
            linear,
            quadratic,
            constant,
            reg_terms,
            target=0.0,
            weight=config.regularization,
        )

        for bit_idx in range(config.bits_per_sign):
            neg_name = f"c{coefficient_terms.index(coef_terms)}_neg_b{bit_idx}"
            pos_name = f"c{coefficient_terms.index(coef_terms)}_pos_b{bit_idx}"
            quadratic[tuple(sorted((neg_name, pos_name)))] += config.mutual_exclusion

    qp.minimize(
        constant=constant[0],
        linear=dict(linear),
        quadratic=dict(quadratic),
    )
    return qp, coefficient_terms


def decode_weights(
    variables: Dict[str, float],
    coefficient_terms: CoefficientTerms,
) -> Tuple[float, np.ndarray]:
    coefficients = []
    for coef_terms in coefficient_terms:
        coefficients.append(sum(weight * variables.get(variable_name, 0.0) for variable_name, weight in coef_terms))
    return float(coefficients[0]), np.array(coefficients[1:], dtype=float)


def solve_qubo_exact(qp: QuadraticProgram) -> Tuple[Dict[str, float], float, str]:
    variable_names = [variable.name for variable in qp.variables]
    best_bits = None
    best_value = None

    for bits in product([0.0, 1.0], repeat=len(variable_names)):
        bit_array = np.array(bits, dtype=float)
        value = float(qp.objective.evaluate(bit_array))
        if best_value is None or value < best_value:
            best_bits = bit_array
            best_value = value

    if best_bits is None or best_value is None:
        raise RuntimeError("Nao foi possivel resolver o QUBO por forca bruta.")

    variables = {name: float(value) for name, value in zip(variable_names, best_bits)}
    return variables, best_value, "SUCCESS_EXACT"


def solve_qubo_qaoa(
    qp: QuadraticProgram,
    config: QaoaConfig,
) -> Tuple[Dict[str, float], float, str, float]:
    optimizer = create_optimizer(config.optimizer_name, config.maxiter)
    sampler = StatevectorSampler(seed=config.random_state)
    qaoa = QAOA(
        sampler=sampler,
        optimizer=optimizer,
        reps=config.qaoa_reps,
        initial_point=np.full(2 * config.qaoa_reps, 0.1),
    )
    solver = MinimumEigenOptimizer(qaoa)

    start = time.time()
    result = solver.solve(qp)
    duration = time.time() - start
    status = getattr(result.status, "name", str(result.status))
    return result.variables_dict, float(result.fval), status, duration


def predict_linear(X: np.ndarray, bias: float, weights: np.ndarray) -> np.ndarray:
    scores = bias + X @ weights
    return np.where(scores >= 0.0, 1, 0)


def run_single_experiment(config: QaoaConfig) -> List[Dict[str, object]]:
    set_qiskit_seed(config.random_state)
    X_train, X_test, y_train, y_test = load_and_preprocess(
        n_samples=config.n_samples,
        n_components=config.n_components,
        random_state=config.random_state,
    )

    _, svm_accuracy, svm_time = train_classic(X_train, y_train, X_test, y_test)

    qp, coefficient_terms = build_qubo(X_train, y_train, config)

    if config.solver_name == "exact":
        start = time.time()
        variables, objective_value, status = solve_qubo_exact(qp)
        solver_time = time.time() - start
        model_name = "Exact-QUBO linear"
        optimizer_name = "BRUTE_FORCE"
        maxiter = ""
    else:
        variables, objective_value, status, solver_time = solve_qubo_qaoa(qp, config)
        model_name = "QAOA-QUBO linear"
        optimizer_name = config.optimizer_name.upper()
        maxiter = config.maxiter

    bias, weights = decode_weights(variables, coefficient_terms)
    qaoa_predictions = predict_linear(X_test, bias, weights)
    qaoa_accuracy = accuracy_score(y_test, qaoa_predictions)

    shared = {
        "fase": 2,
        "n_samples": config.n_samples,
        "n_components": config.n_components,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "qaoa_reps": config.qaoa_reps,
        "bits_per_sign": config.bits_per_sign,
        "coefficient_scale": config.coefficient_scale,
        "regularization": config.regularization,
        "mutual_exclusion": config.mutual_exclusion,
    }

    return [
        {
            **shared,
            "modelo": "SVM linear",
            "otimizador": "",
            "maxiter": "",
            "n_binary_variables": 0,
            "accuracy": svm_accuracy,
            "train_time_seconds": svm_time,
            "objective_value": "",
            "status": "SUCCESS",
            "observacoes": "Baseline classico no mesmo split.",
        },
        {
            **shared,
            "modelo": model_name,
            "otimizador": optimizer_name,
            "maxiter": maxiter,
            "n_binary_variables": qp.get_num_binary_vars(),
            "accuracy": qaoa_accuracy,
            "train_time_seconds": solver_time,
            "objective_value": objective_value,
            "status": status,
            "observacoes": "QUBO de classificador linear discretizado com perda quadratica de margem.",
        },
    ]


def write_csv(rows: Iterable[Dict[str, object]], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    if not rows:
        return

    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def print_rows(rows: Iterable[Dict[str, object]]) -> None:
    for row in rows:
        accuracy = float(row["accuracy"]) * 100.0
        duration = float(row["train_time_seconds"])
        print(
            f"PCA={row['n_components']} | {row['modelo']} | "
            f"acc={accuracy:.2f}% | tempo={duration:.4f}s | "
            f"vars={row['n_binary_variables']} | status={row['status']}"
        )


def parse_components(value: str) -> List[int]:
    if "," in value:
        return [int(item.strip()) for item in value.split(",") if item.strip()]
    return [int(value)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa classificador QUBO/QAOA para a IC.")
    parser.add_argument("--components", default="2", help="Componentes PCA. Use '2' ou '2,3,4,5'.")
    parser.add_argument("--stress", action="store_true", help="Executa PCA 2, 3, 4 e 5.")
    parser.add_argument("--n-samples", type=int, default=100)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--bits-per-sign", type=int, default=1)
    parser.add_argument("--coefficient-scale", type=float, default=2.0)
    parser.add_argument("--regularization", type=float, default=0.05)
    parser.add_argument("--mutual-exclusion", type=float, default=0.25)
    parser.add_argument("--qaoa-reps", type=int, default=1)
    parser.add_argument("--optimizer", default="COBYLA", choices=["COBYLA", "SPSA"])
    parser.add_argument("--maxiter", type=int, default=60)
    parser.add_argument("--solver", default="qaoa", choices=["qaoa", "exact"])
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    components = [2, 3, 4, 5] if args.stress else parse_components(args.components)
    all_rows: List[Dict[str, object]] = []

    for n_components in components:
        config = QaoaConfig(
            n_samples=args.n_samples,
            n_components=n_components,
            random_state=args.random_state,
            bits_per_sign=args.bits_per_sign,
            coefficient_scale=args.coefficient_scale,
            regularization=args.regularization,
            mutual_exclusion=args.mutual_exclusion,
            qaoa_reps=args.qaoa_reps,
            optimizer_name=args.optimizer,
            maxiter=args.maxiter,
            solver_name=args.solver,
        )
        rows = run_single_experiment(config)
        all_rows.extend(rows)
        print_rows(rows)

    write_csv(all_rows, args.output)
    print(f"Resultados salvos em: {args.output}")


if __name__ == "__main__":
    main()
