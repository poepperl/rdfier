import streamlit.web.bootstrap

def main():
    print("|--- Welcome to UnCo. What do you want to do? ---|")
    print("|--- 0 - Start a benchmark                    ---|")
    print("|--- 1 - Start RDFier                         ---|")
    mode = input(">>>> Choose the mode (0):")
    if mode == "1":
        streamlit.web.bootstrap.run("src/app/RDFier.py", "", [], [])
    elif mode == "0":
        increasing_alternatives = None
        modellist = None
        querylist = None
        x_range: range = range(0, 301, 30)

        while increasing_alternatives not in ["0", "1", ""]:
            print("|--- Input your parameters:                   ---|")
            print("|---                                          ---|")
            print("|--- Increase alternatives?                   ---|")
            print("|--- 0 - Set mode to increasing uncertainties ---|")
            print("|--- 1 - Set mode to increasing uncertainties ---|")
            increasing_alternatives = input(">>>> Choose your mode (0):").strip()
            if increasing_alternatives not in ["0", "1", ""]: print("!!!! Wrong input!                             !!!!")
        
        increasing_alternatives = 0 if increasing_alternatives == "" else int(increasing_alternatives)
        
        while not all(ids in [1,2,3,4,5,6,7,8,9,10] for ids in modellist):
            print("|---                                          ---|")
            print("|--- Choose the list of models.               ---|")
            print("|--- Numbers from 1 to 10 separated by commas ---|")
            modellist = map(int, input(">>>> Choose the models (all):").split(","))
            if not all(ids in [1,2,3,4,5,6,7,8,9,10] for ids in modellist): print("!!!! Wrong input!                             !!!!")
        
        if not modellist: modellist = [1,2,3,4,5,6,7,8,9,10]

        while not all(ids in [1,2,3,4,5,6] for ids in querylist):
            print("|---                                          ---|")
            print("|--- Choose the list of queries.              ---|")
            print("|--- Numbers from 1 to 6 separated by commas  ---|")
            querylist = map(int, input(">>>> Choose the queries (all):").split(","))
            if not all(ids in [1,2,3,4,5,6] for ids in querylist): print("!!!! Wrong input!                             !!!!")

        if not querylist: querylist = [1,2,3,4,5,6]

        while not x_range:
            print("|---                                          ---|")
            print("|--- Choose the range of increasing.          ---|")
            print("|--- Defined by start, stop and step.         ---|")
            start = input(">>>> Set start (0):")
            stop = input(">>>> Set stop (301):")
            step = input(">>>> Set step (30):")
            start = 0 if start == "" else int(start)
            stop = 301 if stop == "" else int(stop)
            step = 30 if step == "" else int(step)
            x_range = range(start, stop, step)
            if not x_range: print("!!!! Wrong input!                             !!!!")

if __name__ == "__main__":
    main()