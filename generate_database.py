import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
from table_correspondance import regenerate_moves_obtention_table, regenerate_type_table, regenerate_binary_description_table



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
    df2_expanded['Moves_name'] = df2_expanded['Moves'].apply(lambda x: x[0])
    df2_expanded['Moves_occurence'] = df2_expanded['Moves'].apply(lambda x: x[2])
    df2_expanded['Moves_usage'] = df2_expanded['Moves'].apply(lambda x: x[3])
    df2_expanded.reset_index(inplace=True, drop=True)
    df2_expanded = df2_expanded[['name_pokemon', 'Moves_name', 'Moves_occurence', 'Moves_usage']]

    data_file3 = 'usage/gen9ou-0.json'
    df3 = pd.read_json(data_file3)
    df3 = df3.transpose()
    df3 = df3.applymap(lambda cell: dict_to_list(cell) if isinstance(cell, dict) else cell)
    df3 = df3.reset_index()
    df3.rename(columns = {'index': 'name_pokemon'}, inplace=True)
    for i in range(len(df3)):
        df3['Abilities'].iloc[i] = calcul_occurence(df3['Abilities'].iloc[i], 1, usage_occurence_ratio=1)
        
    df3_expanded = df3.explode('Abilities')[['name_pokemon', 'Abilities']]
    df3_expanded['Ability_name'] = df3_expanded['Abilities'].apply(lambda x: x[0])
    df3_expanded['Ability_occurence'] = df3_expanded['Abilities'].apply(lambda x: x[2])
    df3_expanded['Ability_usage'] = df3_expanded['Abilities'].apply(lambda x: x[3])
    df3_expanded.reset_index(inplace=True, drop=True)
    df3_expanded = df3_expanded[['name_pokemon', 'Ability_name', 'Ability_occurence', 'Ability_usage']]
    path = 'stats_pokemons/'
    database = 'STNUM_pokemon.db'
    engine = create_engine('sqlite:///' + database)
    df1.to_sql("Pokemons_usage", engine, index=False, if_exists='replace')
    df2_expanded.to_sql("Moves_usage", engine, index=False, if_exists='replace')
    df3_expanded.to_sql("Abilities_usage", engine, index=False, if_exists='replace')


import sqlite3

