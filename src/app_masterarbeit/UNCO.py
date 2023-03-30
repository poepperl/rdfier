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

if "data_state" not in st.session_state:
    st.session_state.data_state = (0,0,0,0,0)

if "path" not in st.session_state:
    st.session_state.path = None

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
    st.session_state.data_state = (0,0,0,0,0)
    st.session_state.path = None
    st.session_state.generator = None

if st.session_state.rdfdata is not None:

    dataframe = st.experimental_data_editor(st.session_state.dataframe)

    if not dataframe.equals(st.session_state.dataframe):
        st.session_state.rdfdata = RDFData(dataframe.copy())
        st.session_state.dataframe = dataframe
        st.session_state.data_state = (0,0,0,0,0)

    with st.container():
        col1, col2 = st.columns(2)

        xml_format = col1.radio("RDF Format", ("Turtle", "XML"))

        graphical_version = col2.checkbox("Graph anzeigen lassen")

    with st.expander("Generiere Unsicherheiten"):
        checkcol1, checkcol2, checkcol3 = st.columns(3)
        solution = checkcol1.selectbox("Modellierung auswählen:", (1,2,3,4,5,6,7,8))
        numb_uncertain_values = checkcol3.number_input("Anzahl unsicherer Werte pro Spalte:", min_value=0, max_value=len(st.session_state.rdfdata.data), step=1)

        manuel = st.checkbox("Spalten manuell auswählen", key="disabled")
        numb_uncertain_columns = checkcol2.number_input("Anzahl unsicherer Spalten:", min_value=0, max_value=len(list(st.session_state.rdfdata.data.columns))-1, step=1, disabled=manuel)

        options = []
        if manuel:
            options = st.multiselect(
            'Wähle die Subjektspalten aus, in denen Unsicherheit generiert werden soll:',
            list(st.session_state.rdfdata.data.columns)[1:])

    uploaded_prefixes = st.file_uploader("Prefixtabelle", type=["csv"], accept_multiple_files=False)

    # Graph generieren-------------------------------------------------------------------------------

    generate = st.button("RDF Graph generieren")

    if generate:
        st.session_state.generate = True
        st.session_state.data_state = (0,0,0,0,0)

    if st.session_state.generate:
        if (xml_format, solution, numb_uncertain_values, numb_uncertain_columns, options) != st.session_state.data_state:
            st.session_state.data_state = (xml_format, solution, numb_uncertain_values, numb_uncertain_columns, options)
            if numb_uncertain_values != 0:
                u_generator = UncertaintyGenerator(st.session_state.rdfdata)
                options = [rdf_data.data.columns.get_loc(c) for c in options if c in st.session_state.rdfdata.data]

                rdf_data = u_generator.add_uncertainty_flags(number_of_uncertain_columns=numb_uncertain_columns, list_of_columns=options, uncertainties_per_column=numb_uncertain_values)
                filename = "graph_model_" + str(solution)
            
            else:
                rdf_data = st.session_state.rdfdata
                filename = "graph"

            st.session_state.generator = GraphGenerator(rdf_data)
            st.session_state.generator.load_prefixes(pd.read_csv(uploaded_prefixes))
            st.session_state.generator.generate_solution(solution if numb_uncertain_values != 0 else 0, xml_format=(xml_format=="XML"))

            if xml_format=="XML":
                st.session_state.path = Path(UNCO_PATH, "data/output/" + filename + ".rdf")
            else:
                st.session_state.path = Path(UNCO_PATH, "data/output/" + filename + ".ttl")


        if graphical_version:
            codcol, graphcol = st.columns(2)

            codcol.code(st.session_state.path.read_text())

            grapher = Grapher(st.session_state.path)
            
            image = Image.open(str(Path(UNCO_PATH, "data/output/downloaded_graph.png")))

            graphcol.image(image, output_format="PNG", use_column_width="auto")
        else:
            st.code(st.session_state.path.read_text())

        # SPARQL-----------------------------------------------------------------------------------------

        sparql = st.checkbox("SPARQL-Schnittstelle")

        if sparql:
            sparql_prefixes = "".join(("PREFIX " + prefix + ": <" + st.session_state.generator.prefixes[prefix] + ">" + "\n" for prefix in st.session_state.generator.prefixes))

            qcol1, qcol2 = st.columns(2)

            query_input = qcol2.file_uploader("Query hochladen:", type=["txt", "rq"], accept_multiple_files=False)

            if query_input:
                querytext = query_input.getvalue().decode("utf-8")
                query = qcol1.text_area("Query eingeben:", querytext)
            else:
                query = qcol1.text_area("Query eingeben:", sparql_prefixes + """\n\nSELECT ?su ?p ?o\nWHERE {\n    ?su ?p ?o\n}""")

            start_query = st.button("Query ausführen")

            if start_query:
                st.dataframe(st.session_state.generator.run_query(query))