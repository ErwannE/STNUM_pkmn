import numpy as np # Pour des calculs mathématiques
import pandas as pd # Pour la manipulation de tableaux de données
import matplotlib.pyplot as plt # Pour les graphiques

from scipy.cluster.hierarchy import dendrogram # Pour le dendrogramme
from sklearn.preprocessing import StandardScaler # Pour la normalisation des données
from sklearn.cluster import AgglomerativeClustering # Pour la CAH
from sklearn.cluster import KMeans # Pour les K-means

import sqlite3 
conn = sqlite3.connect('STNUM_pokemon.db') #Outil permettant d'exploiter la base de donnée

from utils import plot_average_attributes


# Import data. Only pokemon that have usage, in gen n° n_gen.

def import_data():
    request = f'''SELECT Name, Total, HP, Attack, Defense, "Sp. Atk", "Sp. Def", Speed, Generation \
    FROM Pokemon WHERE Pokemon.Can_Evolve = 0'''
    df = pd.read_sql(request, conn)
    # reshaping to get names of pokemon as indexes
    df.index = df['Name']
    df = df.drop('Name', axis=1)
    return df

stats_gen = import_data()
print(stats_gen.head())

def cah_model_plot(data_cluster, n, k_max=0):
    '''Allows to determine the optimal number of clusters'''
    cah_model = AgglomerativeClustering(distance_threshold=0,
                                       metric='euclidean',
                                       linkage='ward',
                                       n_clusters=None)
    cah = cah_model.fit(data_cluster) 
    # Print histogram of heights depending on number of clusters  
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.vlines(range(2, n+1), 0, np.flip(np.sort(cah.distances_)), linewidth=5)
    ax.grid()
    ax.set_xlabel('K')
    ax.set_ylabel('Hauteur')
    plt.title('Passage de K à (K-1) clusters')
    plt.show()

    # Input the number of k_max that user wants to see
    print('Do you want to zoom ? (y/n)')
    answer = input()
    while answer != 'y' and answer != 'n':
        print('Press y for yes and n for no')
        answer = input()
    if answer == 'n':
        return 0
    
    if answer == 'y':
        while k_max == 0:
            print('Please, input number of max clusters that you want to see:')
            k_max = int(input())
            if k_max == 0:
                print('The number of clusters should be a non-zero integer.')

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.vlines(range(2, k_max+1), 0, np.flip(np.sort(cah.distances_))[0:k_max-1], linewidth=5)
        ax.set_xticks(range(2, k_max+1))
        ax.grid()
        ax.set_xlabel('K')
        ax.set_ylabel('Hauteur')
        plt.title('Passage de K à (K-1) clusters')
        plt.show()

def calc_clusters_gen(list_gens, df, mode, k_clusters=0, k_max=0):
    '''Returns :
    - df_gen
    - clusters, a list of k_clusters lists, each of which represents a cluster
    that contains names of Pokemon that belong to this cluster.'''

    assert mode == 'K-means' or mode == 'HAC', 'mode should be "K-means" or "HAC"'
    if type(list_gens) == int:
        list_gens = [list_gens]
    # get the data needed
    df_gen = df[df['Generation'].isin(list_gens)]
    print(df_gen.head())
    df_gen = df_gen.drop('Generation', axis=1)
    
    # get dimensions
    n = df_gen.shape[0]
    p = df_gen.shape[1]
    # Normalize data
    norm = StandardScaler(with_mean=True, with_std=True)
    data_cluster = norm.fit_transform(df_gen)

    # Plot CAH to choose the number of clusters for the K-means
    if k_clusters == 0:
        cah_model_plot(data_cluster, n, k_max)

    # Input number of clusters if needed
    while k_clusters == 0:
        print('Please, input number of clusters chosen :')
        k_clusters = int(input())
        if k_clusters == 0:
            print('The number of clusters should be a non-zero integer.')

    # Once we know the number of clusters, we can perform the clustering.

    # mode K-means
    if mode == 'K-means':
        kmeans_model = KMeans(init='k-means++', max_iter=100, n_clusters=k_clusters, n_init=10)
        kmeans = kmeans_model.fit(data_cluster)
        df_gen['cluster_number'] = kmeans.fit_predict(data_cluster)
        df_gen['cluster_number'].value_counts()

    # mode HAC
    if mode == 'HAC':
        cah_model = AgglomerativeClustering(metric='euclidean',
                                   linkage='ward',
                                   n_clusters=k_clusters)
        cah = cah_model.fit(data_cluster)
        df_gen['cluster_number'] = cah.fit_predict(data_cluster)
        df_gen['cluster_number'].value_counts()

    # Return clusters and table.
    res = [] # list that contains the clusters
    for i in range(k_clusters):
        res.append(list(df_gen[df_gen['cluster_number'] == i].index))
    return df_gen, res

df_gen1, clusters_gen_1 = calc_clusters_gen([1,2,3,4,5,6,7,8,9], stats_gen, 'HAC')
print(clusters_gen_1)

def labellize_clusters(clusters, df):
    # plot the average stats in the cluster:
    mapping = {}
    for i in range(len(clusters)):
        print('Cluster ' + str(i) + ':', clusters[i])
        plot_average_attributes(clusters[i])
        print('Give a label to this cluster:')
        cluster_label = input()
        mapping[i] = cluster_label
    df['Cluster_label'] = [mapping[i] for i in df['cluster_number']]
    return df

df_gen1 = labellize_clusters(clusters_gen_1,df_gen1)
print(df_gen1)







        