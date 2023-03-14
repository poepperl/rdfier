import os
from unco import UNCO_PATH
from unco.data import RDFData

if __name__ == "__main__":
    INPUT_PATH = os.path.join(UNCO_PATH, r"data\input")

    output_datasets = []

    for file in os.listdir(INPUT_PATH):
        dataset = RDFData(os.path.join(INPUT_PATH,file))
        dataset.add_uncertainty_flags()
        dataset.add_alternatives()
        dataset.add_likelihoods()

        output_datasets.append(dataset)