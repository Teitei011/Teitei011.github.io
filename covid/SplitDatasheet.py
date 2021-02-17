# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 14:33:31 2021

@author: stefa
"""


import time
import os

import pandas as pd



tempo_inicial = time.time()

def determine_state_city_or_country(name):
    '''
        This is a hack that only work on this specific scenario
    '''
    if (len(name) == 2):
        return "state"
    elif(name == "Brazil"):
        return "Brazil"
    else:
        return "city"



def get_data(dataframe, name):
    index_ = determine_state_city_or_country(name)
    result_dataframe =  dataframe[dataframe[index_].isin([name])]
    
    result_dataframe.loc[:,"daily cases moving average"] = result_dataframe['daily cases'].rolling(window=14).mean() 
    result_dataframe.loc[:,"daily deaths moving average"] = result_dataframe['daily deaths'].rolling(window=14).mean() 
    result_dataframe.loc[:,"sum_of_daily_cases_week"] = result_dataframe['daily cases'].rolling(window=7).sum() 
    result_dataframe.loc[:,"sum_of_daily_deaths_week"] = result_dataframe['daily deaths'].rolling(window=7).sum() 
    result_dataframe.to_csv(f"{name}.csv", index=False)

    
def separate_each_city_on_dataframe(dataframe):
    # set the index to be this and don't drop
    dataframe.set_index(keys=['city'], drop=False,inplace=True)
    
    # get a list of names
    city_names = dataframe['city'].unique().tolist()

    
    # now we can perform a lookup on a 'view' of the dataframe
    counter = 0
    for city in city_names:
        counter += 1
        print("Processing: {}  - {:.2f}% ...".format(city, counter*100/5297))
        buffer_dataframe = dataframe.loc[dataframe.city==city]
        buffer_dataframe.loc[:, "daily cases moving average"] = buffer_dataframe['daily cases'].rolling(window=7).mean() 
        buffer_dataframe.loc[:, "daily deaths moving average"] =   buffer_dataframe['daily deaths'].rolling(window=7).mean() 
        
        buffer_dataframe.loc[:,"sum_of_daily_cases_week"] = buffer_dataframe['daily cases'].rolling(window=7).sum() 
        buffer_dataframe.loc[:,"sum_of_daily_deaths_week"] = buffer_dataframe['daily deaths'].rolling(window=7).sum() 
        
        buffer_dataframe.drop(buffer_dataframe.index[0])
        buffer_dataframe.to_csv(f"brazil/{city}.csv", index=False)


def createADataframeToEachState(dataframe):
    all_states_name = dataframe["state"].unique()

    for state in all_states_name:
        print(f"Processing {state}...")
        buffer_dataframe = dataframe.loc[dataframe.state==state]
        buffer_dataframe.loc[:, "daily cases moving average"] = buffer_dataframe['daily cases'].rolling(window=7).mean() 
        buffer_dataframe.loc[:, "daily deaths moving average"] =   buffer_dataframe['daily deaths'].rolling(window=7).mean() 
        
        buffer_dataframe.loc[:,"sum_of_daily_cases_week"] = buffer_dataframe['daily cases'].rolling(window=7).sum() 
        buffer_dataframe.loc[:,"sum_of_daily_deaths_week"] = buffer_dataframe['daily deaths'].rolling(window=7).sum() 
        
        buffer_dataframe.drop(buffer_dataframe.index[0])
        buffer_dataframe.to_csv(f"brazil/{state}.csv", index=False)

def divideByTwoWhenPossible(array):
    for i in range(len(array)):
        try:
            array[i] = array[i] / 2
        except:
            pass
    return array

file_name = "brazil.csv"
#def pre_processing_csv_data(file_name):
unprocessedDataset = pd.read_csv(str(file_name), delimiter=";", error_bad_lines=False)

city = unprocessedDataset.groupby(["municipio", "data"])[['casosAcumulado', 'casosNovos', 'obitosAcumulado', 'obitosNovos']].sum()
city = city.rename(columns={"municipio": "city", "data": "date", 'casosAcumulado': 'cases', 'obitosAcumulado': 'deaths', 'casosNovos' : "daily cases", "obitosNovos": "daily deaths"})


state = unprocessedDataset.groupby(["estado", "data"])[['casosAcumulado', 'casosNovos', 'obitosAcumulado', 'obitosNovos']].sum().apply(lambda x: divideByTwoWhenPossible(x))
state = state.rename(columns={"estado": "state", "data": "date", 'casosAcumulado': 'cases', 'obitosAcumulado': 'deaths', 'casosNovos' : "daily cases", "obitosNovos": "daily deaths"})

city.to_csv("brazil/brazil_cities.csv")
state.to_csv("brazil/brazil_states.csv")


del city
del state

cities = pd.read_csv("brazil/brazil_cities.csv")
states = pd.read_csv("brazil/brazil_states.csv")

cities = cities.rename(columns={"municipio": "city", "data": "date"})
states = states.rename(columns={"estado": "state", "data": "date"})

unprocessedDataset = unprocessedDataset.loc[unprocessedDataset["regiao"] == "Brasil"]
unprocessedDataset = unprocessedDataset.rename(columns={"data": "date", 'casosAcumulado': 'cases', 'obitosAcumulado': 'deaths', 'casosNovos' : "daily cases", "obitosNovos": "daily deaths"})

print("Creating Brazil Dataset...")

brazil = unprocessedDataset[["date", "cases", "daily cases", "deaths", "daily deaths"]].copy()

brazil["daily cases moving average"] = brazil['daily cases'].rolling(window=7).mean()
brazil["daily deaths moving average"] = brazil['daily deaths'].rolling(window=7).mean()
brazil.loc[:,"sum_of_daily_cases_week"] = brazil['daily cases'].rolling(window=7).sum() 
brazil.loc[:,"sum_of_daily_deaths_week"] = brazil['daily deaths'].rolling(window=7).sum() 

brazil.to_csv("brazil/Brasil.csv")
brazil.to_csv("Brasil.csv")
os.system("./upload2TheCloud.sh")


separate_each_city_on_dataframe(cities)
createADataframeToEachState(states)




print("It took {:.2f} minutes".format((time.time() - tempo_inicial)/60) )
