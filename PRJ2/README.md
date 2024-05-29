# Instruções para Execução do Projeto (second delivery)

## Estrutura do Projeto

## Descrição dos Ficheiros 

- `cleanup.py`: Script para limpeza do dataset.
- `correlation.py`: Script para criar a matriz de correlação.
- `eda.py`: Script para Análise Exploratória dos Dados (EDA).
- `models.py`: Script com o código para treino de todos os modelos.

## Pré-requisitos

- `pandas`
- `numpy`
- `seaborn`
- `matplotlib`
- `scikit-learn`
- `imblearn`


```bash
pip3 install pandas numpy seaborn matplotlib scikit-learn imblearn
```


### Instruções para execução (EM ORDEM)

```bash
python3 cleanup.py
```


```bash
python3 models.py

```
#### Dados e Graphs

```bash
python correlation.py

```

```bash
python eda.py
```



