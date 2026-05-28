# quantum-workspace

Pequeno repositório de exemplo que compara um classificador clássico (SVM) com
um classificador variacional quântico (VQC) usando o dataset "breast cancer"
do scikit-learn e PCA para redução de dimensionalidade.

## Dependências

Instale as dependências listadas em `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Execução

Rode o script principal:

```bash
python3 script.py
```

Observação: o VQC (Qiskit) é usado quando disponível; se o Qiskit não estiver
instalado ou compatível, o script executa apenas o classificador clássico.
