import streamlit.web.bootstrap
import pandas as pd
from unco.data import RDFData
from src.benchmark.benchmark import Benchmark
from unco import UNCO_PATH
from pathlib import Path
from time import time

def benchmark():
    """
    Runs an UnCo benchmark.
    """
    fuseki_path = ""
    path = ""
    increasing_alternatives = None
    columnlist = [None]
    modellist = [None]
    querylist = [None]
    x_range: range = None

    all_model_ids = ["1","2","3","4","5","6","7","8","9","10"]
    all_query_ids = ["1","2","3","4","5","6"]

    while not Path(fuseki_path, "fuseki-server.jar").is_file():
        print("|--- Input your parameters:                    ---|")
        print("|---                                           ---|")
        print("|--- Select the fuseki server folder.          ---|")
        fuseki_path = input(">>>> Insert the path (src/apache-jena-fuseki-4.8.0):").strip()
        if fuseki_path == "Q": quit()
        if fuseki_path == "":
            fuseki_path = str(Path(UNCO_PATH,"src/apache-jena-fuseki-4.8.0"))
        
        if not Path(fuseki_path, "fuseki-server.jar").is_file():
            print("!!!! Doesn`t found fueski-server.jar           !!!!")


    while not Path(path).is_file() and path[-4:] != ".csv":
        print("|---                                           ---|")
        print("|--- Select the input csv-file.                ---|")
        path = input(">>>> Insert the path (example input):").strip()
        if path == "Q": quit()
        if path == "":
            path = str(Path(UNCO_PATH,"data/example_input.csv"))
        
        if not Path(path).is_file() and path[-4:] != ".csv":
            print("!!!! There is no csv-file on this path!        !!!!")

    rdf_data = RDFData(pd.read_csv(path))
    path = ""

    while not Path(path).is_file() and path[-4:] != ".csv":
        print("|---                                           ---|")
        print("|--- Select the namespaces csv-file.           ---|")
        path = input(">>>> Insert a input path (example namespaces):").strip()
        if path == "Q": quit()
        if path == "":
            path = str(Path(UNCO_PATH,"data/input/namespaces.csv"))
        
        if not Path(path).is_file() and path[-4:] != ".csv":
            print("!!!! There is no csv-file on this path!        !!!!")

    bench = Benchmark(rdf_data, path, )
    del rdf_data

    while increasing_alternatives not in ["0", "1", ""]:
        print("|---                                           ---|")
        print("|--- Which parameter should be increased each  ---|")
        print("|--- step?                                     ---|")
        print("|--- 0 - Set mode to increasing uncertainties  ---|")
        print("|--- 1 - Set mode to increasing alternatives   ---|")
        increasing_alternatives = input(">>>> Choose your mode (0):").strip()
        if increasing_alternatives == "Q": quit()
        if increasing_alternatives not in ["0", "1", ""]: print("!!!! Wrong input!                              !!!!")
    
    increasing_alternatives = False if increasing_alternatives == "" else bool(int(increasing_alternatives))

    set_of_columns = {str(i) for i in range(len(bench.graph_generator.rdfdata.data.columns))}

    while not all(cols in set_of_columns for cols in columnlist):
        print("|---                                           ---|")
        print("|--- Select the columns to be changed each step---|")
        print("|--- Numbers of column ids seperated by commas ---|")
        columnlist = [number.strip() for number in input(">>>> Choose the columns (2, 3, 4, 7, 10, 16, 17, 18, 19):").split(",")]
        if columnlist == ["Q"]: quit()
        if columnlist == [""]: columnlist = ["2", "3", "4", "7", "10", "16", "17", "18", "19"]

        if not all(cols in set_of_columns for cols in columnlist): print("!!!! Wrong column indices!                     !!!!")
    
    del set_of_columns
    columnlist = list(map(int, columnlist))
    
    while not all(ids in all_model_ids for ids in modellist):
        print("|---                                           ---|")
        print("|--- Choose the list of models.                ---|")
        print("|--- Numbers from 1 to 10 separated by commas  ---|")
        modellist = [number.strip() for number in input(">>>> Choose the models (all):").split(",")]
        if modellist == ["Q"]: quit()
        if modellist == [""]: modellist = all_model_ids
        if not all(ids in all_model_ids for ids in modellist): print("!!!! Wrong input!                              !!!!")
    
    modellist = list(map(int, modellist))

    while not all(ids in all_query_ids for ids in querylist):
        print("|---                                           ---|")
        print("|--- Choose the list of queries.               ---|")
        print("|--- Numbers from 1 to 6 separated by commas   ---|")
        querylist = [number.strip() for number in input(">>>> Choose the queries (all):").split(",")]
        if querylist == ["Q"]: quit()
        if querylist == [""]: querylist = all_query_ids
        if not all(ids in all_query_ids for ids in querylist): print("!!!! Wrong input!                              !!!!")

    querylist = list(map(int, querylist))

    while not x_range:
        print("|---                                           ---|")
        print("|--- Choose the range of increasing.           ---|")
        print("|--- Defined by Integers start, stop and step: ---|")
        start = input(">>>> Set start (0):")
        if start == "Q": quit()
        stop = input(">>>> Set stop (1):")
        if stop == "Q": quit()
        step = input(">>>> Set step (1):")
        if step == "Q": quit()

        start = 0 if start == "" else start
        stop = 1 if stop == "" else stop
        step = 1 if step == "" else step

        try:
            start, stop, step = int(start), int(stop), int(step)
        except ValueError:
            print("!!!! Wrong input! Found non-integer values!    !!!!")
            continue

        if step < 1:
            print("!!!! Step must be greater than 0!              !!!!")
            continue
        if stop <= start:
            print("!!!! Stop must be greater than start!          !!!!")
            continue
        x_range = range(start, stop, step)
        if not x_range:
            print("!!!! Range must contain at least one number!   !!!!")
    
    full_time = time()

    print(bench.run_benchmarktest(increasing_alternatives=increasing_alternatives, increasing_columns=columnlist, querylist=querylist, modellist=modellist, x_range=x_range))

    print(f"full runtime: {'%.0f' % (time()-full_time)} seconds")

def main():
    """
    Main function of UnCo, to start RDFier or a benchmark.
    """
    mode = None
    while mode not in ["0", "1", "Q"]:
        print("|--- Welcome to UnCo. What do you want to do?  ---|")
        print("|--- 0 - Start a benchmark                     ---|")
        print("|--- 1 - Start RDFier                          ---|")
        print("|--- Q - Quit (you can quit in every step)     ---|")
        mode = input(">>>> Choose the mode (0):")
        if not mode: mode = "0"
        if mode not in ["0", "1", "Q"]: print("!!!! Wrong input!                              !!!!")

    if mode == "1":
        streamlit.web.bootstrap.run("src/rdfier_app/RDFier.py", "", [], [])
    elif mode == "0":
        benchmark()
        _ = input("Press any key to close the terminal...")

if __name__ == "__main__":
    main()