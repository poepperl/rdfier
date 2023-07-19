import streamlit as st

st.set_page_config(
    page_title="How it works",
    layout="wide")

st.title('About RDFier')

st.write(
    f"""
    This module was developed as part of Luca Pöpperl's master's thesis in order to investigate different models for uncertainty
    in RDF graphs and to perform benchmark tests with them.
    This web application provides a simple way to convert CSV data into RDF graphs using a mapping syntax,
    which is described in more detail on the [📝Input Format](http://localhost:8501/Input_Format) page.

    On the [Home](http://localhost:8501) page, custom csv tables can be entered and the resulting graph displayed.
    After a csv file has been uploaded, further configurations can be made:
    - First, the entered csv table is displayed. All fields of the table can be edited, and by clicking on a column header,
    the respective columns can be sorted.
    - In the area "RDF Format" the output format (Turtle or XML) can be selected.
    - By deactivating "Show graph figure", the graph is only output in a text field in the selected format.
    By default, a graphical representation is also generated for inputs with less than 30 rows.
    - Also, the uncertainty model can be selected. The numbering of the models is equivalent to the numbering in the master thesis.
    - By uploading a prefix table, prefixes, which are contained in the input, can be linked to the desired namespaces.
    These must be entered in csv format, which expects a table with the columns (prefix,namespace).

    Now the RDF graph can be generated. Once a graph has been generated, all of the above configurations can be adjusted "live",
    so that the effects on the graph can be seen.
    """
)