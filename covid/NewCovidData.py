#!/usr/bin/python3
# coding: utf-8

# In[1]:


from multiprocessing import  Pool

import requests
import numpy as np
import pandas as pd
import time
import os

start = time.time()
PATH = "./brazil"


# In[ ]:


os.system("rm *.csv.gz")

print("Dowloading the data...")
# !wget ""
url = 'https://github.com/wcota/covid19br/raw/master/cases-brazil-cities-time.csv.gz'
r = requests.get(url, allow_redirects=True)
open("cases-brazil-cities-time.csv.gz", 'wb').write(r.content)


# In[ ]:


start = time.time()

dataframe  = pd.read_csv("cases-brazil-cities-time.csv.gz")
print("Data downloaded!")


# In[ ]:


print("Extracting city dataframes...")


# In[ ]:


def extractDataframeByCity(dataframe):
    print("Processing... 0%")
    all_names = dataframe.city.unique().tolist()
   
    number_of_names = int(len(all_names) /10)
    
    counter = 0

    for name in all_names:
        newDataframe = dataframe.loc[dataframe.city == name]
        newDataframe.reset_index(inplace=True)
        
        newDataframe.loc[:, "daily_cases_moving_average"] = newDataframe.newCases.rolling(window = 14).mean()
        newDataframe.loc[:, "daily_deaths_moving_average"] = newDataframe.newDeaths.rolling(window = 14).mean()

        counter +=1 
        
        new_name = "Brasil"
        try:
            buffer_name = name.split("/")
            new_name = buffer_name[0]
        except:
            pass

        if (counter % number_of_names == 0):
            print("Processing... {:.0f}% ".format((counter*10)/number_of_names))
        
        newDataframe.to_json(f"{PATH}/{new_name}.json")


# In[ ]:


extractDataframeByCity(dataframe)
print("Cities Processed!")


# # Vaccines

# In[2]:


print("Downloading vaccines dataset...")
url = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
dataframe = pd.read_csv(url,index_col=0,parse_dates=[0])
# dataframe

print("Vaccine Dataset downloaded!")


# In[3]:




dataframe.state = dataframe.state.replace(['AC', 'AL', "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO", "TOTAL"], ["Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",  "Espírito Santo", "Goiás", "Maranhão",  "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins", "Brasil"])
# dataframe.columns
dataframe


# In[4]:


def extractDataframeByState(dataframe):
    all_names = dataframe.state.unique().tolist()
    lenth = len(dataframe.state.unique().tolist())
    number_of_names = len(all_names)
    counter = 0

    for name in all_names:
        
        newDataframe = dataframe.loc[dataframe.state == name]
        newDataframe.drop(newDataframe.index[0])
        newDataframe.reset_index(inplace=True)
        
        dataframe.loc[:,"daily_cases_moving_average"] = dataframe["newCases"].rolling(window=7).mean()
        dataframe.loc[:, "daily_deaths_moving_average"] = dataframe["newDeaths"].rolling(window=7).mean()

        
        dataframe.loc[:,'daily_vaccine'] = dataframe['vaccinated'].diff()
        dataframe['daily_second_vaccine'] = dataframe['vaccinated_second'].diff()

        dataframe.loc[:,"vaccinated_moving_average"] = dataframe["daily_vaccine"].rolling(window=14).mean() 
        dataframe.loc[:,"vaccinated_second_moving_average"] = dataframe["daily_second_vaccine"].rolling(window=14).mean()
        
        dataframe.loc[:,"vaccinated_moving_average"] = dataframe["vaccinated"].rolling(window=7).mean()
        dataframe.loc[:,"vaccinated_second_moving_average"] = dataframe["vaccinated_second"].rolling(window=7).mean()

        newDataframe.to_json(f"{PATH}/{name}.json")
extractDataframeByState(dataframe)


# In[11]:


brasil = []
brasil =  dataframe.loc[dataframe["state"] == "Brasil"]
brasil["daily_cases_moving_average"] = brasil["newCases"].rolling(window=14).mean()
brasil["daily_deaths_moving_average"] = brasil["newDeaths"].rolling(window=14).mean()

brasil['daily_vaccine'] = brasil['vaccinated'].diff()
brasil['daily_second_vaccine'] = brasil['vaccinated_second'].diff()

brasil["vaccinated_moving_average"] = brasil["daily_vaccine"].rolling(window=14).mean() 
brasil["vaccinated_second_moving_average"] = brasil["daily_second_vaccine"].rolling(window=14).mean()
        
brasil.reset_index(inplace=True)
brasil.to_json(f"{PATH}/Brasil.json")


# In[10]:


brasil


# In[12]:


os.system("rm *.csv.gz")

os.system("./upload2TheCloud.sh")

print("It took {:.2f} minutes".format((time.time() - start)/60))


# In[ ]:




