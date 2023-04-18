# streamlit_app.py

import pandas as pd
import streamlit as st
import random

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

def creation_sommaire(df):
    sommaire = {}
    for i, row in df.iterrows():
        start = i
        nom_chap = row.Chapitre
        if nom_chap not in sommaire:
            sommaire[nom_chap] = [start, start]
        else: 
            sommaire[nom_chap][1] = i
    return sommaire
df = load_data(st.secrets["public_gsheets_url"])
df.index = df.index.astype(int)
sommaire = creation_sommaire(df)
st.markdown(f"# Réglages")
chap_courant = st.selectbox('Choisir le chap actuel', (k for k in sommaire.keys()))
#st.write(chap_courant)
#st.write(sommaire[chap_courant][1])
st.markdown(f"Ce chapitre contient {sommaire[chap_courant][1]} questions")
question_chap_courant_max = st.slider('Progression dans le chapitre', 0, sommaire[chap_courant][1],1)
nb_question_courant = st.number_input('Nombre de questions à poser sur le chapitre actuel',min_value = 1,max_value=question_chap_courant_max,value=1)
nb_question = st.number_input('Nombre de questions sur le passé',min_value = 1,max_value=question_chap_courant_max,value=1)

st.markdown("## Roulette de questions actuelles")
# Calcul des index des questions corrspondant au début et fin du chapitre sélectionné
start_index = sommaire[chap_courant][0]
end_index = sommaire[chap_courant][1]
#st.write(start_index)
#st.write(end_index)
# Extraction des nb_question_courant
random_indexes_courant = random.sample(range(start_index,end_index), nb_question_courant)
resultat_courant = df.iloc[random_indexes_courant]
# Extraction des nb_question
random_indexes = random.sample(range(0,end_index), nb_question)
resultat = df.iloc[random_indexes]

#for index, row in df.loc[start_index: end_index].iterrows():
for row in resultat_courant.itertuples():
    st.markdown(f"{row.Question}")
#    st.markdown(f" {row['Question']} ")


st.markdown("## Roulette de questions sur les chapitres passés")


for row in resultat.itertuples():
    st.markdown(f"{row.Question}")

saut_page = ""
for i in range(30):
    saut_page+= "\n"
st.write(saut_page)

#sauvegarde dans la session des df resultat_courant et resultat
# ainsi la page correction.py peut récupérer les dataframe et afficher les questions/réponses
st.session_state['resultat_courant']=resultat_courant
st.session_state['resultat']=resultat
#    print(row)
