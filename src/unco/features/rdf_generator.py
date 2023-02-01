import os
import pandas as pd
from typing import Literal, Tuple
from unco import UNCO_PATH
from unco.data.dataset import Dataset
from rdflib import Graph, Namespace, BNode, Literal, URIRef, IdentifiedNode
from rdflib.namespace import RDF

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
        self.output_folder = os.path.join(UNCO_PATH, r"data\output")

        self.graph.bind("rdf", RDF)
        self.graph.bind("nm", NM)
        self.graph.bind("nmo", NMO)
        self.graph.bind("un", UN)

    def generate_solution(self,solution_id : int) -> None:
        """ 
            Method to generate the RDF-XML file.

        Attributes
        ----------
        solution_id : int
            Solution id, which should be generated.
        """
        coin_ids = self.dataset.data[self.dataset.data.columns[0]] # Get the list of id's

        for row_index, id in enumerate(coin_ids):

            coin = URIRef("Coin_" + str(id))
            self.graph.add((coin, NMO.hasObjectType, NM.coin)) # Coin gets ObjectType Coin

            for column_index in range(1, len(self.dataset.data.columns)):

                if pd.notnull(self.dataset.data.iat[row_index,column_index]): # Check if value isn't NaN
                    if column_index in self.dataset.uncertainty_flags:
                        if row_index in self.dataset.uncertainty_flags[column_index]: # If current value is uncertain, do:

                            match solution_id:
                                case 1:
                                    self._generate_uncertain_value_solution_1(coin, row_index, column_index)
                                case 2:
                                    self._generate_uncertain_value_solution_2(coin, row_index, column_index)
                                case 3:
                                    self._generate_uncertain_value_solution_3()
                                case 4:
                                    self._generate_uncertain_value_solution_4()
                                case 5:
                                    self._generate_uncertain_value_solution_5()
                                case 6:
                                    self._generate_uncertain_value_solution_6(coin, row_index, column_index)
                                case 7:
                                    self._generate_uncertain_value_solution_7(coin, row_index, column_index)
                                case 8:
                                    self._generate_uncertain_value_solution_8()
                            continue
                    
                    predicate = Literal("has" + str(self.dataset.data.columns[column_index]))
                    object = Literal(self.dataset.data.iat[row_index,column_index])

                    self.graph.add((coin, NMO[predicate], NM[object])) # Example: Coin_4 hasMaterial ar
        
        with open(os.path.join(self.output_folder, str(solution_id) + ".ttl"), 'w') as file:
            file.write(generator.graph.serialize(format="ttl"))
        
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

    def _get_node_predicate_object(self, coin : IdentifiedNode, row_index : int, column_index : int) -> Tuple[BNode, Literal, Literal]:
        node = BNode(str(self.dataset.data.columns[column_index]) + self.dataset.data.iat[row_index,column_index])
        predicate = Literal("has" + str(self.dataset.data.columns[column_index]))
        object = Literal(self.dataset.data.iat[row_index,column_index])

        return node, predicate, object

if __name__ == "__main__":
    dataset = Dataset(r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\cointest_5.csv")

    dataset.add_uncertainty_flags(list_of_columns=[2],uncertainties_per_column=1)
    generator = RDFGenerator(dataset)

    generator.generate_solution(7)
    # generator.generate_solution_6()
    # generator.generate_solution_7()
    

    # dataset.add_alternatives()

    # dataset.add_likelihoods()
    # generator = RDFGenerator(dataset)

    # generator.generate_solution_3()
    # generator.generate_solution_4()
    # generator.generate_solution_5()
    # generator.generate_solution_8()