def update_pokemon_hisui(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("UPDATE Pokemon SET Name = Name || '-Hisui' WHERE SUBSTR(Form, 1, 5) = 'Hisui'")

        # Validation de la transaction
        conn.commit()
        print("Mise à jour hisuiréussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la mise à jour :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def update_pokemon_galar(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("UPDATE Pokemon SET Name = Name || '-Galar' WHERE SUBSTR(Form, 1, 5) = 'Galar'")

        # Validation de la transaction
        conn.commit()
        print("Mise à jour Galar réussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la mise à jour :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def update_pokemon_therian(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("UPDATE Pokemon SET Name = Name || '-Therian' WHERE SUBSTR(Form, 1, 5) = 'Theri'")

        # Validation de la transaction
        conn.commit()
        print("Mise à jour Therian réussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la mise à jour :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def update_pokemon_alola(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("UPDATE Pokemon SET Name = Name || '-Alola' WHERE SUBSTR(Form, 1, 5) = 'Alola'")

        # Validation de la transaction
        conn.commit()
        print("Mise à jour Alola réussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la mise à jour :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def update_pokemon_mega(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("UPDATE Pokemon SET Name = Name || '-Mega' WHERE SUBSTR(Form, 1, 4) = 'Mega'")

        # Validation de la transaction
        conn.commit()
        print("Mise à jour Mega réussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la mise à jour :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def update_pokemon_rotom(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("UPDATE Pokemon SET Name = Name || '-' || SUBSTR(Form, 1, 4) WHERE SUBSTR(Form, -5) = 'Rotom'")
        cursor.execute("UPDATE Pokemon SET Name = 'Rotom-Frost' WHERE Name = 'Rotom-Fros'")
        conn.commit()
        cursor.execute("UPDATE Pokemon SET Name = 'Rotom-Fan' WHERE Name = 'Rotom-Fan '")
        conn.commit()
        cursor.execute("UPDATE Pokemon SET Name = 'Rotom-Mow' WHERE Name = 'Rotom-Mow '")
        conn.commit()
        # Validation de la transaction
        conn.commit()
        print("Mise à jour Rotom réussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la mise à jour :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def update_pokemon_tauros(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("UPDATE Pokemon SET Name = Name || '-Paldea-Combat'  WHERE Name = 'Tauros' AND SUBSTR(Form, 1, 2) = 'Co'")
        conn.commit()
        cursor.execute("UPDATE Pokemon SET Name = Name || '-Paldea-Aqua'  WHERE Name = 'Tauros' AND SUBSTR(Form, 1, 2) = 'Aq'")
        conn.commit()
        cursor.execute("UPDATE Pokemon SET Name = Name || '-Paldea-Blaze'  WHERE Name = 'Tauros' AND SUBSTR(Form, 1, 2) = 'Bl'")
        conn.commit()
        # Validation de la transaction
        print("Mise à jour Tauros réussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la mise à jour :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def update_pokemon_basculegion_indeedee(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("UPDATE Pokemon SET Name = 'Basculegion-F'  WHERE Name = 'Basculegion' AND SUBSTR(Form, 1, 2) = 'Fe'")
        conn.commit()
        cursor.execute("UPDATE Pokemon SET Name = 'Indeedee-F'  WHERE Name = 'Indeedee' AND SUBSTR(Form, 1, 2) = 'Fe'")
        conn.commit()
        # Validation de la transaction
        print("Mise à jour Basculegion réussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la mise à jour :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def delete_pokemon_squawkabilly(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("DELETE FROM Pokemon WHERE Name = 'Squawkabilly' AND Form != 'Green Plumage'")
        conn.commit()
        # Validation de la transaction
        print("Suppression des Pokemon avec Name = 'Squawkabilly' réussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la suppression :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def delete_pokemon_Tatsugiri(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("DELETE FROM Pokemon WHERE Name = 'Tatsugiri' AND Form != 'Curly Form'")
        conn.commit()
        # Validation de la transaction
        print("Suppression des Pokemon avec Name = 'Tatsugiri' réussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la suppression :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def delete_pokemon_zamazenta_gren_maushold(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("DELETE FROM Pokemon WHERE Name = 'Zamazenta' AND Form != 'Crowned Shield'")
        conn.commit()
        cursor.execute("DELETE FROM Pokemon WHERE Name = 'Greninja' AND Form != 'Ash-Greninja'")
        conn.commit()
        cursor.execute("DELETE FROM Pokemon WHERE Name = 'Maushold' AND Form != 'Family of Three'")
        conn.commit()
        # Validation de la transaction
        print("Suppression des Doublons Zamazenta et Greninja.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la suppression :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()

def delete_duplicate_pokemon(database_path):
    # Connexion à la base de données
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Exécution de la requête SQL
        cursor.execute("""
            DELETE FROM Pokemon
            WHERE Name IN (
                SELECT Name
                FROM Pokemon
                JOIN Pokemons_usage ON Pokemon.name = Pokemons_usage.name_pokemon
                GROUP BY Name
                HAVING COUNT(*) > 1
            )
        """)
        conn.commit()
        # Validation de la transaction
        print("Suppression des doublons réussie.")
    except Exception as e:
        # En cas d'erreur, annuler la transaction
        conn.rollback()
        print("Erreur lors de la suppression des doublons :", str(e))
    finally:
        # Fermeture de la connexion
        conn.close()
'''
def binary_move():
    database = 'STNUM_pokemon.db'
    engine = create_engine('sqlite:///' + database)
    df = pd.read_sql('SELECT DISTINCT moves FROM Moves_usage', engine)
    df['Moves_occurence'] = df['Moves_occurence'].astype(float)
    df['Moves_usage'] = df['Moves_usage'].astype(float)
    df['Moves_occurence'] = df['Moves_occurence'].apply(lambda x: 1 if x > 0 else 0)
    df['Moves_usage'] = df['Moves_usage'].apply(lambda x: 1 if x > 0 else 0)
    df.to_sql('Moves_usage_binary', engine, index=False, if_exists='replace')

def create_pokemon_attacks_table(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        # Création de la nouvelle table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pokemon_Attacks (
                Pokemon TEXT,
                Attack TEXT,
                Value INTEGER
            )
        """)

        # Insertion des données dans la nouvelle table
        cursor.execute("""
            INSERT INTO Pokemon_Attacks (Pokemon, Attack, Value)
            SELECT DISTINCT Pokemon.Name, Moves_usage.moves,
                CASE WHEN Moves_usage.moves IS NOT NULL THEN 1 ELSE 0 END
            FROM Pokemon
            LEFT JOIN Moves_usage ON Pokemon.Name = Moves_usage.moves
        """)

        conn.commit()
        print("La table Pokemon_Attacks a été créée avec succès.")
    except Exception as e:
        conn.rollback()
        print("Erreur lors de la création de la table Pokemon_Attacks :", str(e))
    finally:
        conn.close()
'''


def full_refresh(): #Refresh all the database
    refresh_database_csv()
    execute_analysis_ipynb()
    print("Francois code had been executed")
    update_pokemon_alola('STNUM_Pokemon.db')
    update_pokemon_galar('STNUM_Pokemon.db')
    update_pokemon_hisui('STNUM_Pokemon.db')
    update_pokemon_therian('STNUM_Pokemon.db')
    update_pokemon_mega('STNUM_Pokemon.db')
    update_pokemon_rotom('STNUM_Pokemon.db')
    update_pokemon_tauros('STNUM_Pokemon.db')
    update_pokemon_basculegion_indeedee('STNUM_Pokemon.db')
    delete_pokemon_squawkabilly('STNUM_Pokemon.db')
    delete_pokemon_Tatsugiri('STNUM_Pokemon.db')
    delete_pokemon_zamazenta_gren_maushold('STNUM_Pokemon.db')
    delete_duplicate_pokemon('STNUM_Pokemon.db')
    regenerate_binary_description_table()

full_refresh()
