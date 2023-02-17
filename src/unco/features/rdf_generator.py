from pathlib import Path
from turtle import right
import pandas as pd
from unco import UNCO_PATH
from unco.data.dataset import Dataset
from rdflib import Graph, Namespace, BNode, Literal, URIRef, IdentifiedNode
from rdflib.namespace import RDF, XSD
from colorama import Fore

from unco.data.reader import Reader

NM = Namespace("http://nomisma.org/id/")
NMO = Namespace("http://nomisma.org/ontology#")
UN = Namespace("http://www.w3.org/2005/Incubator/urw3/XGRurw3-20080331/Uncertainty.owl")

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
        self.output_folder = Path(UNCO_PATH, "data/output")
        self.prefixes : dict[str,Namespace] = {"xsd" : XSD}
        self.triple_plan : dict[str, dict[str, set[int]]] = {}
        self.column_datatypes : dict[int, str] = {}
        self.column_languages : dict[int, str] = {}

    def load_prefixes(self, path : str):
        """
            Method to load prefixes of namespaces.

        Parameters
        ----------
        path : str
            Path to the csv file with header: (prefix, namespace)
        """
        namespaces = Reader(path).read()
        for rowindex in range(len(namespaces)):
            self.prefixes[str(namespaces.iloc[rowindex,0]).lower()] = Namespace(str(namespaces.iloc[rowindex,1])) 

    
    def _generate_triple_plan(self):
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


    def _get_subject_predicate_object(self, row_index : int, column_index : int) -> tuple[BNode, Literal, Literal]:
        subject = BNode(str(self.dataset.data.columns[column_index]) + str(self.dataset.data.iat[row_index,column_index]))
        predicate = Literal("has" + str(self.dataset.data.columns[column_index])) 
        object = Literal(str(self.dataset.data.iat[row_index,column_index])) 

        return subject, predicate, object
    

    def _get_datatype(self, value : str):
        try:
            number = int(value)
            return "xsd:long"
        except:
            pass
        try:
            number = float(value)
            return "xsd:double"
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
        value = str(self.dataset.data.iat[row_index,column_index])

        splitlist = value.split("^^")
        if len(splitlist) == 2:
            value = splitlist[0]
            datatype = splitlist[1]

        elif column_index in self.column_datatypes:
            datatype = self.column_datatypes[column_index]

        else:
            datatype = self._get_datatype(value)
        
        match datatype:
            case "id":
                return BNode("r" + str(row_index) + "c" + str(column_index))
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

    def _get_predicate(self, column_index):
        string = str(self.dataset.data.columns[column_index])
        return self._get_uri_node(string, -1, column_index)

    def _get_object_nodes(self, row_index : int, column_index : int) -> list[URIRef | Literal | None]:
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
        for value in right_splitlist:
            splitlist = value.split("^^")
            if len(splitlist) == 2:
                value = splitlist[0]
                datatype = splitlist[1]

            elif column_index in self.column_datatypes:
                datatype = self.column_datatypes[column_index]

            else:
                datatype = self._get_datatype(value)
            
            match datatype:
                case "id":
                    nodelist.append(BNode("r" + str(row_index) + "c" + str(column_index)))
                case "uri":
                    nodelist.append(self._get_uri_node(value, row_index, column_index))
                case "":
                    lang_splitter = value.split("@")
                    if len(lang_splitter) >= 2 and len(lang_splitter[-1]) <= 3:
                        nodelist.append(Literal(lang_splitter[0], lang=lang_splitter[-1]))
                    elif column_index in self.column_languages:
                        nodelist.append(Literal(value, lang=self.column_languages[column_index]))
                    else:
                        nodelist.append(Literal(value))
                case other:
                    if other[0] == "<" and other[-1] == ">":
                        other = other[1:-1]
                        nodelist.append(Literal(value, datatype=other))
                    else:
                        splitlist = other.split(":")
                        if len(splitlist) == 2:
                            if splitlist[0] in self.prefixes:
                                nodelist.append(Literal(value, datatype = self.prefixes[splitlist[0]][splitlist[1]], normalize=True))
                            else:
                                print(Fore.RED + "ERROR: Unknown prefix " + splitlist[0] + " in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)
                                nodelist.append(None)
                        else:
                            print(Fore.RED + "ERROR: Unknown Datatype " + value + " in column " + str(column_index) + " and row " + str(row_index) + Fore.RESET)
                            nodelist.append(None)
                    
        return nodelist


    def generate_solution(self,solution_id : int) -> None:
        """ 
            Method to generate the RDF-XML file.

        Attributes
        ----------
        solution_id : int
            Solution id, which should be generated.
        """
        # Bind namespace prefixes:
        for prefix in self.prefixes:
            self.graph.bind(prefix, self.prefixes[prefix])
        
        # Get triple_plan:
        self._generate_triple_plan()

        self._get_datatype_and_language()

        for ob in self.triple_plan:
            subject_colindex = self.triple_plan[ob]["subject"].copy().pop()
            object_colindices = self.triple_plan[ob]["object"].copy()

            for row_index in range(len(self.dataset.data)):
                subject = self._get_subject_node(row_index,subject_colindex)

                for column_index in object_colindices:

                    if pd.notnull(self.dataset.data.iat[row_index,column_index]): # Check if value isn't NaN
                        predicate = self._get_predicate(column_index)

                        objects = self._get_object_nodes(row_index, column_index)

                        for object in objects:
                            self.graph.add((subject, predicate, object)) # Example: Coin_4 nmo:hasMaterial nm:ar

                        if column_index in self.dataset.uncertainty_flags:
                            if row_index in self.dataset.uncertainty_flags[column_index]: # If current value is uncertain, do:
                                pass
                                # match solution_id:
                                #     case 1:
                                #         self._generate_uncertain_value_solution_1(coin, row_index, column_index)
                                #     case 2:
                                #         self._generate_uncertain_value_solution_2(coin, row_index, column_index)
                                #     case 3:
                                #         self._generate_uncertain_value_solution_3()
                                #     case 4:
                                #         self._generate_uncertain_value_solution_4()
                                #     case 5:
                                #         self._generate_uncertain_value_solution_5()
                                #     case 6:
                                #         self._generate_uncertain_value_solution_6(coin, row_index, column_index)
                                #     case 7:
                                #         self._generate_uncertain_value_solution_7(coin, row_index, column_index)
                                #     case 8:
                                #         self._generate_uncertain_value_solution_8()
                                # continue 
            

        with open(Path(self.output_folder, str(solution_id) + ".rdf"), 'w') as file:
            file.write(generator.graph.serialize(format="xml"))
        
    def _generate_uncertain_value_solution_1(self, coin : IdentifiedNode, row_index : int, column_index : int) -> None:
        """ Method to create an uncertain value of solution 1.
        Attributes
        ----------
        coin : IdentifiedNode
            Node of the coin, which gets an uncertain value.
        row_index : int
            Row index of the uncertain value.
        column_index : int
            Column index of the uncertain value.
        """
        CRM = Namespace("http://erlangen-crm.org/current/")
        BMO = Namespace("http://collection.britishmuseum.org/id/ontology/")
        self.graph.bind("crm", CRM)
        self.graph.bind("bmo", BMO)

        node, predicate, object = self._get_node_predicate_object(coin, row_index, column_index)

        self.graph.add((coin, NMO[predicate], NM[object]))
        self.graph.add((node, CRM["P141_assigned"], NM[object]))
        self.graph.add((node, CRM["P140_assigned_attribute_to"], coin))
        self.graph.add((node, BMO["PX_Property"], NMO[predicate]))
        self.graph.add((node, RDF["type"], CRM["E13"]))
        self.graph.add((node, BMO["PX_likelihood"], NM["uncertain_value"]))

    def _generate_uncertain_value_solution_2(self, coin : IdentifiedNode, row_index : int, column_index : int) -> None:
        """ Method to create an uncertain value of solution 2.
        Attributes
        ----------
        coin : IdentifiedNode
            Node of the coin, which gets an uncertain value.
        row_index : int
            Row index of the uncertain value.
        column_index : int
            Column index of the uncertain value.
        """
        node, predicate, object = self._get_node_predicate_object(coin, row_index, column_index)

        self.graph.add((coin, NMO[predicate], node))
        self.graph.add((node, UN["hasUncertainty"], NM["uncertain_value"]))
        self.graph.add((node, RDF.value, NM[object]))

    def _generate_uncertain_value_solution_3(self) -> None:
        """ Method to create an uncertain value of solution 3.
        """
        pass #TODO: Generieren der unsicheren Werte von Lösung 3

    def _generate_uncertain_value_solution_4(self) -> None:
        """ Method to create an uncertain value of solution 4.
        """
        pass #TODO: Generieren der unsicheren Werte von Lösung 4

    def _generate_uncertain_value_solution_5(self) -> None:
        """ Method to create an uncertain value of solution 5.
        """
        pass #TODO: Generieren der unsicheren Werte von Lösung 5

    def _generate_uncertain_value_solution_6(self, coin : IdentifiedNode, row_index : int, column_index : int) -> None:
        """ Method to create an uncertain value of solution 6.
        Attributes
        ----------
        coin : IdentifiedNode
            Node of the coin, which gets an uncertain value.
        row_index : int
            Row index of the uncertain value.
        column_index : int
            Column index of the uncertain value.
        """
        EDTFO = Namespace("https://periodo.github.io/edtf-ontology/edtfo.ttl")
        self.graph.bind("edtfo", EDTFO)

        node, predicate, object = self._get_node_predicate_object(coin, row_index, column_index)

        self.graph.add((coin, NMO[predicate], NM[object]))
        self.graph.add((node, RDF["object"], NM[object]))
        self.graph.add((node, RDF["subject"], coin))
        self.graph.add((node, RDF["predicate"], NMO[predicate]))
        self.graph.add((node, RDF["type"], EDTFO["UncertainStatement"]))

    def _generate_uncertain_value_solution_7(self, coin : IdentifiedNode, row_index : int, column_index : int) -> None:
        """ Method to create an uncertain value of solution 7.
        Attributes
        ----------
        coin : IdentifiedNode
            Node of the coin, which gets an uncertain value.
        row_index : int
            Row index of the uncertain value.
        column_index : int
            Column index of the uncertain value.
        """
        EDTFO = Namespace("https://periodo.github.io/edtf-ontology/edtfo.ttl")
        self.graph.bind("edtfo", EDTFO)

        node, predicate, object = self._get_node_predicate_object(coin, row_index, column_index)

        self.graph.add((coin, NMO[predicate], node))
        self.graph.add((node, RDF["type"], EDTFO["ApproximateStatement"]))
        self.graph.add((node, RDF.value, NM[object]))

    def _generate_uncertain_value_solution_8(self) -> None:
        """ Method to create an uncertain value of solution 8.
        """
        pass #TODO: Generieren der unsicheren Werte von Lösung 8


if __name__ == "__main__":
    from pathlib import Path
    from unco import UNCO_PATH

    dataset = Dataset(str(Path(UNCO_PATH,"tests/test_data/csv_testdata/eingabeformat.csv")))

    dataset.add_uncertainty_flags(list_of_columns=[2],uncertainties_per_column=1)
    generator = RDFGenerator(dataset)

    generator.load_prefixes(str(Path(UNCO_PATH,"tests/test_data/csv_testdata/namespaces.csv")))

    generator.generate_solution(0)

    # generator.generate_solution(7)
    # generator.generate_solution_6()
    # generator.generate_solution_7()
    

    # dataset.add_alternatives()

    # dataset.add_likelihoods()
    # generator = RDFGenerator(dataset)

    # generator.generate_solution_3()
    # generator.generate_solution_4()
    # generator.generate_solution_5()
    # generator.generate_solution_8()
