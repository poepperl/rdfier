import pandas as pd
from typing import Literal
from unco.data.dataset import Dataset
from rdflib import Graph, Namespace, BNode, Literal, URIRef
from rdflib.namespace import RDF, FOAF

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

        self.graph.bind("nm", NM)
        self.graph.bind("nmo", NMO)
        self.graph.bind("un", UN)
        self.graph.bind("foaf", FOAF)

    def generate_solution(self,solution_id):
        """ Method to generate the RDF-XML file.
        """
        coin_ids = self.dataset.data[self.dataset.data.columns[0]] # Get the list of id's

        for row_index, id in enumerate(coin_ids):
            coin = URIRef("Coin_" + str(id))
            self.graph.add((coin, NMO.hasObjectType, NM.coin)) # Coin_X gets ObjectType Coin

            for column_index in range(1, len(self.dataset.data.columns)):
                if pd.notnull(self.dataset.data.iat[row_index,column_index]): # Check if value isn't NaN

                    predicate = Literal("has" + str(self.dataset.data.columns[column_index]))

                    object = Literal(self.dataset.data.iat[row_index,column_index])

                    if column_index in self.dataset.uncertainty_flags:
                        if row_index in self.dataset.uncertainty_flags[column_index]: # If current value is uncertain, do:
                            match solution_id:
                                case 1:
                                    self._generate_uncertain_value_solution_1()
                                case 2:
                                    self._generate_uncertain_value_solution_2(coin, predicate, str(self.dataset.data.columns[column_index]) + self.dataset.data.iat[row_index,column_index])
                                case 3:
                                    self._generate_uncertain_value_solution_3()
                                case 4:
                                    self._generate_uncertain_value_solution_4()
                                case 5:
                                    self._generate_uncertain_value_solution_5()
                                case 6:
                                    self._generate_uncertain_value_solution_6()
                                case 7:
                                    self._generate_uncertain_value_solution_7()
                                case 8:
                                    self._generate_uncertain_value_solution_8()
                            continue

                    self.graph.add((coin, NMO[predicate], NM[object])) # Example: Coin_4 hasMaterial ar
        
    def _generate_uncertain_value_solution_1(self) -> None:
        """ Method to create an uncertain value of solution 1.
        """
        pass #TODO: Generieren der unsicheren Werte von Lösung 1

    def _generate_uncertain_value_solution_2(self, coin, predicate, nodename : str) -> None:
        """ Method to create an uncertain value of solution 2.
        """
        node = BNode(nodename)

        self.graph.add((coin, NMO[predicate], node))
        self.graph.add((node, UN.hasUncertainty, NM.uncertain_value))
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

    def _generate_uncertain_value_solution_6(self) -> None:
        """ Method to create an uncertain value of solution 6.
        """
        pass #TODO: Generieren der unsicheren Werte von Lösung 6

    def _generate_uncertain_value_solution_7(self) -> None:
        """ Method to create an uncertain value of solution 7.
        """
        pass #TODO: Generieren der unsicheren Werte von Lösung 7

    def _generate_uncertain_value_solution_8(self) -> None:
        """ Method to create an uncertain value of solution 8.
        """
        pass #TODO: Generieren der unsicheren Werte von Lösung 8

if __name__ == "__main__":
    dataset = Dataset(r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\cointest_5.csv")

    dataset.add_uncertainty_flags(list_of_columns=[2],uncertainties_per_column=4)
    generator = RDFGenerator(dataset)

    # generator.generate_solution_1()
    generator.generate_solution(2)
    print(generator.graph.serialize())
    # generator.generate_solution_6()
    # generator.generate_solution_7()
    

    # dataset.add_alternatives()

    # dataset.add_likelihoods()
    # generator = RDFGenerator(dataset)

    # generator.generate_solution_3()
    # generator.generate_solution_4()
    # generator.generate_solution_5()
    # generator.generate_solution_8()
