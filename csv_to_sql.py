import pandas as pd
from sqlalchemy import create_engine


def name_doc(document): #take a document.extention, return it's name without the extension
    for i in range(1,len(document)):
        if document[len(document)-i] == '.':
            return document[:len(document)-i]

def refresh_database():
    path = 'stats_pokemons/'
    list_doc = ['gen01.csv','gen02.csv','gen03.csv','gen04.csv','gen05.csv','gen06.csv','gen07.csv','gen08.csv','gen09.csv','Pokemon.csv']
    database = path + 'stats_pokemons.db'
    engine = create_engine('sqlite:///' + database)
    for doc in list_doc:
        df = pd.read_csv(path + doc)
        df.to_sql(name_doc(doc), engine, index=False, if_exists='replace')
            
        print(doc + " has been updated")

refresh_database()
