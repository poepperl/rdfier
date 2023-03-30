import streamlit as st
import pandas as pd
from unco import UNCO_PATH
from unco.data.rdf_data import RDFData
from unco.data.uncertainty_generator import UncertaintyGenerator
from unco.features.graph_generator import GraphGenerator
from unco.features.grapher import Grapher
from unco.features.fuseki import FusekiServer
from pathlib import Path
from PIL import Image

st.set_page_config(
    page_title="Uncertainty Comparator",
    layout="wide")

if "rdfdata" not in st.session_state:
    st.session_state.rdfdata = None

if "generate" not in st.session_state:
    st.session_state.generate = False

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

if "turtle" not in st.session_state:
    st.session_state.turtle = None

if "generator" not in st.session_state:
    st.session_state.generator = None

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None

# Begin webpage---------------------------------------------------------------------------

st.title('Uncertainty Comparator')

uploaded_file = st.file_uploader("Upload", type=["csv"], accept_multiple_files=False)

if uploaded_file and not st.session_state.uploaded:
    st.session_state.dataframe = pd.read_csv(uploaded_file)
    st.session_state.rdfdata = RDFData(st.session_state.dataframe.copy())
    st.session_state.uploaded = True

elif st.session_state.uploaded and not uploaded_file:
    st.session_state.uploaded = False
    st.session_state.generate = False
    st.session_state.rdfdata = None
    st.session_state.turtle = None
    st.session_state.generator = None

if st.session_state.rdfdata is not None:

    dataframe = st.experimental_data_editor(st.session_state.dataframe)
    
    if not dataframe.equals(st.session_state.dataframe):
        st.session_state.rdfdata = RDFData(dataframe.copy())
        st.session_state.dataframe = dataframe
        st.session_state.turtle = None

    with st.container():
        col1, col2 = st.columns(2)

        xml_format = col1.radio("RDF Format", ("Turtle", "XML"))

        graphical_version = col2.checkbox("Graph anzeigen lassen")

    uploaded_prefixes = st.file_uploader("Prefixtabelle", type=["csv"], accept_multiple_files=False)

    # Graph generieren-------------------------------------------------------------------------------

    generate = st.button("RDF Graph generieren")

    if generate:
        st.session_state.generate = True
        st.session_state.data_state = (0,0,0,0,0)

    if st.session_state.generate:
        if (xml_format == "Turtle") != st.session_state.turtle:
            st.session_state.data_state = (xml_format == "Turtle")
            rdf_data = st.session_state.rdfdata

            st.session_state.generator = GraphGenerator(rdf_data)
            st.session_state.generator.load_prefixes(pd.read_csv(uploaded_prefixes))
            st.session_state.generator.generate_solution(xml_format=(xml_format=="XML"))

        
        path = Path(UNCO_PATH, "data/output/graph" + (".ttl" if xml_format=="Turtle" else ".rdf"))

        if graphical_version:
            codcol, graphcol = st.columns(2)

            codcol.code(path.read_text())

            grapher = Grapher(path)
            
            image = Image.open(str(Path(UNCO_PATH, "data/output/downloaded_graph.png")))

            graphcol.image(image, output_format="PNG", use_column_width="auto")
        else:
            st.code(path.read_text())