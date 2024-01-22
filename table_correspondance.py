import pandas as pd
import sqlite3 
conn = sqlite3.connect('STNUM_pokemon.db') #Outil permettant d'exploiter la base de donnée

#On peut ensuite récupérer dans un format dataframe (le même format que pour la STNum) les données via des commandes SQL
request = 'SELECT sum(usage) FROM Pokemon JOIN Pokemons_usage ON Pokemon.name = Pokemons_usage.name_pokemon ' 
pkmn_linked = pd.read_sql(request, conn)
print(pkmn_linked.info())
print(pkmn_linked)
