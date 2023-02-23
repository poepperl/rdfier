import streamlit as st
import pandas as pd
from unco import UNCO_PATH
from unco.data.dataset import Dataset
from unco.features.rdf_generator import RDFGenerator
from unco.features.grapher import Grapher
from pathlib import Path
from PIL import Image

st.set_page_config(
    page_title="RDF Grapher",
    layout="wide")

st.title('RDF Grapher')

uploaded_file = st.file_uploader("Upload", type=["csv"], accept_multiple_files=False)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df, 1500, 400)
    dataset = Dataset(df)

    with st.container():
        "Parameter:"
        col1, col2 = st.columns(2)

        xml_format = col1.radio("RDF Format", ("XML", "Turtle"))

        graphical_version = col2.checkbox("Graph anzeigen lassen")

    with st.expander("Unsicherheiten"):
        if "disabled" not in st.session_state:
            st.session_state.disabled = False
        checkcol1, checkcol2, checkcol3 = st.columns(3)
        solution = checkcol1.selectbox("Modellierung auswählen:", (1,2,3,4,5,6,7,8))
        numb_uncertain_columns = checkcol2.number_input("Anzahl unsicherer Spalten:", min_value=0, max_value=len(list(dataset.data.columns)), step=1, disabled=st.session_state.disabled)
        numb_uncertain_values = checkcol3.number_input("Anzahl unsicherer Werte pro Spalte:", min_value=0, max_value=len(dataset.data), step=1)

        manuel = st.checkbox("Spalten manuell auswählen", key="disabled")
        options = []
        if manuel:
            options = st.multiselect(
            'What are your favorite colors',
            list(dataset.data.columns))
    
    uploaded_prefixes = st.file_uploader("Prefixtabelle", type=["csv"], accept_multiple_files=False)

    generate = st.button("RDF Graph generieren")

    if generate:
        filename = "graph_model_"
        if options:
            dataset.add_uncertainty_flags(list_of_columns=[dataset.data.columns.get_loc(c) for c in options if c in dataset.data])
            filename += str(solution)
        elif numb_uncertain_columns != 0 and numb_uncertain_values != 0:
            dataset.add_uncertainty_flags(number_of_uncertain_columns=numb_uncertain_columns, uncertainties_per_column=numb_uncertain_values)
            filename += str(solution)
        else:
            solution = None
            filename = "graph"
        
        generator = RDFGenerator(dataset)
        generator.load_prefixes(pd.read_csv(uploaded_prefixes))
        generator.generate_solution(solution, xml_format=(xml_format=="XML"))

        if xml_format=="XML":
            path = Path(UNCO_PATH, "data/output/" + filename + ".rdf")
        else:
            format = ".ttl"
            path = Path(UNCO_PATH, "data/output/" + filename + ".ttl")

        if graphical_version:
            codcol, graphcol = st.columns(2)

            codcol.code(path.read_text())

            grapher = Grapher(path)
            
            image = Image.open(str(Path(UNCO_PATH, "data/output/downloaded_graph.png")))

            graphcol.image(image, output_format="PNG",use_column_width="auto")