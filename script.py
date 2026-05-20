import time
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Bibliotecas do Qiskit
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit_algorithms.optimizers import COBYLA
from qiskit_machine_learning.algorithms import VQC
from qiskit.primitives import Sampler

# 1. Dados (Drasticamente reduzidos para não travar sua CPU)
data = load_breast_cancer()
X = data.data[:60]  # Pegando apenas 60 amostras
y = data.target[:60]

# PCA para reduzir a apenas 2 variáveis (features)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.3, random_state=42)

# 2. Modelo Clássico (Baseline para comparação)
inicio_classico = time.time()
modelo_classico = SVC(kernel='linear')
modelo_classico.fit(X_train, y_train)
tempo_classico = time.time() - inicio_classico

acc_classico = accuracy_score(y_test, modelo_classico.predict(X_test))

# 3. Modelo Quântico (Simulado)
# Usamos o VQC (Classificador Quântico Variacional). 
# Na próxima etapa da IC, você substituirá o 'ansatz' padrão pela formulação exata do QAOA.
num_features = X_train.shape[1]
feature_map = ZZFeatureMap(feature_dimension=num_features, reps=1)
ansatz = RealAmplitudes(num_qubits=num_features, reps=1) # Onde o QAOA vai entrar depois
otimizador = COBYLA(maxiter=30) # Apenas 30 iterações para rodar rápido
sampler = Sampler()

modelo_quantico = VQC(
    sampler=sampler,
    feature_map=feature_map,
    ansatz=ansatz,
    optimizer=otimizador
)

inicio_quantico = time.time()
modelo_quantico.fit(X_train, y_train)
tempo_quantico = time.time() - inicio_quantico

acc_quantico = accuracy_score(y_test, modelo_quantico.predict(X_test))

# 4. Saída para a sua Tabela da Reunião
print("\n" + "="*30)
print("RESULTADOS DO TESTE INICIAL")
print("="*30)
print(f"Modelo Clássico (SVM):")
print(f" - Acurácia: {acc_classico*100:.2f}%")
print(f" - Tempo de treino: {tempo_classico:.4f} segundos\n")
print(f"Modelo Quântico (VQC Simulado):")
print(f" - Acurácia: {acc_quantico*100:.2f}%")
print(f" - Tempo de treino: {tempo_quantico:.4f} segundos")