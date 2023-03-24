import streamlit as st
import pandas as pd
from unco import UNCO_PATH
from unco.data.rdf_data import RDFData
from unco.features.graph_generator import GraphGenerator
from unco.features.grapher import Grapher
from unco.features.fuseki import FusekiServer
from pathlib import Path
from PIL import Image

st.set_page_config(
    page_title="Uncertainty Comparator",
    layout="wide")


if "rdfdata" not in st.session_state:
    st.session_state["rdfdata"] = pd.DataFrame()

if "solution" not in st.session_state:
    st.session_state["solution"] = 0

# Begin webpage---------------------------------------------------------------------------

st.title('Uncertainty Comparator')

uploaded_file = st.file_uploader("Upload", type=["csv"], accept_multiple_files=False)

if uploaded_file:
    st.session_state["rdfdata"] = pd.read_csv(uploaded_file)
    rdfdata = RDFData(st.session_state["rdfdata"])

st.dataframe(st.session_state["rdfdata"], 1500, 400)

with st.container():
    col1, col2 = st.columns(2)

    xml_format = col1.radio("RDF Format", ("Turtle", "XML"))

    graphical_version = col2.checkbox("Graph anzeigen lassen")

with st.expander("Unsicherheiten"):
    checkcol1, checkcol2, checkcol3 = st.columns(3)
    st.session_state.solution = checkcol1.selectbox("Modellierung auswählen:", (1,2,3,4,5,6,7,8))
    numb_uncertain_columns = checkcol2.number_input("Anzahl unsicherer Spalten:", min_value=0, max_value=len(list(rdfdata.data.columns))-1, step=1, disabled=st.session_state.disabled)
    numb_uncertain_values = checkcol3.number_input("Anzahl unsicherer Werte pro Spalte:", min_value=0, max_value=len(rdfdata.data), step=1)

    manuel = st.checkbox("Spalten manuell auswählen", key="disabled")
    options = []
    if manuel:
        options = st.multiselect(
        'Wähle die Subjektspalten aus, in denen Unsicherheit generiert werden soll:',
        list(rdfdata.data.columns)[1:])

uploaded_prefixes = st.file_uploader("Prefixtabelle", type=["csv"], accept_multiple_files=False)

# Graph generieren-------------------------------------------------------------------------------

st.button("RDF Graph generieren")

if graphical_version:
    codcol, graphcol = st.columns(2)

    codcol.code()

    grapher = Grapher()
    
    image = Image.open(str(Path(UNCO_PATH, "data/output/downloaded_graph.png")))

    graphcol.image(image, output_format="PNG",use_column_width="auto")
else:
    st.code()

# SPARQL-----------------------------------------------------------------------------------------

sparql_prefixes = open(Path(UNCO_PATH, "data/output/" + "_prefixes.txt")).read()

qcol1, qcol2 = st.columns(2)

query_input = qcol2.file_uploader("Query hochladen:", type=["txt", "rq"], accept_multiple_files=False)

if query_input:
    querytext = query_input.getvalue().decode("utf-8")
    query = qcol1.text_area("Query eingeben:", querytext)
else:
    query = qcol1.text_area("Query eingeben:", sparql_prefixes + """\n\nSELECT ?su ?p ?o\nWHERE {\n    ?su ?p ?o\n}""")

start_query = st.button("Query ausführen")

st.code()