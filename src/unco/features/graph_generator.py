from genericpath import exists
import isodate
import pandas as pd
from pathlib import Path
from unco import UNCO_PATH
from unco.data.rdf_data import RDFData
from rdflib import Graph, Namespace, BNode, Literal, URIRef


# Standard Namespaces------------------------------------------------------------------------
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
UN = Namespace("http://www.w3.org/2005/Incubator/urw3/XGRurw3-20080331/Uncertainty.owl")
# CRM = Namespace("http://erlangen-crm.org/current/")
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
BMO = Namespace("http://collection.britishmuseum.org/id/ontology/")
NM = Namespace("http://nomisma.org/id/")
EDTFO = Namespace("https://periodo.github.io/edtf-ontology/edtfo.ttl")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
CRMINF = Namespace("https://ontome.net/ns/crminf/")
AMT = Namespace("http://academic-meta-tool.xyz/vocab#")
UNCO = Namespace("localhost:8501/id/")

class GraphGenerator():
    """
        Class which creates an RDF-XML file.

    Attributes
    ----------
    rdfdata : RDFData
        RDFData which contains the data of the rdf graph.
    graph : Graph
        RDF graph which will be created.
    OUTPUT_FOLDER : Path
        Constant which holds the output path.
    prefixes : dict
        Dictionary which contains the prefixes and namespaces which binds to the graph.
    crm_properties : dict
        Dictionary which contains the .2 properties of solution 5.
    """

    def __init__(self, rdfdata: RDFData) -> None:
        """
        Parameters
        ----------
        rdfdata : RDFData
            Object which contains the data of the rdf graph.
        """
        self.rdfdata = rdfdata
        self.graph = Graph()
        self.OUTPUT_FOLDER = Path(UNCO_PATH, "data/output")
        self.prefixes : dict[str,Namespace] = {"xsd" : XSD, "rdf" : RDF, "rdfs" : RDFS, "" : UNCO}
        self.crm_properties = {}


    def load_prefixes(self, path_data : str | pd.DataFrame):
        """
            Method to load prefixes of namespaces and bind them to the graph.

        Parameters
        ----------
        path_data : str
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
    

    def generate_solution(self,solution_id : int = 4, xml_format : bool = True) -> None:
        """ 
            Method to generate the RDF-XML file.

        Attributes
        ----------
        solution_id : int
            Solution id, which should be generated.
        xml_format : bool
            Output will be in XML format, otherwise Turtle.
        """
        self.graph = Graph()
        self._load_prefixes_of_solution(solution_id)
        for prefix, nspaces in self.prefixes.items():
            self.graph.bind(prefix, nspaces)

        for plan in self.rdfdata.triple_plan.values():
            if not plan["objects"]:
                continue
            subject_colindex = plan["subject"].copy().pop()
            object_colindices = plan["objects"].copy()

            for row_index in range(len(self.rdfdata.data)):

                if pd.notnull(self.rdfdata.data.iat[row_index,subject_colindex]):
                    subject = self._get_node(str(self.rdfdata.data.iat[row_index,subject_colindex]), self.rdfdata.types_and_languages[(row_index,subject_colindex)][0])

                    for column_index in object_colindices:

                        entry = self.rdfdata.data.iat[row_index,column_index]
                        if pd.notnull(entry): # Check if value isn't NaN
                            pred_name = str(self.rdfdata.data.columns[column_index])
                            predicate = self._get_node(pred_name, "^^uri")

                            obj_names = str(entry).split(";")
                            objects = [self._get_node(value, self.rdfdata.types_and_languages[(row_index,column_index)][i]) for i, value in enumerate(obj_names)]

                            for index, object in enumerate(objects):
                                if (row_index,column_index) in self.rdfdata.uncertainties:
                                    # uncertainty_id = ''.join(c for c in pred_name + obj_names[index] if c.isalnum())
                                    uncertainty_id = subject.n3() + pred_name
                                    if solution_id in [3,4,5]:
                                        if "likelihoods" in self.rdfdata.uncertainties[(row_index,column_index)]:
                                            weight = self.rdfdata.uncertainties[(row_index,column_index)]["likelihoods"][index]
                                        else:
                                            weight = 0.5
                                            print(f"Warning: No weighted uncertainties for entry {object} in column {predicate}, altough model {solution_id} needs some. Weight 0.5 will be taken instead.")
                                    match solution_id:
                                        case 1:
                                            self._generate_uncertain_value_solution_1(subject, predicate, object)
                                        case 2:
                                            self._generate_uncertain_value_solution_2(subject, predicate, object)
                                        case 3:
                                            self._generate_uncertain_value_solution_3(subject, predicate, object, weight)
                                        case 4:
                                            self._generate_uncertain_value_solution_4(subject, predicate, object, weight, uncertainty_id, index)
                                        case 5:
                                            self._generate_uncertain_value_solution_5(subject, predicate, object, weight)
                                        case 6:
                                            self._generate_uncertain_value_solution_6(subject, predicate, object)
                                        case 7:
                                            self._generate_uncertain_value_solution_7(subject, predicate, object)
                                        case 8:
                                            self._generate_uncertain_value_solution_8(subject, predicate, object)
                                        case _:
                                            self.graph.add((subject, predicate, object))

                                else:
                                        self.graph.add((subject, predicate, object))

        filename = "graph"

        # Save sparql-prefix txt:
        with open(Path(self.OUTPUT_FOLDER, filename + "_prefixes.txt"), 'w') as file:
            file.write("".join("PREFIX " + prefix + ": <" + self.prefixes[prefix] + ">" + "\n" for prefix in self.prefixes))

        # Save RDF Graph:
        if xml_format:
            with open(Path(self.OUTPUT_FOLDER, filename + ".rdf"), 'w') as file:
                    file.write(self.graph.serialize(format='pretty-xml'))
        else:
            with open(Path(self.OUTPUT_FOLDER, filename + ".ttl"), 'w') as file:
                    file.write(self.graph.serialize(format="turtle"))


    def _get_node(self, value: str, type: str):
        """
        Method which returns the node of the given value and type.

        Parameter
        ---------
        value : str
            String of the entry of the value of the node.
        type : str
            String of the type or the language of the node.
        """
        value = value.strip()
        if type is None:
            return Literal(value)
        elif type[0:2] == "^^":
            if type == "^^id":
                return BNode("id" + value)
            if type == "^^uri":
                return self._get_uri_node(value)
            else:
                return Literal(value, datatype=self._get_uri_node(type[2:]))
        elif type[0:1] == "@":
            return Literal(value, lang=type[1:])
        else:
            raise ValueError(f"Could not translate type \"{type}\"")
            
    
    def _get_uri_node(self, string: str):
        """
        Method which return the uri node of the given type.

        Parameter
        ---------
        string : str
            String of the uri. Can be a uri in prefix shape or the complete uri with starting < and ending >.
        """
        if string[0] == "<" and string[-1] == ">":
            string = string[1:-1]
            return URIRef(string)
        else:
            splitlist = string.split(":")
            if len(splitlist) >= 2:
                if splitlist[0] in self.prefixes:
                    return self.prefixes[splitlist[0]][string[len(splitlist[0])+1:]]
                else:
                    raise ValueError(f"Unknown prefix {splitlist[0]} in uri \"{string}\". To add prefixes for namespaces use the method \"load_prefixes\".")
            else:
                raise ValueError(f"Could not find prefix in uri \"{string}\"")


    def _load_prefixes_of_solution(self, solution_id : int = 0) -> None:
        """
            Method to load and bind the necessary prefixes for a solution.

        Parameters
        ----------
        solution_id : int
            Number of the solution.
        """
        match solution_id:
            case 1:
                self.graph.bind("crm", CRM)
                self.graph.bind("bmo", BMO)
                self.graph.bind("rdf", RDF)
                self.graph.bind("nm", NM)
                self.prefixes["crm"] = CRM
                self.prefixes["bmo"] = BMO
                self.prefixes["rdf"] = RDF
                self.prefixes["nm"] = NM
            case 2:
                self.graph.bind("rdf", RDF)
                self.graph.bind("nm", NM)
                self.graph.bind("un", UN)
                self.prefixes["rdf"] = RDF
                self.prefixes["nm"] = NM
                self.prefixes["un"] = UN
            case 3:
                self.graph.bind("crm", CRM)
                self.graph.bind("rdf", RDF)
                self.prefixes["crm"] = CRM
                self.prefixes["rdf"] = RDF
                self.graph.add((BNode("A3"), RDF.type, CRM["R1_Reliability_Assessment"]))
            case 4:
                self.graph.bind("rdf", RDF)
                self.graph.bind("crminf", CRMINF)
                self.prefixes["crminf"] = CRMINF
                self.prefixes["rdf"] = RDF
            case 5:
                self.graph.bind("amt", AMT)
                self.graph.bind("crm", CRM)
                self.graph.bind("rdfs", RDFS)
                self.prefixes["rdfs"] = RDFS
                self.prefixes["amt"] = AMT
                self.prefixes["crm"] = CRM
                self.crm_properties = self._get_crm_properties()
            case 6:
                self.graph.bind("rdf", RDF)
                self.graph.bind("edtfo", EDTFO)
                self.prefixes["edtfo"] = EDTFO
                self.prefixes["rdf"] = RDF
            case 7:
                self.graph.bind("rdf", RDF)
                self.graph.bind("edtfo", EDTFO)
                self.prefixes["edtfo"] = EDTFO
                self.prefixes["rdf"] = RDF
            case 8:
                self.graph.bind("un", UN)
                self.prefixes["un"] = UN
            case _:
                pass


    def _generate_uncertain_value_solution_1(self, subject : URIRef | Literal, predicate : URIRef, object : URIRef | Literal) -> None:
        """ Method to create an uncertain value of solution 1.
        Attributes
        ----------
        subject : URIRef | Literal
            Node of the subject, which gets an uncertain value.
        predicate : URIRef
            Node of the predicate, which is uncertain.
        object : URIRef | Literal
            Node of the object, which is uncertain.
        uncertainty_id : str
            Unique string to identify the predicate and object of this uncertain relation.
        """
        node = BNode()
        self.graph.add((subject, predicate, object))
        self.graph.add((node, CRM["P141_assigned"], object))
        self.graph.add((node, CRM["P140_assigned_attribute_to"], subject))
        self.graph.add((node, BMO["PX_Property"], predicate))
        self.graph.add((node, RDF["type"], CRM["E13"]))
        self.graph.add((node, BMO["PX_likelihood"], NM["uncertain_value"]))


    def _generate_uncertain_value_solution_2(self, subject : URIRef | Literal, predicate : URIRef, object : URIRef | Literal) -> None:
        """ Method to create an uncertain value of solution 2.
        Attributes
        ----------
        subject : URIRef | Literal
            Node of the subject, which gets an uncertain value.
        predicate : URIRef
            Node of the predicate, which is uncertain.
        object : URIRef | Literal
            Node of the object, which is uncertain.
        uncertainty_id : str
            Unique string to identify the predicate and object of this uncertain relation.
        """
        node = BNode()
        self.graph.add((subject, predicate, node))
        self.graph.add((node, UN["hasUncertainty"], NM["uncertain_value"]))
        self.graph.add((node, RDF.value, object))


    def _generate_uncertain_value_solution_3(self, subject : URIRef | Literal, predicate : URIRef, object : URIRef | Literal, weight : float) -> None:
        """ Method to create an uncertain value of solution 3.
        Attributes
        ----------
        subject : URIRef | Literal
            Node of the subject, which gets an uncertain value.
        predicate : URIRef
            Node of the predicate, which is uncertain.
        object : URIRef | Literal
            Node of the object, which is uncertain.
        weight : float
            Weight or likelihood of the certainty.
        """
        b = BNode()
        c = BNode()

        self.graph.add((BNode("A3"), CRM["T1_assessed_the_reliability_of"], b))

        self.graph.add((b, RDF.type, CRM["E13"]))
        self.graph.add((b, RDF.Property, predicate))
        self.graph.add((b, CRM["T2_assessed_as_reliability"], c))
        self.graph.add((b, CRM["P140_assigned_attribute_to"], subject))
        self.graph.add((b, CRM["P141_assigned"], object))

        # Likelihood:
        self.graph.add((c, CRM["P90_has_value"], Literal(weight, datatype = XSD["double"], normalize=True)))
        self.graph.add((c, RDF.type, CRM["R2_Reliability"]))

        self.graph.add((subject, predicate, object))


    def _generate_uncertain_value_solution_4(self, subject : URIRef | Literal, predicate : URIRef, object : URIRef | Literal, weight : float, uncertainty_id : str, object_index : int) -> None:
        """ Method to create an uncertain value of solution 4.
        Attributes
        ----------
        subject : URIRef | Literal
            Node of the subject, which gets an uncertain value.
        predicate : URIRef
            Node of the predicate, which is uncertain.
        object : URIRef | Literal
            Node of the object, which is uncertain.
        weight : float
            Weight or likelihood of the certainty.
        uncertainty_id : str
            Unique string to identify the predicate and object of this uncertain relation.
        has_alternatives : bool
            Boolean value to mark, if the entry has other alternatives or not.
        """
        b = BNode(uncertainty_id)
        c = BNode()

        self.graph.add((subject,predicate,b))
        self.graph.add((b,RDF.type,CRMINF["I5_Inference_Making"]))
        self.graph.add((b,CRMINF["J2_concluded_that"],c))


        if weight>0.5:
            level = "more likely"
        else:
            level = "uncertain"

        self.graph.add((c, CRMINF["I4_Proposition_Set"], Literal(f"Proposetion_{object_index}")))
        self.graph.add((c, CRMINF["J5_holds_to_be"], Literal(level)))
        self.graph.add((c, CRMINF["J4_that"], object))
        self.graph.add((c, RDF["type"], CRMINF["I2_Belief"]))


    def _generate_uncertain_value_solution_5(self, subject : URIRef | Literal, predicate : URIRef, object : URIRef | Literal, weight : float) -> None:
        """ Method to create an uncertain value of solution 5.
        Attributes
        ----------
        subject : URIRef | Literal
            Node of the subject, which gets an uncertain value.
        predicate : URIRef
            Node of the predicate, which is uncertain.
        object : URIRef | Literal
            Node of the object, which is uncertain.
        weight : float
            Weight or likelihood of the certainty.
        uncertainty_id : str
            Unique string to identify the predicate and object of this uncertain relation.
        """
        node = BNode()
        crm_property = "P3.2_uncertain_value" if predicate.n3()[1:-1] not in self.crm_properties else self.crm_properties[predicate.n3()[1:-1]]
        
        self.graph.add((CRM[crm_property], RDFS["domain"], CRM[f"PC{crm_property.split('.2')[0][1:]}_approximates"]))
        self.graph.add((CRM[crm_property], RDFS["range"], CRM["E55_Type"]))
        
        self.graph.add((subject, predicate, node))

        self.graph.add((node, AMT["weight"], Literal(weight, datatype = XSD["double"], normalize=True)))
        self.graph.add((node, CRM[crm_property], object))


    def _generate_uncertain_value_solution_6(self, subject : URIRef | Literal, predicate : URIRef, object : URIRef | Literal) -> None:
        """ Method to create an uncertain value of solution 6.
        Attributes
        ----------
        subject : URIRef | Literal
            Node of the subject, which gets an uncertain value.
        predicate : URIRef
            Node of the predicate, which is uncertain.
        object : URIRef | Literal
            Node of the object, which is uncertain.
        uncertainty_id : str
            Unique string to identify the predicate and object of this uncertain relation.
        """
        node = BNode()

        self.graph.add((subject, predicate, object))
        self.graph.add((node, RDF["object"], object))
        self.graph.add((node, RDF["subject"], subject))
        self.graph.add((node, RDF["predicate"], predicate))
        self.graph.add((node, RDF["type"], EDTFO["UncertainStatement"]))


    def _generate_uncertain_value_solution_7(self, subject : URIRef | Literal, predicate : URIRef, object : URIRef | Literal) -> None:
        """ Method to create an uncertain value of solution 7.
        Attributes
        ----------
        subject : URIRef | Literal
            Node of the subject, which gets an uncertain value.
        predicate : URIRef
            Node of the predicate, which is uncertain.
        object : URIRef | Literal
            Node of the object, which is uncertain.
        uncertainty_id : str
            Unique string to identify the predicate and object of this uncertain relation.
        """
        node = BNode()

        self.graph.add((subject, predicate, node))
        self.graph.add((node, RDF["type"], EDTFO["ApproximateStatement"]))
        self.graph.add((node, RDF.value, object))


    def _generate_uncertain_value_solution_8(self, subject : URIRef | Literal, predicate : URIRef, object : URIRef | Literal) -> None:
        """ Method to create an uncertain value of solution 8.
        Attributes
        ----------
        subject : URIRef | Literal
            Node of the subject, which gets an uncertain value.
        predicate : URIRef
            Node of the predicate, which is uncertain.
        object : URIRef | Literal
            Node of the object, which is uncertain.
        uncertainty_id : str
            Unique string to identify the predicate and object of this uncertain relation.
        """
        node = BNode(subject.n3())
        
        self.graph.add((subject, UN["hasUncertainty"], node))

        self.graph.add((node, predicate, object))


    def _get_crm_properties(self):
        """
        Method which returns the dictionary for the .2 properties of solution 5.
        """
        nmo_prefix = "http://nomisma.org/ontology#"

        crm_dict = {
            nmo_prefix + "hasCollection" : "P107.2_uncertain_member",
            nmo_prefix + "hasTypeSeriesItem" : "P107.2_uncertain_member",

            nmo_prefix + "hasContemporaryName" : "P102.2_uncertain_name_or_ethnic",
            nmo_prefix + "hasScholarlyName" : "P102.2_uncertain_name_or_ethnic",

            nmo_prefix + "hasDie" : "P16.2_uncertain_technique_or_object_used_for_creation",
            nmo_prefix + "hasProductionObject" : "P16.2_uncertain_technique_or_object_used_for_creation",
            nmo_prefix + "hasManufacture" : "P16.2_uncertain_technique_or_object_used_for_creation",

            nmo_prefix + "hasCountermark" : "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasMintmark" : "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasSecondaryTreatment" : "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasPeculiarity" : "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasPeculiarityOfProduction" : "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasCorrosion" : "P103.2_uncertain_symbole_or_features",
            nmo_prefix + "hasWear" : "P103.2_uncertain_symbole_or_features",

            nmo_prefix + "hasObjectType" : "P67.2_uncertain_type",
            nmo_prefix + "representsObjectType" : "P67.2_uncertain_type",

            nmo_prefix + "hasAuthenticity" : "P138.2_uncertain_authenticity",

            nmo_prefix + "hasAuthority" : "P14.2_uncertain_authority_or_issuer",
            nmo_prefix + "hasIssuer" : "P14.2_uncertain_authority_or_issuer",

            nmo_prefix + "hasMint" : "P189.2_uncertain_place",
            nmo_prefix + "hasFindspot" : "P189.2_uncertain_place",

            nmo_prefix + "hasMaterial" : "P137.2_uncertain_material",

            nmo_prefix + "hasContext" : "P136.2_uncertain_context_or_taxonomy",

            nmo_prefix + "hasAppearance" : "P139.2_uncertain_form",
            nmo_prefix + "hasShape" : "P139.2_uncertain_form",
            nmo_prefix + "hasEdge" : "P139.2_uncertain_form",

            nmo_prefix + "hasFace" : "P19.2_uncertain_mode",
            nmo_prefix + "hasObverse" : "P19.2_uncertain_mode",
            nmo_prefix + "hasReverse" : "P19.2_uncertain_mode",

            nmo_prefix + "hasPortrait" : "P62.2_uncertain_depiction",
            nmo_prefix + "hasIconography" : "P62.2_uncertain_depiction",
            nmo_prefix + "hasLegend" : "P62.2_uncertain_depiction"
        }
        return crm_dict
    

    def run_query(self, query : str) -> pd.DataFrame:
        result = self.graph.query(query)

        result.serialize(format="csv", destination=str(Path(self.OUTPUT_FOLDER, "query_results.csv")))

        csvdata = pd.read_csv(open(Path(self.OUTPUT_FOLDER, "query_results.csv"), 'r', encoding='utf-8'))

        return pd.DataFrame(csvdata)
    

if __name__ == "__main__":
    # Corpus Nummorum Beispiel:
    # file = open(str(Path(UNCO_PATH,"tests/test_data/csv_testdata/CorpusNummorum_Beispiel/input_data.csv")), encoding='utf-8')
    # prefixes = str(Path(UNCO_PATH,"tests/test_data/csv_testdata/CorpusNummorum_Beispiel/namespaces.csv"))

    # Uncertain Mint:
    # file = open(str(Path(UNCO_PATH,"tests/test_data/csv_testdata/1certain2uncertainMints/input_data.csv")), encoding='utf-8')
    # prefixes = str(Path(UNCO_PATH,"tests/test_data/csv_testdata/1certain2uncertainMints/namespaces.csv"))

    # Eingabeformat-Test:
    file = open(str(Path(UNCO_PATH,"tests/test_data/csv_testdata/eingabeformat.csv")), encoding='utf-8')
    prefixes = str(Path(UNCO_PATH,"tests/test_data/csv_testdata/namespaces.csv"))

    rdfdata = RDFData(pd.read_csv(file))
    generator = GraphGenerator(rdfdata)
    generator.load_prefixes(prefixes)
    generator.generate_solution(xml_format=False)

    test_query =    """
                    PREFIX nmo: <http://nomisma.org/ontology#>

                    SELECT ?su ?p ?o
                    WHERE {
                        ?su ?p ?o
                    }
                    """
    
    print(generator.run_query(test_query))