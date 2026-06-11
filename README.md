# quantum-workspace

Pequeno repositório de exemplo que compara um classificador clássico (SVM) com
um classificador variacional quântico (VQC) usando o dataset "breast cancer"
do scikit-learn e PCA para redução de dimensionalidade.

O estado atual corresponde à Fase 1 da IC: estabilizar o baseline VQC antes de
partir para a formulação QUBO/QAOA. A configuração padrão usa 100 amostras
estratificadas, PCA com 2 componentes, escala `0..1`, SPSA e `maxiter=100`.

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

## Otimizador do VQC

O otimizador do VQC pode ser configurado diretamente no `main()` do script
principal, usando as variaveis padrão:

```python
DEFAULT_OPTIMIZER = "SPSA"
DEFAULT_MAXITER = 100
DEFAULT_N_SAMPLES = 100
DEFAULT_N_COMPONENTS = 2
```

Troque `optimizer_name` para `COBYLA`, `SPSA`, `ADAM`, etc., e ajuste
`optimizer_options` conforme os parametros aceitos pelo otimizador.

Observação: o VQC (Qiskit) é usado quando disponível; se o Qiskit não estiver
instalado ou compatível, o script executa apenas o classificador clássico.
