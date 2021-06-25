#!/usr/bin/env python
# coding: utf-8

# In[1]:


from multiprocessing import  Pool

import numpy as np
import pandas as pd
import time
import os

start = time.time()
PATH = "./brazil"


# In[2]:


os.system("wget https://github.com/wcota/covid19br/blob/master/cases-brazil-cities-time.csv.gz")


# In[3]:


dataframe  = pd.read_csv("./cases-brazil-cities-time.csv.gz")
# dataframe


# In[4]:


dataframe["daily_cases_moving_average"] = dataframe['newCases'].rolling(window=14).mean()
dataframe["daily_deaths_moving_average"] = dataframe['newDeaths'].rolling(window=14).mean()


# In[9]:


def extractDataframeByCity(dataframe):
    all_names = dataframe.city.unique().tolist()
    lenth = len(dataframe.state.unique().tolist())
    number_of_names = len(all_names)
    counter = 0

    for name in all_names:
        newDataframe = dataframe.loc[dataframe.state == name]
        newDataframe.reset_index(inplace=True)
        
        
        counter +=1 
        
        new_name = "Brasil"
        try:
            buffer_name = name.split("/")
            new_name = buffer_name[0]
        except:
            pass
        
        print(counter)
        
        newDataframe.to_json(f"{PATH}/{new_name}.json")


# In[10]:


extractDataframeByCity(dataframe)


# # Vaccines

# In[11]:


url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
dataframe = pd.read_csv(url,index_col=0,parse_dates=[0])
# dataframe


# In[12]:


# dataframe.state.unique().tolist()

dataframe["daily_cases_moving_average"] = dataframe['newCases'].rolling(window=14).mean()
dataframe["daily_deaths_moving_average"] = dataframe['newDeaths'].rolling(window=14).mean()

dataframe["vaccinated_moving_average"] = dataframe['vaccinated'].rolling(window=14).mean()
dataframe["vaccinated_second_moving_average"] = dataframe['vaccinated_second'].rolling(window=14).mean()

dataframe.state = dataframe.state.replace(['AC', 'AL', "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO", "TOTAL"], ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",  "Espírito Santo", "Goiás", "Maranhão",  "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins", "Brasil"])
# dataframe.columns


# In[13]:


def extractDataframeByState(dataframe):
    all_names = dataframe.state.unique().tolist()
    lenth = len(dataframe.state.unique().tolist())
    number_of_names = len(all_names)
    counter = 0

    for name in all_names:
        newDataframe = dataframe.loc[dataframe.state == name]
        newDataframe.drop(newDataframe.index[0])
        newDataframe.reset_index(inplace=True)

        newDataframe.to_json(f"{PATH}/{name}.json")
extractDataframeByState(dataframe)


# In[14]:


os.system("rm *.csv.gz")

os.system("./upload2TheCloud.sh")

print("It took {:.2f} minutes".format((time.time() - start)/60))


# In[ ]:




