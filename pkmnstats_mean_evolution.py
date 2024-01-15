import pandas as pd
import sqlite3 
conn = sqlite3.connect('STNUM_pokemon.db') #Outil permettant d'exploiter la base de donnée

import numpy as np # Pour les calculs mathématiques
import matplotlib.pyplot as plt # Pour les graphiques
import pandas as pd # Pour la manipulation de tableaux de données

from statsmodels.api import OLS # Pour la régression linéaire (avec statsmodels)
from statsmodels.tools.tools import add_constant # Pour l'ajout d'une constante dans statsmodels

from sklearn.linear_model import LinearRegression # Pour la régression linéaire (avec sklearn)

request = 'SELECT "Generation", AVG("Total"), AVG("HP"), AVG("Attack"), AVG("Defense"), AVG("Sp. Atk"), AVG("Sp. Def"), AVG("Speed"), COUNT(*) FROM Pokemon WHERE "Can Evolve" = 0 GROUP BY "Generation"' 
df_stats_evolution = pd.read_sql(request, conn)
print(df_stats_evolution)

var_X = ['Generation']
X = df_stats_evolution[var_X]


list_attribute=['AVG("Total")', 'AVG("HP")', 'AVG("Attack")', 'AVG("Defense")', 'AVG("Sp. Atk")', 'AVG("Sp. Def")', 'AVG("Speed")']

for cl in list_attribute:

    var_y = cl
    y = df_stats_evolution[var_y]

    linreg_model = OLS(y, add_constant(X))
    linreg = linreg_model.fit()
    linreg_sk_model = LinearRegression()
    linreg_sk = linreg_sk_model.fit(X, y)
    print(linreg.summary())

    a = linreg_sk.coef_
    cte = linreg_sk.intercept_
    line_reg = a*X + cte

    hauteurs = y
    # Numéros pour l'axe des x
    numeros_x = X['Generation'].tolist()
    # Création de l'histogramme
    plt.bar(numeros_x, hauteurs, color='blue', edgecolor='black')

    plt.plot(X, line_reg, "r-")
    # Ajout de titres et d'étiquettes
    plt.title('Evolution des statistiques des pokémons en fonction de leur génération')
    plt.xlabel('Génération')
    plt.ylabel(cl)


    # Affichage de l'histogramme
    plt.show()
    
def evolution_par_type(type, stat):
    request2 = f'SELECT "Generation", AVG("{stat}") as avg_stat, COUNT(*) FROM Pokemon WHERE "Type1" = "{type}" OR "Type2" = "{type}" GROUP BY "Generation"' 
    df_stats_evolution = pd.read_sql(request2, conn)
    
    var_X = ['Generation']
    X = df_stats_evolution[var_X]
    
    var_y = 'avg_stat'
    y = df_stats_evolution[var_y]
    
    linreg_model = OLS(y, add_constant(X))
    linreg = linreg_model.fit()
    linreg_sk_model = LinearRegression()
    linreg_sk = linreg_sk_model.fit(X, y)
    print(linreg.summary())

    a = linreg_sk.coef_
    cte = linreg_sk.intercept_
    line_reg = a*X + cte

    hauteurs = y
    # Numéros pour l'axe des x
    numeros_x = X['Generation'].tolist()
    # Création de l'histogramme
    plt.bar(numeros_x, hauteurs, color='blue', edgecolor='black')

    plt.plot(X, line_reg, "r-")
    # Ajout de titres et d'étiquettes
    plt.title(f'Evolution des statistiques des pokémons en fonction de leur génération pour le type {type}')
    plt.xlabel('Génération')
    plt.ylabel(f'{stat}')


    # Affichage de l'histogramme
    plt.show()

print(evolution_par_type("Fire", "Attack"))