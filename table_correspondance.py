import pandas as pd
import sqlite3 
conn = sqlite3.connect('STNUM_pokemon.db') #Outil permettant d'exploiter la base de donnée

#On peut ensuite récupérer dans un format dataframe (le même format que pour la STNum) les données via des commandes SQL
'''request = 'SELECT DISTINCT Moves_name FROM Moves_Usage'
pkmn_linked = pd.read_sql(request, conn)
print(pkmn_linked.info())
print(pkmn_linked)'''

def regenerate_moves_obtention_table():
    conn = sqlite3.connect('STNUM_pokemon.db')

    drop_table_query = "DROP TABLE IF EXISTS Moves_obtention"
    conn.execute(drop_table_query)
    conn.commit()

    # Récupérer les noms des mouvements distincts
    request = 'SELECT DISTINCT Moves_name FROM Moves_Usage'
    moves_names = pd.read_sql(request, conn)['Moves_name']

    # Créer une nouvelle table avec des attributs binaires
    new_table_name = 'Moves_obtention'
    create_table_query = f'CREATE TABLE {new_table_name} ('
    create_table_query += f'{"Name_pokemon"} TEXT, '
    for move_name in moves_names:
        if not move_name=='':
            create_table_query += f'{move_name} BINARY, '
    create_table_query = create_table_query[:-2] + ')'

    # Exécuter la requête pour créer la nouvelle table
    conn.execute(create_table_query)

    # Ajouter un champ pour chaque pokémon dans la jointure de Pokemon et Moves_Usage
    join_query = f'INSERT INTO {new_table_name} (Name_pokemon) SELECT Name FROM Pokemon INNER JOIN Pokemons_usage ON Pokemon.Name = Pokemons_usage.name_pokemon'
    conn.execute(join_query)
    
    # Mettre à jour les attributs binaires de la table Moves_obtention
    update_query = "UPDATE Moves_obtention SET "
    moves_names = pd.read_sql("SELECT DISTINCT Moves_name FROM Moves_Usage", conn)['Moves_name']
    for move_name in moves_names:
        if not move_name == '':
            update_query += f"{move_name} = 0, "
    update_query = update_query[:-2]
    conn.execute(update_query)
    conn.commit()

    # Mettre à jour les attributs binaires de la table Moves_obtention
    update_query = "UPDATE Moves_obtention SET "
    moves = pd.read_sql("SELECT DISTINCT name_pokemon, Moves_name FROM Moves_Usage WHERE name_pokemon IN (SELECT DISTINCT Name_pokemon FROM Moves_obtention)", conn)
    
    for index, row in moves.iterrows():
        pokemon = row['name_pokemon']
        move_name = row['Moves_name']
        if not move_name == '':
            update_query = f"UPDATE Moves_obtention SET {move_name} = 1 WHERE Name_pokemon = '{pokemon}'"
            conn.execute(update_query)
    conn.commit()

    print('Table Moves_obtention regenerated')

def regenerate_type_table():
    conn = sqlite3.connect('STNUM_pokemon.db')

    drop_table_query = "DROP TABLE IF EXISTS Type"
    conn.execute(drop_table_query)
    conn.commit()

    # Récupérer les noms des mouvements distincts
    request = 'SELECT DISTINCT Type1 FROM Pokemon'
    types = pd.read_sql(request, conn)['Type1']

    # Créer une nouvelle table avec des attributs binaires
    new_table_name = 'Type'
    create_table_query = f'CREATE TABLE {new_table_name} ('
    create_table_query += f'{"Name_pokemon"} TEXT, '
    for type_name in types:
        if not type_name=='':
            create_table_query += f'{type_name} BINARY, '
    create_table_query = create_table_query[:-2] + ')'

    # Exécuter la requête pour créer la nouvelle table
    conn.execute(create_table_query)

    # Ajouter un champ pour chaque pokémon dans la jointure de Pokemon et Moves_Usage
    join_query = f'INSERT INTO {new_table_name} (Name_pokemon) SELECT name_pokemon FROM Pokemons_usage'
    conn.execute(join_query)
    
    # Mettre à jour les attributs binaires de la table Moves_obtention
    update_query = "UPDATE Type SET "
    types1 = pd.read_sql("SELECT DISTINCT Type1 FROM Pokemon", conn)['Type1']
    for type_name in types:
        if not type_name == '':
            update_query += f"{type_name} = 0, "
    update_query = update_query[:-2]
    conn.execute(update_query)
    conn.commit()

    # Mettre à jour les attributs binaires de la table Type
    update_query = "UPDATE Type SET "
    types = pd.read_sql("SELECT DISTINCT Type1, Type2, Name FROM Pokemon WHERE Name IN (SELECT DISTINCT Name_pokemon FROM Type)", conn)
    for index, row in types.iterrows():
        pokemon = row['Name']
        type1_name = row['Type1']
        type2_name = row['Type2']
        if not type1_name == ' ':
            update_query = f'UPDATE Type SET {type1_name} = 1 WHERE Name_pokemon = "{pokemon}"'
            #print(update_query)
            conn.execute(update_query)
        if not type2_name == ' ':
            update_query = f'UPDATE Type SET {type2_name} = 1 WHERE Name_pokemon = "{pokemon}"'
            #print(update_query)
            conn.execute(update_query)
    conn.commit()

    print('Table Type regenerated')

