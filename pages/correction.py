import pandas as pd
import streamlit as st
import random
resultat_courant= st.session_state['resultat_courant']
resultat= st.session_state['resultat']
st.markdown(f"# Correction des questions du présent")
for row in resultat_courant.itertuples():
    st.markdown(f"{row.Question}  ")
    st.markdown(f"- *{row.Answer}*")

st.markdown(f"# Correction des questions du passé")
for row in resultat.itertuples():
    st.markdown(f"{row.Question}  ")
    st.markdown(f"- *{row.Answer}*")