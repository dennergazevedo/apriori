# Implementação Python do Algoritmo Apriori
Algoritmo usado para estudo de Data Mining, implementação de algoritmos rápidos para regras de associação de mineração. A base de dados utilizada foi disponibilizada pelo Governo do Brasil:
**Casos de Síndrome Respiratória Aguda Grave Hospitalizados**

## Streamlit App
Biblioteca utilizada para visualizar um aplicativo interativo ao vivo e com maior facilidade modificar os valores de entrada.
### Como usar:
Instale a biblioteca através do comando:
```
pip install streamlit
```

Após a instalação, você poderá executar o app acessando a pasta do projeto pelo seu terminal e executar o comando:
```
python -m streamlit run streamlit_app.py
```

## Como usar o Algoritmo
Você pode executar o programa com um conjunto de dados de sua preferência, para isso você precisa abrir a pasta do projeto no seu terminal e executar a linha de código abaixo:
```
python apriori.py -f SUA_BASE.csv -s 0.35 -c 0.75
```
**-s** representa o suporte mínimo
**-c** representa a confiança mínima

Para executar o programa com conjunto de dados fornecido e valores padrão basta executar:
```
python apriori.py -f SUA_BASE.csv
```
**Valores Padrão:** 
*Suporte Mínimo = 0,5* e *Confiança Mínima = 0,5*

Para melhores resultados tente os seguintes valores de suporte e confiança:
**Suporte**: entre 0,1 e 0,2
**Confiança**: entre 0,5 e 0,7