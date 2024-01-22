import matplotlib.pyplot as plt 
#Petit tuto pour apprendre à utiliser la base de donnée stats_pokemons.db 
#La lecture de la base de donnée se fait via des commandes en SQL et les deux bibliothèques suivantes :
import pandas as pd
import sqlite3 
conn = sqlite3.connect('stats_pokemons/stats_pokemons.db') #Outil permettant d'exploiter la base de données

def dict_to_list(dict):
    #Transforme un dictionnaire en liste de listes    
    list = []
    for key, value in dict.items():
        list.append([key, value])
    return list

data_file = 'usage/gen7ou-0.json'
df_gen7 = pd.read_json(data_file)
df_gen7 = df_gen7.transpose()
df_gen7 = df_gen7.applymap(lambda cell: dict_to_list(cell) if isinstance(cell, dict) else cell)
df_gen7 = df_gen7.loc[:, ['usage']]

print(df_gen7)

data_file = 'usage/gen8ou-0.json'
df_gen8 = pd.read_json(data_file)
df_gen8 = df_gen8.transpose()
df_gen8 = df_gen8.applymap(lambda cell: dict_to_list(cell) if isinstance(cell, dict) else cell)
df_gen8 = df_gen8.loc[:, ['usage']]

data_file = 'usage/gen9ou-0.json'
df_gen9 = pd.read_json(data_file)
df_gen9 = df_gen9.transpose()
df_gen9 = df_gen9.applymap(lambda cell: dict_to_list(cell) if isinstance(cell, dict) else cell)
df_gen9 = df_gen9.loc[:, ['usage']]