import csv
import random
from src.unco.data import Reader


class Dataset:
    """
        Class that adds a perturbation by creating random uncertainty.
    """

    data: csv

    def __init__(self, path: str) -> None:
        self.data = Reader(path).read()

    def add_uncertainty(self) -> None:
        # get random number of uncertainties between 1 and the number of rows
        number_of_uncertainties = random.randrange(1, len(next(self.data)))


p = Dataset(r"D:\Dokumente\Repositories\unco\tests\test_data\csv_testdata\unittest_reader.csv")
