import time
import importlib
from inspect import signature
from typing import Any, Dict, Optional, Tuple

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


def get_qiskit_primitives() -> Dict[str, Any]:
    """Detecta dinamicamente primitives do Qiskit quando disponíveis."""
    Sampler = None
    _HAS_SAMPLER_PRIMITIVE = False
    try:
        primitives_mod = importlib.import_module("qiskit.primitives")
        Sampler = getattr(primitives_mod, "Sampler", None)
        _HAS_SAMPLER_PRIMITIVE = Sampler is not None
    except Exception:
        Sampler = None
        _HAS_SAMPLER_PRIMITIVE = False

    QuantumInstance = None
    AerSimulator = None
    _HAS_AER = False
    try:
        qiskit_utils = importlib.import_module("qiskit.utils")
        QuantumInstance = getattr(qiskit_utils, "QuantumInstance", None)
        aer_mod = importlib.import_module("qiskit.providers.aer")
        AerSimulator = getattr(aer_mod, "AerSimulator", None)
        _HAS_AER = AerSimulator is not None
    except Exception:
        QuantumInstance = None
        AerSimulator = None
        _HAS_AER = False

    return {
        "Sampler": Sampler,
        "QuantumInstance": QuantumInstance,
        "AerSimulator": AerSimulator,
        "_HAS_SAMPLER_PRIMITIVE": _HAS_SAMPLER_PRIMITIVE,
        "_HAS_AER": _HAS_AER,
    }


def load_and_preprocess(
    n_samples: int = 60, n_components: int = 2, test_size: float = 0.3, random_state: int = 42
) -> Tuple[Any, Any, Any, Any]:
    """Carrega dataset e aplica PCA + split."""
    data = load_breast_cancer()
    X = data.data[:n_samples]
    y = data.target[:n_samples]
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X_pca, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test


def train_classic(X_train: Any, y_train: Any, X_test: Any, y_test: Any) -> Tuple[Any, float, float]:
    """Treina um SVM linear e retorna (modelo, acurácia, tempo)."""
    start = time.time()
    model = SVC(kernel="linear")
    model.fit(X_train, y_train)
    duration = time.time() - start
    acc = accuracy_score(y_test, model.predict(X_test))
    return model, acc, duration


def create_optimizer(
    optimizer_name: str, optimizer_options: Optional[Dict[str, Any]] = None
) -> Tuple[Optional[Any], Optional[Exception]]:
    """Cria e retorna um otimizador do Qiskit Algorithms pelo nome."""
    try:
        qalg = importlib.import_module("qiskit_algorithms.optimizers")
    except Exception as e:
        return None, e

    name_norm = optimizer_name.strip().upper()
    optimizer_class = getattr(qalg, name_norm, None)
    if optimizer_class is None:
        return None, ValueError(f"Otimizador nao encontrado: {optimizer_name}")

    options = optimizer_options or {}
    try:
        return optimizer_class(**options), None
    except Exception as e:
        return None, e


