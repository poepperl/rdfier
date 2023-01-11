import pandas as pd
from cmath import nan
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
        self.node_counter = 1

        self.graph.bind("nm", NM)
        self.graph.bind("nmo", NMO)
        self.graph.bind("un", UN)
        self.graph.bind("foaf", FOAF)

    def generate_solution_1(self) -> None:
        """ Method to generate the RDF-XML file of solution 1.
        """
        pass #TODO: Generieren des Graphs von Lösung 1

    def generate_solution_2(self) -> None:
        """ Method to generate the RDF-XML file of solution 2.
        """
        coin_ids = self.dataset.data[self.dataset.data.columns[0]] # Get the list of id's

        for row_index, id in enumerate(coin_ids):
            coin = URIRef("node_" + str(row_index))
            
            self.graph.add((coin, NMO.hasObjectType, NM.coin))
            self.graph.add((coin, FOAF.name, Literal("Coin_" + str(id))))

            for column_index in range(1, len(self.dataset.data.columns)):
                if pd.notnull(self.dataset.data.iat[row_index,column_index]): # Check if value isn't NaN

                    predicate = Literal("has" + str(self.dataset.data.columns[column_index]))

                    object = Literal(self.dataset.data.iat[row_index,column_index])

                    if column_index in self.dataset.uncertainty_flags:
                        if row_index in self.dataset.uncertainty_flags[column_index]:
                            print("Uncertainty at row " + str(row_index) + " and column " + str(column_index))
                            node = BNode(str(self.dataset.data.columns[column_index]) + self.dataset.data.iat[row_index,column_index])
                            self.node_counter += 1
                            self.graph.add((coin, NMO[predicate], node))
                            self.graph.add((node, UN.hasUncertainty, NM.uncertain_value))
                            self.graph.add((node, RDF.value, NM[object]))
                            continue

                    self.graph.add((coin, NMO[predicate], NM[object]))


    def generate_solution_3(self) -> None:
        """ Method to generate the RDF-XML file of solution 3.
        """
        pass #TODO: Generieren des Graphs von Lösung 3

    def generate_solution_4(self) -> None:
        """ Method to generate the RDF-XML file of solution 4.
        """
        pass #TODO: Generieren des Graphs von Lösung 4

    def generate_solution_5(self) -> None:
        """ Method to generate the RDF-XML file of solution 5.
        """
        pass #TODO: Generieren des Graphs von Lösung 5

    def generate_solution_6(self) -> None:
        """ Method to generate the RDF-XML file of solution 6.
        """
        pass #TODO: Generieren des Graphs von Lösung 6

    def generate_solution_7(self) -> None:
        """ Method to generate the RDF-XML file of solution 7.
        """
        pass #TODO: Generieren des Graphs von Lösung 7

    def generate_solution_8(self) -> None:
        """ Method to generate the RDF-XML file of solution 8.
        """
        pass #TODO: Generieren des Graphs von Lösung 8

if __name__ == "__main__":
    dataset = Dataset(r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\cointest_5.csv")

    dataset.add_uncertainty_flags(list_of_columns=[2],uncertainties_per_column=4)
    generator = RDFGenerator(dataset)

    # generator.generate_solution_1()
    generator.generate_solution_2()
    # generator.generate_solution_6()
    # generator.generate_solution_7()
    

    # dataset.add_alternatives()

    # dataset.add_likelihoods()
    # generator = RDFGenerator(dataset)

    # generator.generate_solution_3()
    # generator.generate_solution_4()
    # generator.generate_solution_5()
    # generator.generate_solution_8()
