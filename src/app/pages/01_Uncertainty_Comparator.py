import streamlit as st
import pandas as pd
from unco import UNCO_PATH
from unco.data.rdf_data import RDFData
from unco.features.rdf_generator import RDFGenerator
from unco.features.grapher import Grapher
from unco.features.fuseki import FusekiServer
from pathlib import Path
from PIL import Image

st.set_page_config(
    page_title="RDF Grapher",
    layout="wide")

# Set session states--------------------------------------------------------------------

if "disabled" not in st.session_state:
    st.session_state.disabled = False

if "generated" not in st.session_state:
    st.session_state.generated = False

if "filename" not in st.session_state:
    st.session_state.filename = ""

if "solution" not in st.session_state:
    st.session_state.solution = 0

if "fuseki" not in st.session_state:
    st.session_state.fuseki = False

if "path" not in st.session_state:
    st.session_state.path = ""

if "server" not in st.session_state:
    st.session_state.server = FusekiServer()

def generate():
    st.session_state.filename = "graph_model_"
    if options:
        dataset.add_uncertainty_flags(list_of_columns=[dataset.data.columns.get_loc(c) for c in options if c in dataset.data])
        st.session_state.filename += str(st.session_state.solution)
    elif numb_uncertain_columns != 0 and numb_uncertain_values != 0:
        dataset.add_uncertainty_flags(number_of_uncertain_columns=numb_uncertain_columns, uncertainties_per_column=numb_uncertain_values)
        st.session_state.filename += str(st.session_state.solution)
    else:
        st.session_state.solution = None
        st.session_state.filename = "graph"
    
    generator = RDFGenerator(dataset)
    generator.load_prefixes(pd.read_csv(uploaded_prefixes))
    generator.generate_solution(st.session_state.solution, xml_format=(xml_format=="XML"))

    if xml_format=="XML":
        st.session_state.path = Path(UNCO_PATH, "data/output/" + st.session_state.filename + ".rdf")
    else:
        st.session_state.path = Path(UNCO_PATH, "data/output/" + st.session_state.filename + ".ttl")
    st.session_state.generated = True

def start_stop_fuseki():
    if st.session_state.fuseki:
        st.session_state.server.stop_server()
        st.session_state.fuseki = False
    else:
        st.session_state.server.start_server()
        st.session_state.server.upload_data(str(st.session_state.path))
        st.session_state.fuseki = True

# Begin webpage---------------------------------------------------------------------------

st.title('Uncertainty Comparator')

uploaded_file = st.file_uploader("Upload", type=["csv"], accept_multiple_files=False)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df, 1500, 400)
    dataset = RDFData(df)

    with st.container():
        "Parameter:"
        col1, col2 = st.columns(2)

        xml_format = col1.radio("RDF Format", ("Turtle", "XML"))

        graphical_version = col2.checkbox("Graph anzeigen lassen")

    with st.expander("Unsicherheiten"):
        checkcol1, checkcol2, checkcol3 = st.columns(3)
        st.session_state.solution = checkcol1.selectbox("Modellierung auswählen:", (1,2,3,4,5,6,7,8))
        numb_uncertain_columns = checkcol2.number_input("Anzahl unsicherer Spalten:", min_value=0, max_value=len(list(dataset.data.columns))-1, step=1, disabled=st.session_state.disabled)
        numb_uncertain_values = checkcol3.number_input("Anzahl unsicherer Werte pro Spalte:", min_value=0, max_value=len(dataset.data), step=1)

        manuel = st.checkbox("Spalten manuell auswählen", key="disabled")
        options = []
        if manuel:
            options = st.multiselect(
            'Wähle die Subjektspalten aus, in denen Unsicherheit generiert werden soll:',
            list(dataset.data.columns)[1:])
    
    uploaded_prefixes = st.file_uploader("Prefixtabelle", type=["csv"], accept_multiple_files=False)

    # Graph generieren-------------------------------------------------------------------------------

    st.button("RDF Graph generieren", on_click=generate)

    if st.session_state.generated and uploaded_prefixes:

        if graphical_version:
            codcol, graphcol = st.columns(2)

            codcol.code(st.session_state.path.read_text())

            grapher = Grapher(st.session_state.path)
            
            image = Image.open(str(Path(UNCO_PATH, "data/output/downloaded_graph.png")))

            graphcol.image(image, output_format="PNG",use_column_width="auto")
        else:
            st.code(st.session_state.path.read_text())
        
        # Fusekianbindung-------------------------------------------------------------------------------

        start_fuseki = st.button("Start/Stop Fusekiserver", on_click=start_stop_fuseki)

        sparql_prefixes = open(Path(UNCO_PATH, "data/output/" + st.session_state.filename + "_prefixes.txt")).read()

        if st.session_state.fuseki:
            qcol1, qcol2 = st.columns(2)
            
            query_input = qcol2.file_uploader("Query hochladen:", type=["txt", "rq"], accept_multiple_files=False)

            if query_input:
                querytext = query_input.getvalue().decode("utf-8")
                query = qcol1.text_area("Query eingeben:", querytext)
            else:
                query = qcol1.text_area("Query eingeben:", sparql_prefixes + """\n\nSELECT ?su ?p ?o\nWHERE {\n    ?su ?p ?o\n}""")

            start_query = st.button("Query ausführen")
            if start_query:
                st.code(st.session_state.server.sparql_query(query))