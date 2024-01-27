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

def import_stats():
    request = f'''SELECT Name, HP, Attack, Defense, "Sp. Atk", "Sp. Def", Speed, Generation \
    FROM Pokemon WHERE Pokemon.Can_Evolve = 0'''
    df = pd.read_sql(request, conn)
    # reshaping to get names of pokemon as indexes
    df.index = df['Name']
    df = df.drop('Name', axis=1)
    return df

def import_usage():
    req = f'''SELECT * FROM Pokemons_usage'''
    df = pd.read_sql(req, conn)
    # reshaping to get names of pokemon as indexes
    df.index = df['name_pokemon']
    df = df.drop('name_pokemon', axis=1)
    return df

stats_gen = import_stats()
print(stats_gen.head())
print(stats_gen.info())

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
    - df_clusters
    - clusters, a list of k_clusters lists, each of which represents a cluster
    that contains names of Pokemon that belong to this cluster.'''

    assert mode == 'K-means' or mode == 'HAC', 'mode should be "K-means" or "HAC"'
    if type(list_gens) == int:
        list_gens = [list_gens]
    # get the data needed
    df_clusters = df[df['Generation'].isin(list_gens)]
    print(df_clusters.head())
    df_clusters = df_clusters.drop('Generation', axis=1)
    
    # get dimensions
    n = df_clusters.shape[0]
    p = df_clusters.shape[1]
    # Normalize data
    norm = StandardScaler(with_mean=True, with_std=True)
    data_cluster = norm.fit_transform(df_clusters)

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
        df_clusters['cluster_number'] = kmeans.fit_predict(data_cluster)
        df_clusters['cluster_number'].value_counts()

    # mode HAC
    if mode == 'HAC':
        cah_model = AgglomerativeClustering(metric='euclidean',
                                   linkage='ward',
                                   n_clusters=k_clusters)
        cah = cah_model.fit(data_cluster)
        df_clusters['cluster_number'] = cah.fit_predict(data_cluster)
        df_clusters['cluster_number'].value_counts()

    # Return clusters and table.
    res = [] # list that contains the clusters
    for i in range(k_clusters):
        res.append(list(df_clusters[df_clusters['cluster_number'] == i].index))
    return df_clusters, res

def labellize_clusters(clusters, df):
    # plot the average stats in the cluster:
    mapping = {}
    for i in range(len(clusters)):
        print('Cluster ' + str(i) + ':', clusters[i])
        print('Give a label to this cluster:')
        plot_average_attributes(clusters[i])
        cluster_label = input()
        mapping[i] = cluster_label
    df['Cluster_label'] = [mapping[i] for i in df['cluster_number']]
    return df, mapping

# TO DO LIST
# % of pokemon used in the cluster
# BST in the cluster


# After labellizing the clusters, we want to study their viability (usage)
# Lots of pokemon are not used
def add_cluster_to_df(df_clusters,df):
    df = df.merge(df_clusters[['Cluster_label']], left_index=True, right_index=True)
    return df

def mean_usage_by_cluster(df_usage):
    mean_usage_by_cluster = df_usage.groupby('Cluster_label')['usage'].mean().reset_index()
    mean_usage_by_cluster.index = mean_usage_by_cluster['Cluster_label']
    mean_usage_by_cluster = mean_usage_by_cluster.drop('Cluster_label', axis=1)
    return mean_usage_by_cluster

def add_percent_of_used(df_usage,df_clusters,mean_usage):
    # compute the number of pokemon in each cluster
    cluster_counts = df_clusters['Cluster_label'].value_counts()
    # compute the number of pokemon used in each cluster
    cluster_used_counts = df_usage['Cluster_label'].value_counts()
    # compute the part of pokemon used in each cluster
    part_used_counts = [100*cluster_used_counts[i]/cluster_counts[i] for i in cluster_used_counts.index]
    # add it to mean_usage_by_cluster
    mean_usage['%_pkmn_used'] = part_used_counts

'''
def mean_BST_by_cluster(stats_clus):
    # compute the mean BST in the cluster
    mean_BST_by_cluster = stats_clus.groupby('Cluster_label')['Total'].mean().reset_index()
    mean_BST_by_cluster.index = mean_BST_by_cluster['Cluster_label']
    mean_BST_by_cluster = mean_BST_by_cluster.drop('Cluster_label', axis=1)
    return mean_BST_by_cluster

