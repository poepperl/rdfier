import pandas as pd
from pathlib import Path
from colorama import Fore

from unco import UNCO_PATH
from unco.data.dataset import Dataset
from unco.data.reader import Reader

from rdflib import Graph, Namespace, BNode, Literal, URIRef, IdentifiedNode

# Standard Namespaces------------------------------------------------------------------------
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
UN = Namespace("http://www.w3.org/2005/Incubator/urw3/XGRurw3-20080331/Uncertainty.owl")
CRM = Namespace("http://erlangen-crm.org/current/")
BMO = Namespace("http://collection.britishmuseum.org/id/ontology/")
NM = Namespace("http://nomisma.org/id/")
EDTFO = Namespace("https://periodo.github.io/edtf-ontology/edtfo.ttl")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
CRMINF = Namespace("https://ontome.net/ns/crminf/")
AMT = Namespace("http://academic-meta-tool.xyz/vocab#")
UNCO = Namespace("localhost:8501/id/")

class RDFGenerator():
    """
        Class which creates an RDF-XML file.

    Attributes
    ----------
    dataset : Dataset
        Dataset which contains the data of the rdf graph.
    graph : Graph
        RDF graph which will be created.
    """

    def __init__(self, dataset: Dataset) -> None:
        """
        Parameters
        ----------
        dataset : Dataset
            Dataset which contains the data of the rdf graph.
        """
        self.dataset = dataset
        self.graph = Graph()
        self.generated_graph : Graph
        self.output_folder = Path(UNCO_PATH, "data/output")
        self.prefixes : dict[str,Namespace] = {"xsd" : XSD, "rdf" : RDF, "rdfs" : RDFS, "" : UNCO}
        self.triple_plan : dict[str, dict[str, set[int]]] = {}
        self.column_datatypes : dict[int, str] = {}
        self.column_languages : dict[int, str] = {}
        self.crm_properties = {}

    def load_prefixes(self, path_data : str | pd.DataFrame):
        """
            Method to load prefixes of namespaces and bind them to the graph.

        Parameters
        ----------
        path : str
            Path to the csv file with header: (prefix, namespace) or DataFrame of the file.
        """
        if type(path_data) == pd.DataFrame:
            namespaces = path_data
        else:
            namespaces = Reader(path_data).read()

        for rowindex in range(len(namespaces)):
            self.prefixes[str(namespaces.iloc[rowindex,0]).lower()] = Namespace(str(namespaces.iloc[rowindex,1])) 

        for prefix in self.prefixes:
            self.graph.bind(prefix, self.prefixes[prefix])
    

    def _generate_triple_plan(self):
        """
            Method which locates the subject columns and the corresponding objects and saves it in the triple_plan.
        """
        first_col_has_ref = (False, '')
        first_col_objects = set()

        for index, column in enumerate(self.dataset.data):
            new_column_name = column

            splitlist = str(new_column_name).split("**")
            if len(splitlist) == 2:
                subject_id = splitlist[-1]
                new_column_name = splitlist[0]

                if index == 0:
                    first_col_has_ref = (True, subject_id)

                if subject_id in self.triple_plan:
                    if len(self.triple_plan[subject_id]["subject"]) > 0:
                        print(Fore.RED + "ERROR: Duplicate subject reference: " + subject_id + Fore.RESET)
                    self.triple_plan[subject_id]["subject"] = set([index])
                    
                else:
                    self.triple_plan[subject_id] = {"subject" : set([index]), "object" : set()}

            elif len(splitlist) > 2:
                print(Fore.RED + "ERROR: Column " + str(column) + " has more than one subject reference marker '**'." + Fore.RESET)


            splitlist = str(new_column_name).split("__")
            if len(splitlist) == 2:
                object_id = splitlist[0]
                new_column_name = splitlist[1]

                if object_id in self.triple_plan:
                    self.triple_plan[object_id]["object"].add(index)

                else:
                    self.triple_plan[object_id] = {"object" : set([index]), "subject" : set()}

            elif len(splitlist) > 2:
                print(Fore.RED + "ERROR: Column " + str(column) + " has more than one object reference marker '__'." + Fore.RESET)

            elif index != 0:
                first_col_objects.add(index)


            if first_col_has_ref[0]:
                self.triple_plan[first_col_has_ref[1]]["object"].update(first_col_objects)
                self.triple_plan["**"] = self.triple_plan.pop(first_col_has_ref[1])

            else:
                self.triple_plan["**"] = {"object" : first_col_objects, "subject" : set([0])}
        
            self.dataset.data.rename({column : new_column_name}, axis=1, inplace=True) # Rename column


    def _get_datatype_and_language(self):
        """
            Method which read the datatype or language of all columns.
        """
        for index, column in enumerate(self.dataset.data):
            new_column_name = str(column)

            type_splitlist = str(column).split("^^")
            language_splitlist = str(column).split("@")

            if len(type_splitlist) == 2:
                new_column_name = type_splitlist[0]
                self.column_datatypes[index] = type_splitlist[1]

            elif len(type_splitlist) > 2:
                print(Fore.RED + "ERROR: Duplicate type reference (**) in " + str(column) + Fore.RESET)

            elif len(language_splitlist) >= 2 and len(language_splitlist[-1]) <= 3:
                new_column_name = new_column_name[:-len(language_splitlist[-1]) -1]
                self.column_languages[index] = language_splitlist[-1]
            
            self.dataset.data.rename({column : new_column_name}, axis=1, inplace=True) # Rename column
    

    def _get_datatype(self, value : str):
        """
            Method which tries to find the fitting datatype of a value.

        Parameters
        ----------
        value : str
            Entry of the csv table.
        """
        try:
            number = int(value)
            return "xsd:long"
        except:
            pass
        
        try:
            number = float(value)
            return "xsd:float"
        except:
            pass

        if value.lower() == "true" or value.lower() == "false":
            return "xsd:boolean"
        else:
            return ""
    

    def _get_uri_node(self, string : str, row_index : int, column_index : int):
        string = string
        if string[0] == "<" and string[-1] == ">":
            string = string[1:-1]
            return URIRef(string)
        else:
            splitlist = string.split(":")
            if len(splitlist) == 2:
                if splitlist[0] in self.prefixes:
                    return self.prefixes[splitlist[0]][splitlist[1]]
                else:
                    print(Fore.RED + "ERROR: Unknown prefix " + splitlist[0] + " in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)
            else:
                print(Fore.RED + "ERROR: Unknown URI " + string + " in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)


    def _get_subject_node(self, row_index : int, column_index : int) -> URIRef | Literal | None:
        """
            Method to generate and output the subject-node.

        Parameters
        ----------
        row_index : int
            Row index of the entry.
        column_index : int
            Column index of the entry.
        """
        value = str(self.dataset.data.iat[row_index,column_index])

        splitlist = value.split("^^")
        if len(splitlist) == 2:
            value = splitlist[0]
            datatype = splitlist[1]

        elif len(splitlist) > 2:
            print(Fore.RED + "ERROR: Find multiple datatypes in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)

        elif column_index in self.column_datatypes:
            datatype = self.column_datatypes[column_index]

        else:
            datatype = self._get_datatype(value)   

        try:
            if float(value) == int(value):
                value = int(value)
            else:
                value = float(value)
        except:
            pass

        match datatype:
            case "id":
                return BNode("i" + str(value).strip() + "c" + str(column_index))
                # return UNCO[value]
            case "uri":
                return self._get_uri_node(value, row_index, column_index)
            case "":
                return Literal(value)
            case other:
                if other[0] == "<" and other[-1] == ">":
                    other = other[1:-1]
                    return Literal(value, datatype=other)
                else:
                    splitlist = other.split(":")
                    if len(splitlist) == 2:
                        if splitlist[0] in self.prefixes:
                            return Literal(value, datatype = self.prefixes[splitlist[0]][splitlist[1]], normalize=True)
                        else:
                            print(Fore.RED + "ERROR: Unknown prefix " + splitlist[0] + " in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)
                    else:
                        print(Fore.RED + "ERROR: Unknown Datatype " + value + " in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)
        print(Fore.RED + "ERROR: Couldn't add node in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)
        return None


    def _get_predicate(self, column_index) -> tuple[URIRef | Literal | None, str]:
        """
            Method to generate and output the predicate.

        Parameters
        ----------
        column_index : int
            Column index of the entry.
        """
        string = str(self.dataset.data.columns[column_index]).strip()
        return self._get_uri_node(string, -1, column_index), string


    def _get_object_nodes(self, row_index : int, column_index : int) -> tuple[list[URIRef | Literal | None], list[str]]:
        """
            Method to generate and output the object-node.

        Parameters
        ----------
        row_index : int
            Row index of the entry.
        column_index : int
            Column index of the entry.
        """
        wrong_splitlist = str(self.dataset.data.iat[row_index,column_index]).split(";")
        right_splitlist = []
        old_element = ""
        for element in wrong_splitlist:
            if len(element.split("\"")) % 2 == 0:
                if len(old_element) > 0:
                    old_element = old_element + ";" + element
                else:
                    old_element = old_element + element
            else:
                if old_element != "":
                    right_splitlist.append(old_element)
                right_splitlist.append(element)
        
        if len(old_element) > 0:
            right_splitlist.append(old_element)

        nodelist = []
        namelist = []
        for value in right_splitlist:
            splitlist = str(value).split("^^")
            if len(splitlist) == 2:
                value = splitlist[0]
                datatype = splitlist[1]
            elif len(splitlist) > 2:
                print(Fore.RED + "ERROR: Find multiple datatypes in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)
            elif column_index in self.column_datatypes:
                datatype = self.column_datatypes[column_index]

            else:
                datatype = self._get_datatype(value)

            try:
                if float(value) == int(value):
                    value = int(value)
                else:
                    value = float(value)
            except:
                pass

            match datatype:
                case "id":
                    nodelist.append(BNode("i" + str(value).strip() + "c" + str(column_index)))
                    # nodelist.append(UNCO[value])
                    namelist.append(value)
                case "uri":
                    nodelist.append(self._get_uri_node(value, row_index, column_index))
                    namelist.append(value)
                case "":
                    lang_splitter = value.split("@")
                    if len(lang_splitter) >= 2 and len(lang_splitter[-1]) <= 3:
                        nodelist.append(Literal(lang_splitter[0], lang=lang_splitter[-1]))
                        namelist.append(value)
                    elif column_index in self.column_languages:
                        nodelist.append(Literal(value, lang=self.column_languages[column_index]))
                        namelist.append(value)
                    else:
                        nodelist.append(Literal(value))
                        namelist.append(value)
                case other:
                    if other[0] == "<" and other[-1] == ">":
                        other = other[1:-1]
                        nodelist.append(Literal(value, datatype=other))
                        namelist.append(value)
                    else:
                        splitlist = other.split(":")
                        if len(splitlist) == 2:
                            if splitlist[0] in self.prefixes:
                                nodelist.append(Literal(value, datatype = self.prefixes[splitlist[0]][splitlist[1]], normalize=True))
                                namelist.append(value)
                            else:
                                print(Fore.RED + "ERROR: Unknown prefix " + splitlist[0] + " in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)
                                nodelist.append(None)
                                namelist.append("")
                        else:
                            print(Fore.RED + "ERROR: Unknown Datatype " + value + " in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)
                            nodelist.append(None)
                            namelist.append("")
                    
        return nodelist, namelist


    def _remove_special_chars(self, value : str) -> str:
        """
            Method to generate and output a node id without special characters.

        Parameters
        ----------
        value : str
            Value with special characters, outputs the same string without special characters.
        """
        return ''.join(c for c in value if c.isalnum())

    def _get_sparql_prefixes(self) -> str:
        text = ""
        for prefix in self.prefixes:
            text += "PREFIX " + prefix + ": <" + self.prefixes[prefix] + ">" + "\n"
        return text

    def generate_solution(self,solution_id : int = 0, xml_format : bool = True) -> None:
        """ 
            Method to generate the RDF-XML file.

        Attributes
        ----------
        solution_id : int
            Solution id, which should be generated.
        xml_format : bool
            Output will be in XML format, otherwise Turtle.
        """
        self.generated_graph = self.graph

        self._load_prefixes_of_solution(solution_id)
        # Get triple_plan:
        self._generate_triple_plan()

        self._get_datatype_and_language()


        for plan in self.triple_plan:
            subject_colindex = self.triple_plan[plan]["subject"].copy().pop()
            object_colindices = self.triple_plan[plan]["object"].copy()

            for row_index in range(len(self.dataset.data)):
                subject = self._get_subject_node(row_index,subject_colindex)

                for column_index in object_colindices:

                    if pd.notnull(self.dataset.data.iat[row_index,column_index]): # Check if value isn't NaN
                        predicate, name = self._get_predicate(column_index)
                        objects, names = self._get_object_nodes(row_index, column_index)

                        for index, object in enumerate(objects):
                            if column_index in self.dataset.uncertainty_flags and row_index in self.dataset.uncertainty_flags[column_index]: # If current value is uncertain, do:
                                uncertainty_id = self._remove_special_chars(name + names[index])
                                match solution_id:
                                    case 1:
                                        self._generate_uncertain_value_solution_1(subject, predicate, object, uncertainty_id)
                                    case 2:
                                        self._generate_uncertain_value_solution_2(subject, predicate, object, uncertainty_id)
                                    case 3:
                                        self._generate_uncertain_value_solution_3(subject, predicate, object)
                                    case 4:
                                        self._generate_uncertain_value_solution_4(subject, predicate, object, uncertainty_id)
                                    case 5:
                                        self._generate_uncertain_value_solution_5(subject, predicate, object, uncertainty_id)
                                    case 6:
                                        self._generate_uncertain_value_solution_6(subject, predicate, object, uncertainty_id)
                                    case 7:
                                        self._generate_uncertain_value_solution_7(subject, predicate, object, uncertainty_id)
                                    case 8:
                                        self._generate_uncertain_value_solution_8(subject, predicate, object, uncertainty_id)
                                    case _:
                                        self.generated_graph.add((subject, predicate, object))

                            else:
                                    self.generated_graph.add((subject, predicate, object))

        if solution_id:
            filename = "graph_model_" + str(solution_id)
        else:
            filename = "graph"

        # Save sparql-prefix txt:
        with open(Path(self.output_folder, filename + "_prefixes.txt"), 'w') as file:
            file.write(self._get_sparql_prefixes())

        # Save RDF Graph:
        if xml_format:
            with open(Path(self.output_folder, filename + ".rdf"), 'w') as file:
                    file.write(self.generated_graph.serialize(format="xml"))
        else:
            with open(Path(self.output_folder, filename + ".ttl"), 'w') as file:
                    file.write(self.generated_graph.serialize(format="ttl"))


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
                self.generated_graph.bind("crm", CRM)
                self.generated_graph.bind("bmo", BMO)
                self.generated_graph.bind("rdf", RDF)
                self.generated_graph.bind("nm", NM)
                self.prefixes["crm"] = CRM
                self.prefixes["bmo"] = BMO
                self.prefixes["rdf"] = RDF
                self.prefixes["nm"] = NM
            case 2:
                self.generated_graph.bind("rdf", RDF)
                self.generated_graph.bind("nm", NM)
                self.generated_graph.bind("un", UN)
                self.prefixes["rdf"] = RDF
                self.prefixes["nm"] = NM
                self.prefixes["un"] = UN
            case 3:
                self.generated_graph.bind("crm", CRM)
                self.generated_graph.bind("rdf", RDF)
                self.prefixes["crm"] = CRM
                self.prefixes["rdf"] = RDF
            case 4:
                self.generated_graph.bind("crminf", CRMINF)
                self.prefixes["crminf"] = CRMINF
            case 5:
                self.generated_graph.bind("amt", AMT)
                self.generated_graph.bind("crm", CRM)
                self.prefixes["amt"] = AMT
                self.prefixes["crm"] = CRM
                self.crm_properties = self._get_crm_properties()
            case 6:
                self.generated_graph.bind("rdf", RDF)
                self.generated_graph.bind("edtfo", EDTFO)
                self.prefixes["edtfo"] = EDTFO
                self.prefixes["rdf"] = RDF
            case 7:
                self.generated_graph.bind("rdf", RDF)
                self.generated_graph.bind("edtfo", EDTFO)
                self.prefixes["edtfo"] = EDTFO
                self.prefixes["rdf"] = RDF
            case 8:
                self.generated_graph.bind("un", UN)
                self.prefixes["un"] = UN
            case _:
                pass


    def _generate_uncertain_value_solution_1(self, subject : URIRef | Literal | None, predicate : URIRef | None, object : URIRef | Literal | None, uncertainty_id : str) -> None:
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
        node = BNode(uncertainty_id)
        self.generated_graph.add((subject, predicate, object))
        self.generated_graph.add((node, CRM["P141_assigned"], object))
        self.generated_graph.add((node, CRM["P140_assigned_attribute_to"], subject))
        self.generated_graph.add((node, BMO["PX_Property"], predicate))
        self.generated_graph.add((node, RDF["type"], CRM["E13"]))
        self.generated_graph.add((node, BMO["PX_likelihood"], NM["uncertain_value"]))


    def _generate_uncertain_value_solution_2(self, subject : URIRef | Literal | None, predicate : URIRef | None, object : URIRef | Literal | None, uncertainty_id : str) -> None:
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
        node = BNode(uncertainty_id)
        self.generated_graph.add((subject, predicate, node))
        self.generated_graph.add((node, UN["hasUncertainty"], NM["uncertain_value"]))
        self.generated_graph.add((node, RDF.value, object))


    def _generate_uncertain_value_solution_3(self, subject : URIRef | Literal | None, predicate : URIRef | None, object : URIRef | Literal | None) -> None:
        """ Method to create an uncertain value of solution 3.
        Attributes
        ----------
        subject : URIRef | Literal
            Node of the subject, which gets an uncertain value.
        predicate : URIRef
            Node of the predicate, which is uncertain.
        object : URIRef | Literal
            Node of the object, which is uncertain.
        """
        A = BNode("A3")
        b = BNode()
        c = BNode()
        likelihood = 0.92

        self.generated_graph.add((A, RDF.type, CRM["R1_Reliability_Assessment"]))
        self.generated_graph.add((A, CRM["T1_assessed_the_reliability_of"], b))

        self.generated_graph.add((b, RDF.type, CRM["E13"]))
        self.generated_graph.add((b, RDF.Property, predicate))
        self.generated_graph.add((b, CRM["T2_assessed_the_reliability"], c))
        self.generated_graph.add((b, CRM["P140_assigned_the_reliability_to"], subject))
        self.generated_graph.add((b, CRM["P141_assigned"], object))

        # Likelihood:
        self.generated_graph.add((c, CRM["P90_has_value"], Literal(likelihood, datatype = XSD["double"], normalize=True)))
        self.generated_graph.add((c, RDF.type, CRM["R2_Reliability"]))

        self.generated_graph.add((subject, predicate, object))


    def _generate_uncertain_value_solution_4(self, subject : URIRef | Literal | None, predicate : URIRef | None, object : URIRef | Literal | None, uncertainty_id : str) -> None:
        """ Method to create an uncertain value of solution 4.
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
        node = BNode(uncertainty_id)
        
        self.generated_graph.add((subject, predicate, node))

        self.generated_graph.add((node, CRMINF["J5_holds_to_be"], Literal("uncertain")))
        self.generated_graph.add((node, RDF["type"], CRMINF["I2_Belief"]))
        self.generated_graph.add((node, CRMINF["J4_that"], object))


    def _generate_uncertain_value_solution_5(self, subject : URIRef | Literal | None, predicate : URIRef | None, object : URIRef | Literal | None, uncertainty_id : str) -> None:
        """ Method to create an uncertain value of solution 5.
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
        node = BNode(uncertainty_id)
        likelihood = 0.92
        crm_property = "P3_uncertain_value" if predicate.n3()[1:-1] not in self.crm_properties else self.crm_properties[predicate.n3()[1:-1]]
        
        self.generated_graph.add((CRM[crm_property], RDFS["domain"], CRM[f"PC{crm_property.split('.2')[0][1:]}_approximates"]))
        self.generated_graph.add((CRM[crm_property], RDFS["range"], CRM["E55_Type"]))
        
        self.generated_graph.add((subject, predicate, node))

        self.generated_graph.add((node, AMT["weight"], Literal(likelihood, datatype = XSD["double"], normalize=True)))
        self.generated_graph.add((node, CRM[crm_property], object))


    def _generate_uncertain_value_solution_6(self, subject : URIRef | Literal | None, predicate : URIRef | None, object : URIRef | Literal | None, uncertainty_id : str) -> None:
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
        node = BNode(uncertainty_id)

        self.generated_graph.add((subject, predicate, object))
        self.generated_graph.add((node, RDF["object"], object))
        self.generated_graph.add((node, RDF["subject"], subject))
        self.generated_graph.add((node, RDF["predicate"], predicate))
        self.generated_graph.add((node, RDF["type"], EDTFO["UncertainStatement"]))


    def _generate_uncertain_value_solution_7(self, subject : URIRef | Literal | None, predicate : URIRef | None, object : URIRef | Literal | None, uncertainty_id : str) -> None:
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
        node = BNode(uncertainty_id)

        self.generated_graph.add((subject, predicate, node))
        self.generated_graph.add((node, RDF["type"], EDTFO["ApproximateStatement"]))
        self.generated_graph.add((node, RDF.value, object))


    def _generate_uncertain_value_solution_8(self, subject : URIRef | Literal | None, predicate : URIRef | None, object : URIRef | Literal | None, uncertainty_id : str) -> None:
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
        
        self.generated_graph.add((subject, UN["hasUncertainty"], node))

        self.generated_graph.add((node, predicate, object))


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
    

if __name__ == "__main__":
    from pathlib import Path
    from unco import UNCO_PATH

    # Corpus Nummorum Beispiel:

    # dataset = Dataset(str(Path(UNCO_PATH,"tests/test_data/csv_testdata/CorpusNummorum_Beispiel/input_data.csv")))
    # generator = RDFGenerator(dataset)
    # generator.load_prefixes(str(Path(UNCO_PATH,"tests/test_data/csv_testdata/CorpusNummorum_Beispiel/namespaces.csv")))
    # generator.generate_solution()

    # Uncertain Mint:
    dataset = Dataset(str(Path(UNCO_PATH,r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\eingabeformat.csv")))
    dataset.add_uncertainty_flags(list_of_columns=[1], uncertainties_per_column=2)
    generator = RDFGenerator(dataset)
    generator.load_prefixes(str(Path(UNCO_PATH,r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\namespaces.csv")))
    
    print(generator._get_datatype("3.50"))