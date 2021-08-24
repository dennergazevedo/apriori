import streamlit as st
import pandas as pd
from apriori import runApriori, dataFromFile, to_str_results

st.markdown("# Apriori Streamlit")

default_csv = st.selectbox(
    "Selecione uma base de dados:", ("resumida.csv", "completa.csv")
)

st.markdown('Linhas de amostra do conjunto de dados')
csv_file = pd.read_csv(default_csv, header=None, sep="\n")
st.write(csv_file[0].str.split("\,", expand=True).head())

st.markdown('---')
st.markdown("## Inputs")

st.markdown('A base de dados completa leva alguns minutos para atualizar.')

support_helper = ''' > Suporte(A) = (Número de vezes que A aparece)/(Total de resultados') '''
confidence_helper = ''' > Confiança(A->B) = Suporte(AUB)/Suporte(A)') '''
st.markdown('---')

support = st.slider("Suporte Mínimo:", min_value=0.1,
                    max_value=0.9, value=0.15,
                    help=support_helper)

confidence = st.slider("Confiança Mínima:", min_value=0.1,
                       max_value=0.9, value=0.6, help=confidence_helper)

inFile = dataFromFile(default_csv)

items, rules = runApriori(inFile, support, confidence)

i, r = to_str_results(items, rules)

st.markdown("## Resultados")

st.markdown("### Itens frequentes")
st.write(i)

st.markdown("### Regras frquentes")
st.write(r)
