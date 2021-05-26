#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import time
import os


# In[12]:


PATH = "brazil/"
FILE_NAME = "Brazil.csv"


tempo_inicial = time.time()


# In[3]:


def extractDataframeByName(dataframe, location):
    print("Processing... 0%")
    all_names = dataframe[location].unique().tolist()

    number_of_names = len(all_names)
    counter = 0

    for name in all_names:
        counter += 1

        #print("Processing... {}  - {:.2f}%".format(name, (counter*100)/number_of_names))
        if (counter % 530 == 0):
            print("Processing... {:.0f}% ".format(
                (counter*100)/number_of_names))

        newDataframe = dataframe.loc[dataframe[location] == name]
        newDataframe.drop(newDataframe.index[0])
        newDataframe.reset_index(inplace=True)

        newDataframe.to_csv(f"{PATH}/{name}.csv", index=False)

        #newDataframe.to_json(f"{PATH}/{name}.json", orient ='values')


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


# In[35]:


# Regiao pro Brasil né? # Estado tem que dividr por 2
def splitDataframe2Something(dataframe, name):
    dataframe.data = [str(dataframe.data[i]).replace("/", "-")
                      for i in range(len(dataframe))]
    if (name == "estado"):
        newDataframe = dataframe.groupby([name, "data"])[
            ['casosAcumulado', 'casosNovos', 'obitosAcumulado', 'obitosNovos']].sum().apply(lambda x: divideByTwoWhenPossible(x))

    elif (name == "Brasil"):
        dataframe = dataframe.loc[dataframe["regiao"] == "Brasil"]
        newDataframe = dataframe[["data", "casosAcumulado",
                                  "casosNovos", "obitosAcumulado", "obitosNovos"]].copy()

    else:  # Municipios
        newDataframe = dataframe.groupby([name, "data"])[
            ['casosAcumulado', 'casosNovos', 'obitosAcumulado', 'obitosNovos']].sum()

    newDataframe.reset_index(inplace=True)
    newDataframe["daily_cases_moving_average"] = newDataframe['casosNovos'].rolling(
        window=7).mean()
    newDataframe["daily_deaths_moving_average"] = newDataframe['obitosNovos'].rolling(
        window=7).mean()
    newDataframe["sum_of_daily_cases_week"] = newDataframe['casosNovos'].rolling(
        window=7).sum()
    newDataframe["sum_of_daily_deaths_week"] = newDataframe['obitosNovos'].rolling(
        window=7).sum()

    return newDataframe


# In[38]:


def main():

    # def pre_processing_csv_data(file_name):
    unprocessedDataset = pd.read_csv(
        str(FILE_NAME), delimiter=";", error_bad_lines=False)

    cities = splitDataframe2Something(unprocessedDataset, "municipio")
    print("Cities")
    states = splitDataframe2Something(unprocessedDataset, "estado")
    states["estado"] = states["estado"].replace(['AC', 'AL', "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"], ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",  "Espírito Santo", "Goiás", "Maranhão",  "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"])

    print("States")

    brazil = splitDataframe2Something(unprocessedDataset, "Brasil")

    print("Brasil")
    brazil.to_csv(f"{PATH}/Brasil.csv", index=False)

    #brazil["data"] = changeDateOrder(brazil["data"])
    #brazil.to_json(f"{PATH}/Brasil.json", orient ='values')

    extractDataframeByName(cities, "municipio")
    extractDataframeByName(states, "estado")

    print("It took {:.2f} minutes".format((time.time() - tempo_inicial)/60))

    os.system("rm Brazil.csv")
    os.system("./upload2TheCloud.sh")


if __name__ == "__main__":
    main()

s
