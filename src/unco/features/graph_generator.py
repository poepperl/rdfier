import pandas as pd
from fileinput import input
from random import random
from pathlib import Path
from unco import UNCO_PATH
from unco.data.rdf_data import RDFData
from rdflib import Graph, Namespace, BNode, Literal, URIRef, IdentifiedNode


# Standard Namespaces------------------------------------------------------------------------
CRM         = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
DCTERMS     = Namespace("http://purl.org/dc/terms/")
DCMITYPE    = Namespace("http://purl.org/dc/dcmitype/")
FOAF        = Namespace("http://xmlns.com/foaf/0.1/")
GEO         = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
NM          = Namespace("http://nomisma.org/id/")
NMO         = Namespace("http://nomisma.org/ontology#")
ORG         = Namespace("http://www.w3.org/ns/org#")
RDF         = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS        = Namespace("http://www.w3.org/2000/01/rdf-schema#")
SKOS        = Namespace("http://www.w3.org/2004/02/skos/core#")
XSD         = Namespace("http://www.w3.org/2001/XMLSchema#")

# Needed for uncertainty models:
AMT         = Namespace("http://academic-meta-tool.xyz/vocab#")
BMO         = Namespace("http://collection.britishmuseum.org/id/ontology/")
CRMINF      = Namespace("http://www.cidoc-crm.org/crminf/sites/default/files/CRMinf_v0.7_.rdfs#")
EDTFO       = Namespace("http://periodo.github.io/edtf-ontology/edtfo.ttl#")
UN          = Namespace("http://www.w3.org/2005/Incubator/urw3/XGR-urw3-20080331/Uncertainty.owl#")
# UNCO        = Namespace("localhost:8501/id/")