def add_BST_to_df(mean_BST,df):
    df['Mean_BST'] = mean_BST['Total']
    return df'''

def part_poke_in_cluster_by_gen(stats,clusters,mapping):
    n_clusters = len(clusters)
    res_array = np.zeros((9, 1 + n_clusters)) # lignes : générations. colonnes : numéro génération + clusters
    # filling the array
    # generation column
    for k_gen in range(9):
        res_array[k_gen,0] = k_gen+1
    # counting the pokemon in each gen in each cluster
    for k_cluster in range(n_clusters): 
        for name in clusters[k_cluster]: # going through each cluster
            res_array[stats.loc[name]['Generation']-1,1+k_cluster]+=1
    # Dividing by the number of pokemon used in the generation
    res_count = res_array.copy()
    for i in range(res_array.shape[0]):
        n_poke_in_gen = (sum(res_array[i])-res_array[i,0])
        for j in range(1,1+n_clusters): # shouldn't include the generation column
            res_array[i,j] /= n_poke_in_gen
    # conversion en dataframe
    res_df = pd.DataFrame(res_array, columns = ['Generation'] + [mapping[i] for i in range(n_clusters)])
    res_df.index = res_df['Generation']
    res_df = res_df.drop('Generation', axis = 1)
    return res_df, res_count

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def usage_in_cluster_gen(stats,df_usage,clusters,mapping,n_poke_by_gen_by_clus):
    n_clusters = len(clusters)
    res_array = np.zeros((9, 1 + n_clusters)) # lignes : générations. colonnes : numéro génération + clusters
    # filling the array
    # generation column
    for k_gen in range(9):
        res_array[k_gen,0] = k_gen+1
    # counting the usage in each gen in each cluster
    for k_cluster in range(n_clusters): 
        for name in clusters[k_cluster]: # going through each cluster
            if name in df_usage.index:
                res_array[stats.loc[name]['Generation']-1,1+k_cluster]+=df_usage.loc[name]['usage']
    # Dividing by the number of pokemon used in the generation
    for i in range(res_array.shape[0]):
        for j in range(1,1+n_clusters): # shouldn't include the generation column
            if n_poke_by_gen_by_clus[i,j] != 0:
                res_array[i,j] /= n_poke_by_gen_by_clus[i,j]
    # conversion en dataframe
    res_df = pd.DataFrame(res_array, columns = ['Generation'] + [mapping[i] for i in range(n_clusters)])
    res_df.index = res_df['Generation']
    res_df = res_df.drop('Generation', axis = 1)
    return res_df 

def plot_clusters_gen(gen_summary,gens_list,upbound,fixed_axis=True):
    for i in gens_list:
        plt.bar(gen_summary.columns.values, gen_summary.loc[i].values)
        plt.xticks(gen_summary.columns.values, rotation='vertical')
        plt.xlabel("Clusters",fontsize=8)
        if fixed_axis:
            plt.ylim(0, upbound)
        plt.ylabel("Part of Pokemon")
        plt.title("Repartition in clusters for gen " + str(i))
        plt.show()

def plot_usage_clusters_gen(gen_summary,gens_list,upbound,fixed_axis=True):
    for i in gens_list:
        plt.bar(gen_summary.columns.values, gen_summary.loc[i].values)
        plt.xticks(gen_summary.columns.values, rotation='vertical')
        plt.xlabel("Clusters",fontsize=8)
        if fixed_axis:
            plt.ylim(0, upbound)
        plt.ylabel("Usage of Pokemon")
        plt.title("Usage in clusters for gen " + str(i))
        plt.show()


def main(list_gens, mode):
    # Import stats Data
    stats_gen = import_stats()
    print(stats_gen.head())
    # Compute clusters
    df_clusters, clusters = calc_clusters_gen(list_gens, stats_gen, mode)
    # Labellize clusters
    df_clusters, mapping = labellize_clusters(clusters,df_clusters)
    print(df_clusters)
    # Import usage data
    df_usage = import_usage()
    # Add the clusters label to iy
    df_usage = add_cluster_to_df(df_clusters,df_usage)
    # Create the summary, containing mean usage in the cluster, % of pokemon actually used in it, and the mean BST of the pokemon
    mean_usage = mean_usage_by_cluster(df_usage)
    add_percent_of_used(df_usage,df_clusters,mean_usage)
    stats_gen_clus = add_cluster_to_df(df_clusters,stats_gen)
    #mean_BST = mean_BST_by_cluster(stats_gen_clus)
    # Create the summary for each generation
    # Contains the part of pokemon in each cluster for each generation and the mean_BST
    #clusters_summary = add_BST_to_df(mean_BST,mean_usage)
    #clusters_summary = clusters_summary.sort_values(by='usage', ascending=True)
    #print('clusters_summary :', clusters_summary.to_string())
    # plot the part of the number of pokemon in each cluster
    part_poke_in_cluster, n_poke_used_by_gen_by_clus = part_poke_in_cluster_by_gen(stats_gen, clusters, mapping)
    plot_clusters_gen(part_poke_in_cluster,[i for i in range(1,10)],0.3)
    # plot the mean usage of a pokemon in a cluster by generation
    usage_in_cluster_by_gen = usage_in_cluster_gen(stats_gen,df_usage,clusters,mapping,n_poke_used_by_gen_by_clus)
    plot_usage_clusters_gen(usage_in_cluster_by_gen,[i for i in range(1,10)],0.07)




print(main([1,2,3,4,5,6,7,8,9],'HAC'))