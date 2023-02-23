import streamlit as st
import pandas as pd
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
        checkcol1, checkcol2 = st.columns(2)
        numb_uncertain_columns = checkcol1.number_input("Anzahl unsicherer Spalten:", min_value=0, max_value=len(list(dataset.data.columns)), step=1, disabled=st.session_state.disabled)
        numb_uncertain_values = checkcol2.number_input("Anzahl unsicherer Werte pro Spalte:", min_value=0, max_value=len(dataset.data), step=1)

        manuel = st.checkbox("Spalten manuell auswählen", key="disabled")
        options = []
        if manuel:
            options = st.multiselect(
            'What are your favorite colors',
            list(dataset.data.columns))
        
    generate = st.button("RDF Graph generieren")

    if generate:
        if options:
            dataset.add_uncertainty_flags(list_of_columns=[dataset.data.columns.get_loc(c) for c in options if c in dataset.data])
        elif numb_uncertain_columns != 0 and numb_uncertain_values != 0:
            dataset.add_uncertainty_flags(number_of_uncertain_columns=numb_uncertain_columns, uncertainties_per_column=numb_uncertain_values)
        
        generator = RDFGenerator(dataset)
        generator.load_prefixes(r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\1certain2uncertainMints\namespaces.csv")
        generator.generate_solution(7)

        if graphical_version:
            codcol, graphcol = st.columns(2)

            codcol.code(Path(r"D:\Dokumente\Repositories\unco\data\output\graph_model_7.rdf").read_text())

            grapher = Grapher(Path(r"D:\Dokumente\Repositories\unco\data\output\graph_model_7.rdf"))
            
            image = Image.open(r"D:\Dokumente\Repositories\unco\data\output\downloaded_graph.png")

            graphcol.image(image, output_format="PNG",use_column_width="auto")