class GraphGenerator:
    """
        Class which creates an RDF-XML file.

    Attributes
    ----------
    rdfdata: RDFData
        RDFData which contains the data of the rdf graph.
    graph: Graph
        RDF graph which will be created.
    OUTPUT_FOLDER: Path
        Constant which holds the output path.
    prefixes: dict
        Dictionary which contains the prefixes and namespaces which binds to the graph.
    """

    def __init__(self, rdfdata: RDFData) -> None:
        """
        Parameters
        ----------
        rdfdata: RDFData
            Object which contains the data of the rdf graph.
        """
        self.rdfdata = rdfdata
        self.graph = Graph()
        self.OUTPUT_FOLDER = Path(UNCO_PATH, "data/output")
        self.prefixes: dict[str,Namespace] = {"crm": CRM, "dcterms": DCTERMS, "dcmitype": DCMITYPE, "foaf": FOAF, "geo": GEO,
                                               "nm": NM, "nmo": NMO, "org": ORG, "rdf": RDF, "rdfs": RDFS, "skos": SKOS,
                                               "xsd": XSD, "un": UN, "bmo": BMO, "edtfo": EDTFO, "crminf": CRMINF, "amt": AMT}

    def load_prefixes(self, path_data: str | pd.DataFrame) -> None:
        """
            Loads prefixes of namespaces and bind them to the graph.

        Parameters
        ----------
        path_data: str | DataFrame
            Path to the csv file with header: (prefix, namespace) or DataFrame of the file.
        """
        if type(path_data) == pd.DataFrame:
            namespaces = path_data
        else:
            namespaces = pd.read_csv(path_data)

        for rowindex in range(len(namespaces)):
            self.prefixes[str(namespaces.iloc[rowindex,0]).lower()] = Namespace(str(namespaces.iloc[rowindex,1]))

        for prefix in self.prefixes:
            self.graph.bind(prefix, self.prefixes[prefix])

        del namespaces

    def generate_solution(self, model_id: int = 4, xml_format: bool = True) -> None:
        """ 
            Generates and saves the RDF graph.

        Attributes
        ----------
        model_id: int
            Model ID, of the model which should be used to create the uncertain statements.
        xml_format: bool
            If True, the generated graph will be saved in data/output/graph.ttl in turtle format.
            Otherwise it will be saved in data/output/graph.rdf in xml format.
        """
        if model_id == 9 | 10 and xml_format:
            print("Warning: XML format is currently not aviable for rdf* models. The format will be changed to turtle.")
            xml_format = False
        if model_id == 5:
            crm_properties = self._get_crm_properties()

        self.graph = Graph()
        for prefix, nspaces in self.prefixes.items():
            self.graph.bind(prefix, nspaces)

        for plan in self.rdfdata.triple_plan.values():
            if not plan["objects"]:
                continue
            subject_colindex = plan["subject"].copy().pop()
            object_colindices = plan["objects"].copy()

            for row_index in range(len(self.rdfdata.data)):

                if pd.notnull(self.rdfdata.data.iat[row_index, subject_colindex]):
                    subject = self._get_node(str(self.rdfdata.data.iat[row_index, subject_colindex]), self.rdfdata.types_and_languages[(row_index,subject_colindex)][0], f"r{row_index}c{subject_colindex}")

                    for column_index in object_colindices:

                        entry = self.rdfdata.data.iat[row_index, column_index]
                        if pd.notnull(entry) and str(entry) != "":  # Check if value isn't NaN
                            pred_name = str(self.rdfdata.data.columns[column_index])
                            predicate = self._get_node(pred_name, "^^uri")

                            obj_names = str(entry).split(";")
                            objects = [self._get_node(value, self.rdfdata.types_and_languages[(row_index, column_index)][i], f"r{row_index}c{column_index}") for i, value in enumerate(obj_names)]

                            for index, objekt in enumerate(objects):
                                if (row_index, column_index) in self.rdfdata.uncertainties:
                                    if model_id in [3, 4, 5, 10]:
                                        if "weights" in self.rdfdata.uncertainties[(row_index, column_index)]:
                                            if len(self.rdfdata.uncertainties[(row_index, column_index)]["weights"]) <= index:
                                                print(f"Coin {subject.n3()} Predicate {pred_name} has uncertainties {self.rdfdata.uncertainties[(row_index, column_index)]['weights']} and object {[ob.n3() for ob in objects]}")
                                            weight = self.rdfdata.uncertainties[(row_index, column_index)]["weights"][index]
                                        else:
                                            weight = float("%.2f" % random())
                                    match model_id:
                                        case 1:
                                            self._generate_uncertain_value_solution_1(subject, predicate, objekt)
                                        case 2:
                                            self._generate_uncertain_value_solution_2(subject, predicate, objekt)
                                        case 3:
                                            self.graph.add((BNode("A3"), RDF["type"], CRM["R1_Reliability_Assessment"]))
                                            self._generate_uncertain_value_solution_3(subject, predicate, objekt, weight)
                                        case 4:
                                            self._generate_uncertain_value_solution_4(subject, predicate, objekt, weight, index)
                                        case 5:
                                            self._generate_uncertain_value_solution_5(subject, predicate, objekt, weight, crm_properties)
                                        case 6:
                                            self._generate_uncertain_value_solution_6(subject, predicate, objekt)
                                        case 7:
                                            self._generate_uncertain_value_solution_7(subject, predicate, objekt)
                                        case 8:
                                            self._generate_uncertain_value_solution_8(subject, predicate, objekt)
                                        case 9:
                                            self._generate_uncertain_value_solution_9a(subject, predicate, objekt)
                                        case 10:
                                            self._generate_uncertain_value_solution_9b(subject, predicate, objekt, weight)
                                        case _:
                                            self.graph.add((subject, predicate, objekt))

                                else:
                                    self.graph.add((subject, predicate, objekt))

        # Save sparql-prefix txt:
        with open(Path(self.OUTPUT_FOLDER, "graph_prefixes.txt"), 'w') as file:
            file.write("".join("PREFIX " + prefix + ": <" + self.prefixes[prefix] + ">" + "\n" for prefix in self.prefixes))

        # Save RDF Graph:
        if xml_format:
            with open(Path(self.OUTPUT_FOLDER, "graph.rdf"), 'w') as file:
                file.write(self.graph.serialize(format='pretty-xml'))
        else:
            with open(Path(self.OUTPUT_FOLDER, "graph.ttl"), 'w') as file:
                file.write(self.graph.serialize(format="turtle"))

            if model_id == 9:
                self.change_to_model_9a()
            elif model_id == 10:
                self.change_to_model_9b()

    def _get_node(self, value: str, datatype: str, identification: str = "") -> Literal | BNode | IdentifiedNode:
        """
        Method which returns the node of the given value and type.

        Parameters
        ----------
        value: str
            String of the entry of the value of the node.
        datatype: str
            String of the type or the language of the node.
        identification: str
            String which includes the cell position to identify a blank node.
        """
        value = value.strip()
        if not datatype:
            return Literal(value)
        elif datatype[0:2] == "^^":
            if datatype == "^^blank":
                return BNode(f"v{value}{identification}")
            if datatype == "^^uri":
                return self._get_uri_node(value)
            else:
                return Literal(value, datatype=self._get_uri_node(datatype[2:]))
        elif datatype[0:1] == "@":
            return Literal(value, lang=datatype[1:])
        else:
            raise ValueError(f"Could not translate type \"{datatype}\"")

    def _get_uri_node(self, uri: str) -> IdentifiedNode:
        """
        Returns the node of the given URI.

        Parameters
        ----------
        uri: str
            String of the URI. Can be a URI in prefix shape or the complete URI with starting < and ending >.
        """
        if uri[0] == "<" and uri[-1] == ">":
            uri = uri[1:-1]
            return URIRef(uri)
        else:
            splitlist = uri.split(":")
            if len(splitlist) >= 2:
                if splitlist[0] in self.prefixes:
                    return self.prefixes[splitlist[0]][uri[len(splitlist[0])+1:]]
                else:
                    raise ValueError(f"Unknown prefix {splitlist[0]} in uri \"{uri}\". To add prefixes for namespaces use the method \"load_prefixes\".")
            else:
                raise ValueError(f"Could not find prefix in uri \"{uri}\"")

    def _generate_uncertain_value_solution_1(self, subject: URIRef, predicate: URIRef, objekt: URIRef | Literal) -> None:
        """ 
        Uses model 1 to add an uncertain statement to the rdf graph.

        Parameters
        ----------
        subject: URIRef | Literal
            Node of the subject of the uncertain statement.
        predicate: URIRef
            Node of the predicate of the uncertain statement.
        objekt: URIRef | Literal
            Node of the object of the uncertain statement.
        """
        node = BNode()
        self.graph.add((subject, predicate, objekt))
        self.graph.add((node, CRM["P141_assigned"], objekt))
        self.graph.add((node, CRM["P140_assigned_attribute_to"], subject))
        self.graph.add((node, BMO["PX_Property"], predicate))
        self.graph.add((node, RDF["type"], CRM["E13_Attribute_Assignment"]))
        self.graph.add((node, BMO["PX_likelihood"], NM["uncertain_value"]))

    def _generate_uncertain_value_solution_2(self, subject: URIRef, predicate: URIRef, objekt: URIRef | Literal) -> None:
        """ 
        Uses model 2 to add an uncertain statement to the rdf graph.
        
        Parameters
        ----------
        subject: URIRef | Literal
            Node of the subject of the uncertain statement.
        predicate: URIRef
            Node of the predicate of the uncertain statement.
        objekt: URIRef | Literal
            Node of the object of the uncertain statement.
        """
        node = BNode()
        self.graph.add((subject, predicate, node))
        self.graph.add((node, UN["hasUncertainty"], NM["uncertain_value"]))
        self.graph.add((node, RDF.value, objekt))

    def _generate_uncertain_value_solution_3(self, subject: URIRef, predicate: URIRef, objekt: URIRef | Literal, weight: float) -> None:
        """
        Uses model 3 to add an uncertain statement to the rdf graph.
        
        Parameters
        ----------
        subject: URIRef | Literal
            Node of the subject of the uncertain statement.
        predicate: URIRef
            Node of the predicate of the uncertain statement.
        objekt: URIRef | Literal
            Node of the object of the uncertain statement.
        weight: float
            Weight of the uncertain statement.
        """
        b = BNode()
        c = BNode()

        self.graph.add((BNode("A3"), CRM["T1_assessed_the_reliability_of"], b))

        self.graph.add((b, RDF.type, CRM["E13_Attribute_Assignment"]))
        self.graph.add((b, RDF.Property, predicate))
        self.graph.add((b, CRM["T2_assessed_as_reliability"], c))
        self.graph.add((b, CRM["P140_assigned_attribute_to"], subject))
        self.graph.add((b, CRM["P141_assigned"], objekt))

        # Weight:
        self.graph.add((c, CRM["P90_has_value"], Literal(weight, datatype=XSD["double"], normalize=True)))
        self.graph.add((c, RDF.type, CRM["R2_Reliability"]))

        self.graph.add((subject, predicate, objekt))

    def _generate_uncertain_value_solution_4(self, subject: URIRef, predicate: URIRef, objekt: URIRef | Literal, weight: float, object_index: int) -> None:
        """ 
        Uses model 4 to add an uncertain statement to the rdf graph.
        
        Parameters
        ----------
        subject: URIRef | Literal
            Node of the subject of the uncertain statement.
        predicate: URIRef
            Node of the predicate of the uncertain statement.
        objekt: URIRef | Literal
            Node of the object of the uncertain statement.
        weight: float
            Weight of the uncertain statement.
        object_index: int
            Index of the object of its cell.
        """
        uncertainty_id = (subject.n3() + predicate.n3()).replace(":", "")
        b = BNode(uncertainty_id)
        c = BNode()

        self.graph.add((subject, predicate, b))
        self.graph.add((b, RDF.type, CRMINF["I5_Inference_Making"]))
        self.graph.add((b, CRMINF["J2_concluded_that"], c))

        if weight < 0.25:
            level = "uncertain"
        elif weight < 0.5:
            level = "plausible"
        elif weight < 0.75:
            level = "likely"
        else:
            level = "very likely"

        self.graph.add((c, CRMINF["I4_Proposition_Set"], Literal(f"Proposetion_{object_index}")))
        self.graph.add((c, CRMINF["J5_holds_to_be"], Literal(level)))
        self.graph.add((c, CRMINF["J4_that"], objekt))
        self.graph.add((c, RDF["type"], CRMINF["I2_Belief"]))

    def _generate_uncertain_value_solution_5(self, subject: URIRef, predicate: URIRef, objekt: URIRef | Literal, weight: float, crm_properties: dict) -> None:
        """
        Uses model 5 to add an uncertain statement to the rdf graph.
        
        Parameters
        ----------
        subject: URIRef | Literal
            Node of the subject of the uncertain statement.
        predicate: URIRef
            Node of the predicate of the uncertain statement.
        objekt: URIRef | Literal
            Node of the object of the uncertain statement.
        weight: float
            Weight of the uncertain statement.
        crm_properties: dict
            Dictionary which contains the nomisma properties as keys and the corresponding .2 CRM properties as values.
        """
        node = BNode()
        crm_property = "P3.2_uncertain_value" if predicate.n3()[1:-1] not in crm_properties else crm_properties[predicate.n3()[1:-1]]

        self.graph.add((subject, predicate, node))

        self.graph.add((node, AMT["weight"], Literal(weight, datatype=XSD["double"], normalize=True)))
        self.graph.add((node, CRM[crm_property], objekt))

    def _generate_uncertain_value_solution_6(self, subject: URIRef, predicate: URIRef, objekt: URIRef | Literal) -> None:
        """
        Uses model 6 to add an uncertain statement to the rdf graph.
        
        Parameters
        ----------
        subject: URIRef | Literal
            Node of the subject of the uncertain statement.
        predicate: URIRef
            Node of the predicate of the uncertain statement.
        objekt: URIRef | Literal
            Node of the object of the uncertain statement.
        """
        node = BNode()

        self.graph.add((subject, predicate, objekt))
        self.graph.add((node, RDF["object"], objekt))
        self.graph.add((node, RDF["subject"], subject))
        self.graph.add((node, RDF["predicate"], predicate))
        self.graph.add((node, RDF["type"], EDTFO["UncertainStatement"]))

    def _generate_uncertain_value_solution_7(self, subject: URIRef, predicate: URIRef, objekt: URIRef | Literal) -> None:
        """
        Uses model 7 to add an uncertain statement to the rdf graph.
        
        Parameters
        ----------
        subject: URIRef | Literal
            Node of the subject of the uncertain statement.
        predicate: URIRef
            Node of the predicate of the uncertain statement.
        objekt: URIRef | Literal
            Node of the object of the uncertain statement.
        """
        node = BNode()

        self.graph.add((subject, predicate, node))
        self.graph.add((node, RDF["type"], EDTFO["ApproximateStatement"]))
        self.graph.add((node, RDF.value, objekt))

    def _generate_uncertain_value_solution_8(self, subject: URIRef, predicate: URIRef, objekt: URIRef | Literal) -> None:
        """
        Uses model 8 to add an uncertain statement to the rdf graph.
        
        Parameters
        ----------
        subject: URIRef | Literal
            Node of the subject of the uncertain statement.
        predicate: URIRef
            Node of the predicate of the uncertain statement.
        objekt: URIRef | Literal
            Node of the object of the uncertain statement.
        """
        node = BNode(subject.n3().replace(":", ""))

        self.graph.add((subject, UN["hasUncertainty"], node))

        self.graph.add((node, predicate, objekt))

    def _generate_uncertain_value_solution_9a(self, subject: URIRef, predicate: URIRef, objekt: URIRef | Literal) -> None:
        """
        Creates a placeholder statement, which has to be replaced by change_to_model_9a() to create
        the correct uncertain statement.
        
        Parameters
        ----------
        subject: URIRef | Literal
            Node of the subject of the uncertain statement.
        predicate: URIRef
            Node of the predicate of the uncertain statement.
        objekt: URIRef | Literal
            Node of the object of the uncertain statement.
        """
        node = BNode()

        self.graph.add((EDTFO[node.n3()[2:]], RDF["star"], Literal(f"{subject.n3(namespace_manager=self.graph.namespace_manager)}$${predicate.n3(namespace_manager=self.graph.namespace_manager)}$${objekt.n3(namespace_manager=self.graph.namespace_manager)}")))

    def _generate_uncertain_value_solution_9b(self, subject: URIRef, predicate: URIRef, objekt: URIRef | Literal, weight: float) -> None:
        """
        Creates a placeholder statement, which has to be replaced by change_to_model_9b()
        to create the correct uncertain statement.
        
        Parameters
        ----------
        subject: URIRef
            Node of the subject of the uncertain statement.
        predicate: URIRef
            Node of the predicate of the uncertain statement.
        objekt: URIRef | Literal
            Node of the object of the uncertain statement.
        weight: float
            Weight of the uncertain statement.
        """
        node = BNode()

        self.graph.add((UN[node.n3()[2:]], RDF["star"], Literal(f"{subject.n3(namespace_manager=self.graph.namespace_manager)}$${predicate.n3(namespace_manager=self.graph.namespace_manager)}$${objekt.n3(namespace_manager=self.graph.namespace_manager)}$${weight}")))

    def _get_crm_properties(self) -> dict:
        """
        Method which returns the dictionary for the .2 properties of solution 5.
        """
        nmo_prefix = "http://nomisma.org/ontology#"

        crm_dict = {
            nmo_prefix + "hasCollection": "P107.2_uncertain_member",
            nmo_prefix + "hasTypeSeriesItem": "P107.2_uncertain_member",

            nmo_prefix + "hasContemporaryName": "P102.2_uncertain_name_or_ethnic",
            nmo_prefix + "hasScholarlyName": "P102.2_uncertain_name_or_ethnic",

            nmo_prefix + "hasDie": "P16.2_uncertain_technique_or_object_used_for_creation",
            nmo_prefix + "hasProductionObject": "P16.2_uncertain_technique_or_object_used_for_creation",
            nmo_prefix + "hasManufacture": "P16.2_uncertain_technique_or_object_used_for_creation",

            nmo_prefix + "hasCountermark": "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasMintmark": "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasSecondaryTreatment": "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasPeculiarity": "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasPeculiarityOfProduction": "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasCorrosion": "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasWear": "P103.2_uncertain_symbole_or_features",

            nmo_prefix + "hasObjectType": "P67.2_uncertain_type",
            nmo_prefix + "representsObjectType": "P67.2_uncertain_type",

            nmo_prefix + "hasAuthenticity": "P138.2_uncertain_authenticity",

            nmo_prefix + "hasAuthority": "P14.2_uncertain_authority_or_issuer",
            nmo_prefix + "hasIssuer": "P14.2_uncertain_authority_or_issuer",

            nmo_prefix + "hasMint": "P189.2_uncertain_place",
            nmo_prefix + "hasFindspot": "P189.2_uncertain_place",

            nmo_prefix + "hasMaterial": "P137.2_uncertain_material",

            nmo_prefix + "hasContext": "P136.2_uncertain_context_or_taxonomy",

            nmo_prefix + "hasAppearance": "P139.2_uncertain_form",
            nmo_prefix + "hasShape": "P139.2_uncertain_form",
            nmo_prefix + "hasEdge": "P139.2_uncertain_form",

            nmo_prefix + "hasFace": "P19.2_uncertain_mode",
            nmo_prefix + "hasObverse": "P19.2_uncertain_mode",
            nmo_prefix + "hasReverse": "P19.2_uncertain_mode",

            nmo_prefix + "hasPortrait": "P62.2_uncertain_depiction",
            nmo_prefix + "hasIconography": "P62.2_uncertain_depiction",
            nmo_prefix + "hasLegend": "P62.2_uncertain_depiction"
        }
        return crm_dict

    def run_query(self, query: str, save_result: bool = True) -> pd.DataFrame:
        """
        Runs the given query on the generated rdf graph.
        
        Parameters
        ----------
        query: str
            String of the hole query.
        save_result: bool
            If True, the method saves the result in data/output/query_results_fuseki.csv.
        """
        result = self.graph.query(query)

        dataframe = data_optimize(pd.DataFrame(result.bindings))

        if save_result:
            dataframe.to_csv(str(Path(UNCO_PATH, "data/output/query_results_fuseki.csv")))

        return dataframe

    def change_to_model_9a(self) -> None:
        """
        Creates all rdf* uncertain statements of solution 9a.
        """
        for line in input(str(Path(self.OUTPUT_FOLDER, "graph.ttl")), inplace=True):
            if "rdf:star" in line:
                splitlist = line.split("rdf:star")
                splitlist = splitlist[1][:-2].strip().split("$$")

                # Delete ":
                splitlist[0] = splitlist[0][1:]
                splitlist[-1] = splitlist[-1][:-1]

                line = f"<< {splitlist[0]} {splitlist[1]} {splitlist[2]} >> rdf:type edtfo:UncertainStatement .".replace("\\\"", "\"")

            print(line)

    def change_to_model_9b(self) -> None:
        """
        Creates all rdf* uncertain statements of solution 9b.
        """
        for line in input(str(Path(self.OUTPUT_FOLDER, "graph.ttl")), inplace=True):
            if "rdf:star" in line:
                splitlist = line.split("rdf:star")
                splitlist = splitlist[1][:-2].strip().split("$$")

                # Clean lineparts
                splitlist[0] = splitlist[0][1:]
                splitlist[-1] = splitlist[-1][:-1]

                line = f"<< {splitlist[0]} {splitlist[1]} {splitlist[2]} >> un:hasUncertainty {splitlist[3]} .".replace("\\\"", "\"")

            print(line)


if __name__ == "__main__":
    afe = open(str(Path(UNCO_PATH, "data/testdata/afe/afemapping_changed_10rows.csv")), encoding='utf-8')
    prefixes = str(Path(UNCO_PATH, "data/testdata/afe/namespaces.csv"))

    from unco.data.uncertainty_generator import UncertaintyGenerator
    from unco.data.data_util import data_optimize

    rdf_data = RDFData(data_optimize(pd.read_csv(afe)))
    generator = GraphGenerator(UncertaintyGenerator(rdf_data).add_pseudorand_uncertainty_flags([1], 2, 2))
    generator.load_prefixes(prefixes)
    generator.generate_solution(xml_format=False, model_id=10)

    test_query = """
                    PREFIX nmo: <http://nomisma.org/ontology#>

                    SELECT ?su ?p ?o
                    WHERE {
                        ?su ?p ?o
                    }
                    """

    print(generator.run_query(test_query))
