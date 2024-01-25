import pandas as pd # Pour lire les fichiers
import numpy as np # Pour effectuer des calculs mathématiques
import matplotlib.pyplot as plt # Pour réaliser des graphiques
from scipy import stats # Pour effectuer des calculs statistiques
from sklearn.preprocessing import StandardScaler # Pour normaliser les données
from sklearn import decomposition # Pour effectuer une ACP

import sqlite3 
conn = sqlite3.connect('STNUM_pokemon.db') #Outil permettant d'exploiter la base de donnée

#On peut ensuite récupérer dans un format dataframe (le même format que pour la STNum) les données via des commandes SQL
request = 'SELECT "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed" FROM Pokemon WHERE "Can_Evolve" = 0 ORDER BY "Total"' 
table_stats = pd.read_sql(request, conn)
print(table_stats)

pca = decomposition.PCA()
pca.fit(table_stats)
plt.plot(range(1,7),pca.explained_variance_)
plt.show()

def print_stats(stats):
    print("HP : ", stats[0])
    print("Attack : ", stats[1])
    print("Defense : ", stats[2])
    print("Sp. Atk : ", stats[3])
    print("Sp. Def : ", stats[4])
    print("Speed : ", stats[5])

def print_pca_stats(pca):
    print("Composante n°0 (moyenne) :")
    print_stats(pca.mean_)
    print("")
    for i in range(len(pca.components_)):
        print("Composante n°", i+1)
        print_stats(pca.components_[i])
        print("")

def plot_scatter_pca(pca):
    fig, axs = plt.subplots(len(pca.components_), figsize=(10, 5*len(pca.components_)))

    for i in range(len(pca.components_)):
        axs[i].scatter(range(len(pca.components_[i])), pca.components_[i])
        axs[i].set_xlabel("Index")
        axs[i].set_ylabel("Value")
        axs[i].set_title("Scatter plot of PCA Component {}".format(i+1))

    plt.tight_layout()
    plt.show()

def plot_pca_mean(pca):
    labels = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    mean_values = pca.mean_
    plt.bar(labels, mean_values)
    plt.xlabel("Features")
    plt.ylabel("Mean Value")
    plt.title("PCA Mean Values")
    plt.show()


def plot_bar_pca(pca):
    fig, axs = plt.subplots(len(pca.components_)//3 + len(pca.components_)%3, 3, figsize=(8, len(pca.components_)))
    labels = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    for i in range(len(pca.components_)):
        row = i // 3
        col = i % 3
        axs[row, col].bar(labels, pca.components_[i])
        axs[row, col].set_xlabel("Index")
        axs[row, col].set_ylabel("Value")
        axs[row, col].set_title("Bar plot of PCA Component {}".format(i+1))

    plt.tight_layout()
    plt.show()

print_pca_stats(pca)
plot_pca_mean(pca)
plot_bar_pca(pca)