import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt


def name_doc(document): #take a document.extention, return it's name without the extension
    for i in range(1,len(document)):
        if document[len(document)-i] == '.':
            return document[:len(document)-i]

def refresh_database_csv():
    path = 'stats_pokemons/'
    list_doc = ['gen01.csv','gen02.csv','gen03.csv','gen04.csv','gen05.csv','gen06.csv','gen07.csv','gen08.csv','gen09.csv','Pokemon.csv']
    database = 'STNUM_pokemon.db'
    engine = create_engine('sqlite:///' + database)
    for doc in list_doc:
        df = pd.read_csv(path + doc)
        df.to_sql(name_doc(doc), engine, index=False, if_exists='replace')
            
        print(doc + " has been updated")

def refresh_database_json():
    path = 'usage/'
    list_doc = ['gen1ou-0.json','gen2ou-0.json','gen3ou-0.json','gen4ou-0.json','gen5ou-0.json','gen6ou-0.json','gen7ou-0.json','gen8ou-0.json','gen9ou-0.json']
    database = 'STNUM_pokemon.db'
    engine = create_engine('sqlite:///' + database)
    for doc in list_doc:
        df = pd.read_json(path + doc)
        df.to_sql(name_doc(doc), engine, index=False, if_exists='replace')
            
        print(doc + " has been updated")

def execute_analysis_ipynb():
    def dict_to_list(dict):
        list = []
        for key, value in dict.items():
            list.append([key, value])
        return list
    def calcul_occurence(list, index_occurence, usage_column = True, usage_occurence_ratio = 4): #index_occurence est l'indice dans la une sous-liste de la valeur permettant de calculer l'occurence
        occurence = 0
        for sublist in list:
            """print(sublist)
            print(sublist[index_occurence])"""
            occurence += sublist[index_occurence]
        for sublist in list:
            sublist.append(sublist[index_occurence]/occurence)
        if usage_column:
            for sublist in list:
                sublist.append(usage_occurence_ratio*sublist[-1])
        return list
    data_file0 = 'usage/gen9ou-0.json'
    df0 = pd.read_json(data_file0)
    df0 = df0.transpose()
    df0 = df0.applymap(lambda cell: dict_to_list(cell) if isinstance(cell, dict) else cell)
    df0 = df0.reset_index()
    df0.rename(columns = {'index': 'name_pokemon'}, inplace=True)
    data_file1 = 'usage/gen9ou-0.json'
    df1 = pd.read_json(data_file1)
    df1 = df1.transpose()
    df1 = df1.applymap(lambda cell: dict_to_list(cell) if isinstance(cell, dict) else cell)
    df1 = df1.reset_index()
    df1.rename(columns = {'index': 'name_pokemon'}, inplace=True)

    df1 = df1.loc[:, ['name_pokemon', 'usage']]

    data_file2 = 'usage/gen9ou-0.json'
    df2 = pd.read_json(data_file2)
    df2 = df2.transpose()
    df2 = df2.applymap(lambda cell: dict_to_list(cell) if isinstance(cell, dict) else cell)
    df2 = df2.reset_index()
    df2.rename(columns = {'index': 'name_pokemon'}, inplace=True)
    for i in range(len(df2)):
        df2['Moves'].iloc[i] = calcul_occurence(df2['Moves'].iloc[i], 1)

    df2_expanded = df2.explode('Moves')[['name_pokemon', 'Moves']]
    df2_expanded['Moves name'] = df2_expanded['Moves'].apply(lambda x: x[0])
    df2_expanded['Moves occurence'] = df2_expanded['Moves'].apply(lambda x: x[2])
    df2_expanded['Moves usage'] = df2_expanded['Moves'].apply(lambda x: x[3])
    df2_expanded.reset_index(inplace=True, drop=True)
    df2_expanded = df2_expanded[['name_pokemon', 'Moves name', 'Moves occurence', 'Moves usage']]

    data_file3 = 'usage/gen9ou-0.json'
    df3 = pd.read_json(data_file3)
    df3 = df3.transpose()
    df3 = df3.applymap(lambda cell: dict_to_list(cell) if isinstance(cell, dict) else cell)
    df3 = df3.reset_index()
    df3.rename(columns = {'index': 'name_pokemon'}, inplace=True)
    for i in range(len(df3)):
        df3['Abilities'].iloc[i] = calcul_occurence(df3['Abilities'].iloc[i], 1, usage_occurence_ratio=1)
        
    df3_expanded = df3.explode('Abilities')[['name_pokemon', 'Abilities']]
    df3_expanded['Ability name'] = df3_expanded['Abilities'].apply(lambda x: x[0])
    df3_expanded['Ability occurence'] = df3_expanded['Abilities'].apply(lambda x: x[2])
    df3_expanded['Ability usage'] = df3_expanded['Abilities'].apply(lambda x: x[3])
    df3_expanded.reset_index(inplace=True, drop=True)
    df3_expanded = df3_expanded[['name_pokemon', 'Ability name', 'Ability occurence', 'Ability usage']]
    path = 'stats_pokemons/'
    database = 'STNUM_pokemon.db'
    engine = create_engine('sqlite:///' + database)
    df1.to_sql("Pokemons usage", engine, index=False, if_exists='replace')
    df2_expanded.to_sql("Moves usage", engine, index=False, if_exists='replace')
    df3_expanded.to_sql("Abilities usage", engine, index=False, if_exists='replace')

def full_refresh(): #Refresh all the database
    refresh_database_csv()
    execute_analysis_ipynb()
    print("Francois code had been executed")

full_refresh()