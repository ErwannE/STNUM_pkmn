#Petit tuto pour apprendre à utiliser la base de donnée stats_pokemons.db 
#La lecture de la base de donnée se fait via des commandes en SQL et les deux bibliothèques suivantes :
import pandas as pd
import sqlite3 
conn = sqlite3.connect('stats_pokemons/stats_pokemons.db') #Outil permettant d'exploiter la base de donnée

#On peut ensuite récupérer dans un format dataframe (le même format que pour la STNum) les données via des commandes SQL
request = 'SELECT "Name", "Attack", "Sp. Atk" FROM Pokemon WHERE Type1="Fire" OR Type2="Fire" ORDER BY "Total"' 
df_fire_type_atk_spa = pd.read_sql(request, conn)
print(df_fire_type_atk_spa.info())
print(df_fire_type_atk_spa)

request = 'SELECT AVG("Attack"), AVG("Sp. Atk") FROM Pokemon WHERE Type1="Fire" OR Type2="Fire"'
df_fire_type_atk_spa_AVG = pd.read_sql(request, conn)
print(df_fire_type_atk_spa_AVG)

#A vous de vous amuser, à savoir qu'on travaille sous l'environnement SQLite