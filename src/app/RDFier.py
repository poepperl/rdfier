import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
from unco import UNCO_PATH
from unco.data.rdf_data import RDFData
from unco.features.grapher import Grapher
from unco.features.graph_generator import GraphGenerator

st.set_page_config(
    page_title="RDFier",
    layout="wide")

# if "rdfdata" not in st.session_state:
#     st.session_state.rdfdata = None

# if "generate" not in st.session_state:
#     st.session_state.generate = False

if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

# if "turtle" not in st.session_state:
#     st.session_state.turtle = None

# if "generator" not in st.session_state:
#     st.session_state.generator = None

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None

def update():
    st.session_state.rdfdata = RDFData(st.session_state.dataframe.copy())
    st.session_state.turtle = None

# Begin webpage---------------------------------------------------------------------------

st.title('RDFier')
st.subheader("A RDF Mapper")

uploaded_file = st.file_uploader("Upload", type=["csv"], accept_multiple_files=False)

if not uploaded_file:
    st.session_state.generate = False
    st.session_state.rdfdata = None
    st.session_state.turtle = None
    st.session_state.generator = None

else:
    st.session_state.dataframe = st.experimental_data_editor(pd.read_csv(uploaded_file), on_change=update)
    if st.session_state.rdfdata is None:
        update()

    with st.container():
        col1, col2 = st.columns(2)

        xml_format = col1.radio("RDF format", ("Turtle", "XML"))

        graphical_version = col2.checkbox("Show graphical version", value=True)

        solution = col2.selectbox("Select model:", (1,2,3,4,5,6,7,8))

    uploaded_prefixes = st.file_uploader("Prefixes", type=["csv"], accept_multiple_files=False)

    # Graph generieren-------------------------------------------------------------------------------

    generate = st.button("Generate RDF graph")

    if generate:
        st.session_state.generate = True
        st.session_state.turtle = None

    if st.session_state.generate:
        if (xml_format == "Turtle") != st.session_state.turtle:
            st.session_state.data_state = (xml_format == "Turtle")
            st.session_state.generator = GraphGenerator(st.session_state.rdfdata)
            st.session_state.generator.load_prefixes(pd.read_csv(uploaded_prefixes))
            st.session_state.generator.generate_solution(solution_id=solution,xml_format=(xml_format=="XML"))

        
        path = Path(UNCO_PATH, "data/output/graph" + (".ttl" if xml_format=="Turtle" else ".rdf"))

        if graphical_version:
            codcol, graphcol = st.columns(2)

            codcol.code(path.read_text())

            grapher = Grapher(path)
            
            image = Image.open(str(Path(UNCO_PATH, "data/output/downloaded_graph.png")))

            graphcol.image(image, output_format="PNG", use_column_width="auto")
        else:
            st.code(path.read_text())