def create_vqc(
    X_train: Any,
    maxiter: int = 100,
    optimizer_name: str = "COBYLA",
    optimizer_options: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[Any], Optional[Exception]]:
    """Cria uma instância do VQC (não treinada). Retorna (modelo, erro)."""
    try:
        qclib = importlib.import_module("qiskit.circuit.library")
        ZZFeatureMap = getattr(qclib, "ZZFeatureMap")
        RealAmplitudes = getattr(qclib, "RealAmplitudes")
        qml = importlib.import_module("qiskit_machine_learning.algorithms")
        VQC = getattr(qml, "VQC")
    except Exception as e:
        return None, e

    primitives = get_qiskit_primitives()
    Sampler = primitives["Sampler"]
    QuantumInstance = primitives["QuantumInstance"]
    AerSimulator = primitives["AerSimulator"]
    _HAS_SAMPLER_PRIMITIVE = primitives["_HAS_SAMPLER_PRIMITIVE"]
    _HAS_AER = primitives["_HAS_AER"]

    num_features = X_train.shape[1]
    feature_map = ZZFeatureMap(feature_dimension=num_features, reps=1)
    ansatz = RealAmplitudes(num_qubits=num_features, reps=1)
    optimizer_params = {"maxiter": maxiter}
    if optimizer_options:
        optimizer_params.update(optimizer_options)

    optimizer, opt_err = create_optimizer(optimizer_name, optimizer_params)
    if optimizer is None:
        return None, opt_err
    vqc_kwargs = dict(feature_map=feature_map, ansatz=ansatz, optimizer=optimizer)

    # Tentar configurar um `sampler` (primitive novo) quando disponível
    if _HAS_SAMPLER_PRIMITIVE and Sampler is not None:
        try:
            sampler = Sampler()
            vqc_kwargs["sampler"] = sampler
        except Exception:
            try:
                primitives_mod = importlib.import_module("qiskit.primitives")
                BackendSampler = getattr(primitives_mod, "BackendSampler", None)
                if _HAS_AER and BackendSampler is not None:
                    backend = AerSimulator()
                    sampler = BackendSampler(backend=backend)
                    vqc_kwargs["sampler"] = sampler
            except Exception:
                pass

    # Algumas versões antigas do VQC esperam `quantum_instance` em vez de `sampler`
    try:
        sig = signature(VQC.__init__)
        params = sig.parameters
    except Exception:
        params = {}

    if "quantum_instance" in params and "quantum_instance" not in vqc_kwargs:
        if _HAS_AER and QuantumInstance is not None:
            try:
                qi = QuantumInstance(AerSimulator())
                vqc_kwargs["quantum_instance"] = qi
            except Exception:
                pass

    try:
        model_q = VQC(**vqc_kwargs)
        return model_q, None
    except Exception as e:
        return None, e


def train_quantum(
    X_train: Any,
    y_train: Any,
    X_test: Any,
    y_test: Any,
    maxiter: int = 30,
    optimizer_name: str = "SPSA",
    optimizer_options: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[Any], Optional[float], Optional[float], Optional[Exception]]:
    """Cria o VQC e treina; retorna (modelo, acurácia, tempo, erro)."""
    model_q, creation_err = create_vqc(
        X_train,
        maxiter=maxiter,
        optimizer_name=optimizer_name,
        optimizer_options=optimizer_options,
    )
    if model_q is None:
        return None, None, None, creation_err

    try:
        start = time.time()
        model_q.fit(X_train, y_train)
        duration_q = time.time() - start
        acc_q = accuracy_score(y_test, model_q.predict(X_test))
        return model_q, acc_q, duration_q, None
    except Exception as e:
        return None, None, None, e


def print_results(
    acc_classic: float,
    time_classic: float,
    acc_quantum: Optional[float],
    time_quantum: Optional[float],
    maxiter: int,
    optimizer_name: str,
    quantum_error: Optional[Exception] = None,
) -> None:
    print("## PARAMETROS")
    print(f" - Maxiter: {maxiter}")
    print(f" - Otimizador: {optimizer_name}\n")
    print("## RESULTADOS DA FASE 1")
    print("Modelo Clássico (SVM):")
    print(f" - Acurácia: {acc_classic * 100:.2f}%")
    print(f" - Tempo de treino: {time_classic:.4f} segundos\n")
    print("Modelo Quântico (VQC Simulado):")
    if acc_quantum is None:
        print(" - Acurácia: N/A (VQC não executado)")
        print(" - Tempo de treino: N/A")
        if quantum_error is not None:
            print("Aviso: não foi possível executar o VQC (compatibilidade/execução).")
            print("Erro:", quantum_error)
    else:
        print(f" - Acurácia: {acc_quantum * 100:.2f}%")
        print(f" - Tempo de treino: {time_quantum:.4f} segundos")


def main(n_samples: int = 60, n_components: int = 2) -> None:
    optimizer_name = "SPSA"
    optimizer_options: Dict[str, Any] = {"maxiter": 30}
    maxiter = optimizer_options.get("maxiter", 30)
    X_train, X_test, y_train, y_test = load_and_preprocess(
        n_samples=n_samples, n_components=n_components
    )
    _, acc_classic, time_classic = train_classic(X_train, y_train, X_test, y_test)
    _, acc_quantum, time_quantum, q_err = train_quantum(
        X_train,
        y_train,
        X_test,
        y_test,
        maxiter=maxiter,
        optimizer_name=optimizer_name,
        optimizer_options=optimizer_options,
    )
    print_results(
        acc_classic,
        time_classic,
        acc_quantum,
        time_quantum,
        maxiter,
        optimizer_name,
        q_err,
    )


if __name__ == "__main__":
    main()
