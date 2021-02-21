import multiprocessing as mp
import pandas as pd
import time
import os
#import numba

PATH = "brazil/"
FILE_NAME = "Brazil.csv"

#@jit(nopython=True, parallel=True)
def extractDataframeByName(dataframe, location):
    print("Processing... 0%")
    all_names = dataframe[location].unique().tolist()

    number_of_names = len(all_names)
    counter = 0

    for name in all_names:
        counter +=1 

        #print("Processing... {}  - {:.2f}%".format(name, (counter*100)/number_of_names))
        if (counter % 530 == 0):
            print("Processing... {:.2f}%".format( (counter*100)/number_of_names))


        newDataframe = dataframe.loc[dataframe[location] == name]
        newDataframe.drop(newDataframe.index[0])
        newDataframe.to_csv(f"{PATH}/{name}.csv", index=False)


def divideByTwoWhenPossible(array):
    for i in range(len(array)):
        try:
            array[i] = array[i] / 2
        except:
            pass
    return array


def changeDateOrder(array):
    newArray = []
    for date in array:
        buffer = date.split("-")
        newArray.append(buffer[2] + "-" + buffer[1] + "-" + buffer[0])
    return newArray

def splitDataframe2Something(dataframe, name): # Regiao pro Brasil né? # Estado tem que dividr por 2

    if (name == "estado"):
        newDataframe = dataframe.groupby([name, "data"])[['casosAcumulado', 'casosNovos', 'obitosAcumulado', 'obitosNovos']].sum().apply(lambda x: divideByTwoWhenPossible(x))
    elif (name == "Brasil"):
        dataframe = dataframe.loc[dataframe["regiao"] == "Brasil"]
        newDataframe = dataframe[["data", "casosAcumulado", "casosNovos", "obitosAcumulado", "obitosNovos"]].copy()
 
    else: # Municipios
         newDataframe = dataframe.groupby([name, "data"])[['casosAcumulado', 'casosNovos', 'obitosAcumulado', 'obitosNovos']].sum()
    
    newDataframe.reset_index(inplace = True)
    newDataframe["data"] = changeDateOrder(newDataframe["data"])
    newDataframe["daily cases moving average"] = newDataframe['casosNovos'].rolling(window=7).mean()
    newDataframe["daily deaths moving average"] = newDataframe['obitosNovos'].rolling(window=7).mean()
    newDataframe["sum_of_daily_cases_week"] = newDataframe['casosNovos'].rolling(window=7).sum() 
    newDataframe["sum_of_daily_deaths_week"] = newDataframe['obitosNovos'].rolling(window=7).sum() 

    
    return newDataframe

def main():
    tempo_inicial = time.time()

    #def pre_processing_csv_data(file_name):
    unprocessedDataset = pd.read_csv(str(FILE_NAME), delimiter=";", error_bad_lines=False)

    cities = splitDataframe2Something(unprocessedDataset, "municipio")
    states = splitDataframe2Something(unprocessedDataset, "estado")
    brazil = splitDataframe2Something(unprocessedDataset, "Brasil")
    brazil.to_csv(f"{PATH}/Brasil.csv", index=False)

    extractDataframeByName(cities, "municipio")
    extractDataframeByName(states, "estado")

    print("It took {:.2f} minutes".format((time.time() - tempo_inicial)/60) )

    os.system("rm Brazil.csv")
    os.system("./upload2TheCloud.sh")

if __name__ == "__main__":
    main()