#regenerate_type_table()

def regenerate_binary_description_table():
    conn = sqlite3.connect('STNUM_pokemon.db')

    drop_table_query = "DROP TABLE IF EXISTS binary_description"
    conn.execute(drop_table_query)
    conn.commit()

    # Récupérer les noms des mouvements distincts
    request = 'SELECT DISTINCT Moves_name FROM Moves_Usage'
    moves_names = pd.read_sql(request, conn)['Moves_name']

    # Créer une nouvelle table avec des attributs binaires
    new_table_name = 'binary_description'
    create_table_query = f'CREATE TABLE {new_table_name} ('
    create_table_query += f'{"Name_pokemon"} TEXT, '
    for move_name in moves_names:
        if not move_name=='':
            create_table_query += f'{move_name} BINARY, '

    # Récupérer les noms des mouvements distincts
    request = 'SELECT DISTINCT Type1 FROM Pokemon'
    types = pd.read_sql(request, conn)['Type1']

    for type_name in types:
        if not type_name=='':
            create_table_query += f'{type_name}_Type BINARY, '
    create_table_query = create_table_query[:-2] + ')'

    # Exécuter la requête pour créer la nouvelle table
    conn.execute(create_table_query)

    # Ajouter un champ pour chaque pokémon dans la jointure de Pokemon et Moves_Usage
    join_query = f'INSERT INTO {new_table_name} (Name_pokemon) SELECT Name FROM Pokemon INNER JOIN Pokemons_usage ON Pokemon.Name = Pokemons_usage.name_pokemon'
    conn.execute(join_query)
    
    # Mettre à jour les attributs binaires de la table Moves_obtention
    update_query = "UPDATE binary_description SET "
    moves_names = pd.read_sql("SELECT DISTINCT Moves_name FROM Moves_Usage", conn)['Moves_name']
    for move_name in moves_names:
        if not move_name == '':
            update_query += f"{move_name} = 0, "
    update_query = update_query[:-2]
    conn.execute(update_query)
    conn.commit()

    # Mettre à jour les attributs binaires de la table Moves_obtention
    update_query = "UPDATE binary_description SET "
    moves = pd.read_sql("SELECT DISTINCT name_pokemon, Moves_name FROM Moves_Usage WHERE name_pokemon IN (SELECT DISTINCT Name_pokemon FROM Moves_obtention)", conn)
    
    for index, row in moves.iterrows():
        pokemon = row['name_pokemon']
        move_name = row['Moves_name']
        if not move_name == '':
            update_query = f"UPDATE binary_description SET {move_name} = 1 WHERE Name_pokemon = '{pokemon}'"
            conn.execute(update_query)
    conn.commit()

    
    # Mettre à jour les attributs binaires de la table Moves_obtention
    update_query = "UPDATE binary_description SET "
    types1 = pd.read_sql("SELECT DISTINCT Type1 FROM Pokemon", conn)['Type1']
    for type_name in types:
        if not type_name == '':
            update_query += f"{type_name}_Type = 0, "
    update_query = update_query[:-2]
    conn.execute(update_query)
    conn.commit()

    # Mettre à jour les attributs binaires de la table Type
    update_query = "UPDATE binary_description SET "
    types = pd.read_sql("SELECT DISTINCT Type1, Type2, Name FROM Pokemon WHERE Name IN (SELECT DISTINCT Name_pokemon FROM Type)", conn)
    for index, row in types.iterrows():
        pokemon = row['Name']
        type1_name = row['Type1']
        type2_name = row['Type2']
        if not type1_name == ' ':
            update_query = f'UPDATE binary_description SET {type1_name}_Type = 1 WHERE Name_pokemon = "{pokemon}"'
            #print(update_query)
            conn.execute(update_query)
        if not type2_name == ' ':
            update_query = f'UPDATE binary_description SET {type2_name}_Type = 1 WHERE Name_pokemon = "{pokemon}"'
            #print(update_query)
            conn.execute(update_query)
    conn.commit()

    print('Table binary_description regenerated')

regenerate_binary_description_table()