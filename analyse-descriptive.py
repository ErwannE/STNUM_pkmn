import pandas as pd 
import matplotlib.pyplot as plt 

import sqlite3 


stats_list = ["Total","HP","Attack","Defense","Sp. Atk","Sp. Def","Speed"]

# Creation of a dictionary that contains a dataframe for every gen file
repert = 'stats_pokemons/'
dfs = {}
for i in range(1, 10):
    dfs["gen0{0}".format(i)] = pd.read_csv(repert + 'gen0' + str(i) + '.csv')



def mean_stats(dfs, n_gen, evolved):
    # Returns a dictionary of the mean of stats (only on evolved pokemon if "evolved") for generation n_gen
    res = {}
    # initialize res
    for stat in stats_list:
        res[stat] = 0
    if not evolved:
        for stat in stats_list:
            res[stat] = dfs['gen0'+str(n_gen)][stat].mean()
        return res
    else:
        for stat in stats_list:
            n_evolved_pkmn = 0 # number of evolved pokemon in the generation
            for i_pkmn in range(len(dfs['gen0'+str(n_gen)])):
                if not dfs['gen0'+str(n_gen)]['Can Evolve'][i_pkmn]: 
                    res[stat] += dfs['gen0'+str(n_gen)][stat][i_pkmn] 
                    n_evolved_pkmn += 1 
            res[stat] /= n_evolved_pkmn
        return res
        
def var_stats(dfs, n_gen, evolved):
    # Returns a dictionary of the variance of stats (only on evolved pokemon if "evolved") for generation n_gen
    res = {}
    # initialize res
    for stat in stats_list:
        res[stat] = 0
    if not evolved:
        for stat in stats_list:
            res[stat] = dfs['gen0'+str(n_gen)][stat].var()
        return res
    else:
        for stat in stats_list:
            n_evolved_pkmn = 0 # number of evolved pokemon in the generation
            for i_pkmn in range(len(dfs['gen0'+str(n_gen)])):
                if not dfs['gen0'+str(n_gen)]['Can Evolve'][i_pkmn]: 
                    res[stat] += (dfs['gen0'+str(n_gen)][stat][i_pkmn] - mean_stats(dfs,n_gen,evolved)[stat])**2
                    n_evolved_pkmn += 1 
            res[stat] /= n_evolved_pkmn
        return res

# Plotting the evolution of each stat through generations
"""plt.subplots(figsize=(8, 6))
dfs['gen01']['Total'].hist()
plt.show()"""

def compute_mean_stats(typing = ["Grass", "Fire", "Water", "Bug", "Normal", "Poison", "Electric", "Ground", "Fairy", "Fighting", "Psychic", "Rock", "Ghost", "Ice", "Dragon", "Dark", "Steel", "Flying"], gen=[i for i in range(1,10)], stats_list = ["Total","HP","Attack","Defense","Sp. Atk","Sp. Def","Speed"]):
    if type(typing) == str:
        typing = [typing]
    if type(gen) == int:
        gen = [gen]
    if type(stats_list) == str:
        stats_list = [stats_list]
    conn = sqlite3.connect('STNUM_pokemon.db') #Outil permettant d'exploiter la base de donnée
    mean_stats = ["AVG(\"" + stat + "\")" for stat in stats_list]
    request = 'SELECT ' + ', '.join(mean_stats) +"FROM Pokemon WHERE (Type1 IN (" + ', '.join(['"'+t+'"' for t in typing]) + ') OR Type2 IN (' + ', '.join(['"'+t+'"' for t in typing]) + ') ) AND Generation IN (' + ', '.join([str(g) for g in gen]) + ') AND "Can_Evolve" = 0'
    #print(request)
    df_stats_evolution = pd.read_sql(request, conn)
    return df_stats_evolution




def plot_mean_stats(typing = ["Grass", "Fire", "Water", "Bug", "Normal", "Poison", "Electric", "Ground", "Fairy", "Fighting", "Psychic", "Rock", "Ghost", "Ice", "Dragon", "Dark", "Steel", "Flying"], gen=[i for i in range(1,10)], stats_list = ["Total","HP","Attack","Defense","Sp. Atk","Sp. Def","Speed"]):
    if type(typing) == str:
        typing = [typing]
    if type(gen) == int:
        gen = [gen]
    if type(stats_list) == str:
        stats_list = [stats_list]
    df = compute_mean_stats(typing, gen, stats_list)
    labels = stats_list
    mean_values = df.values[0]
    if "Total" in labels:
        mean_values[labels.index("Total")] /= 6
        labels[labels.index("Total")] = "Mean"
    plt.bar(labels, mean_values)
    plt.xlabel("Features")
    plt.ylabel("Mean Value")
    plt.title("PCA Mean Values")
    plt.show()


def compute_var_stats(typing = ["Grass", "Fire", "Water", "Bug", "Normal", "Poison", "Electric", "Ground", "Fairy", "Fighting", "Psychic", "Rock", "Ghost", "Ice", "Dragon", "Dark", "Steel", "Flying"], gen=[i for i in range(1,10)], stats_list = ["Total","HP","Attack","Defense","Sp. Atk","Sp. Def","Speed"]):
    if type(typing) == str:
        typing = [typing]
    if type(gen) == int:
        gen = [gen]
    if type(stats_list) == str:
        stats_list = [stats_list]
    conn = sqlite3.connect('STNUM_pokemon.db') #Outil permettant d'exploiter la base de donnée
    mean_stats = ["AVG(\"" + stat + "\")" for stat in stats_list]
    mean_square_stats = ["AVG(\"" + stat + "\"*\"" + stat + "\")" for stat in stats_list]
    var_stats = [mean_square_stats[i] + " - " + mean_stats[i] + "*" + mean_stats[i] for i in range(len(stats_list))]
    request = 'SELECT ' + ', '.join(var_stats) +"FROM Pokemon WHERE (Type1 IN (" + ', '.join(['"'+t+'"' for t in typing]) + ') OR Type2 IN (' + ', '.join(['"'+t+'"' for t in typing]) + ') ) AND Generation IN (' + ', '.join([str(g) for g in gen]) + ') AND "Can_Evolve" = 0'
    df_stats_evolution = pd.read_sql(request, conn)
    return df_stats_evolution

def plot_var_stats(typing = ["Grass", "Fire", "Water", "Bug", "Normal", "Poison", "Electric", "Ground", "Fairy", "Fighting", "Psychic", "Rock", "Ghost", "Ice", "Dragon", "Dark", "Steel", "Flying"], gen=[i for i in range(1,10)], stats_list = ["Total","HP","Attack","Defense","Sp. Atk","Sp. Def","Speed"]):
    if type(typing) == str:
        typing = [typing]
    if type(gen) == int:
        gen = [gen]
    if type(stats_list) == str:
        stats_list = [stats_list]
    df = compute_var_stats(typing, gen, stats_list)
    labels = stats_list
    mean_values = df.values[0]
    if "Total" in labels:
        mean_values[labels.index("Total")] /= 6
        labels[labels.index("Total")] = "Mean"
    plt.bar(labels, mean_values)
    plt.xlabel("Features")
    plt.ylabel("Mean Value")
    plt.title("PCA Mean Values")
    plt.show()

def evolution_mean_stats(stat, typing = ["Grass", "Fire", "Water", "Bug", "Normal", "Poison", "Electric", "Ground", "Fairy", "Fighting", "Psychic", "Rock", "Ghost", "Ice", "Dragon", "Dark", "Steel", "Flying"]):
    if type(typing) == str:
        typing = [typing]
    conn = sqlite3.connect('STNUM_pokemon.db') #Outil permettant d'exploiter la base de donnée
    request = 'SELECT "Generation", AVG("' + stat + '") as avg_stat FROM Pokemon WHERE (Type1 IN ("' + '", "'.join(typing) + '") OR Type2 IN ("' + '", "'.join(typing) + '")) AND "Can_Evolve" = 0 GROUP BY "Generation"'
    df_stats_evolution = pd.read_sql(request, conn)
    return df_stats_evolution

def evolution_var_stats(stat, typing = ["Grass", "Fire", "Water", "Bug", "Normal", "Poison", "Electric", "Ground", "Fairy", "Fighting", "Psychic", "Rock", "Ghost", "Ice", "Dragon", "Dark", "Steel", "Flying"]):
    if type(typing) == str:
        typing = [typing]
    conn = sqlite3.connect('STNUM_pokemon.db') #Outil permettant d'exploiter la base de donnée
    request = 'SELECT "Generation", AVG("' + stat + '"*"' + stat + '")-(AVG("' + stat + '")*AVG("' + stat + '")) as var_stat FROM Pokemon WHERE (Type1 IN ("' + '", "'.join(typing) + '") OR Type2 IN ("' + '", "'.join(typing) + '")) AND "Can_Evolve" = 0 GROUP BY "Generation"' 
    df_stats_evolution = pd.read_sql(request, conn)
    return df_stats_evolution

def var_between_stats(typing = ["Grass", "Fire", "Water", "Bug", "Normal", "Poison", "Electric", "Ground", "Fairy", "Fighting", "Psychic", "Rock", "Ghost", "Ice", "Dragon", "Dark", "Steel", "Flying"], gen=[i for i in range(1,10)], stats_list = ["Total","HP","Attack","Defense","Sp. Atk","Sp. Def","Speed"]):
    if type(typing) == str:
        typing = [typing]
    if type(gen) == int:
        gen = [gen]
    conn = sqlite3.connect('STNUM_pokemon.db') #Outil permettant d'exploiter la base de donnée
    request = 'SELECT "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed" FROM Pokemon WHERE (Type1 IN ("' + '", "'.join(typing) + '") OR Type2 IN ("' + '", "'.join(typing) + '")) AND Generation IN (' + ', '.join([str(g) for g in gen]) + ') AND "Can_Evolve" = 0'
    table_stats = pd.read_sql(request, conn)
    average_var = table_stats.var(axis=1).mean()
    return average_var

def plot_var_between_stats(typing = ["Grass", "Fire", "Water", "Bug", "Normal", "Poison", "Electric", "Ground", "Fairy", "Fighting", "Psychic", "Rock", "Ghost", "Ice", "Dragon", "Dark", "Steel", "Flying"], gen=[i for i in range(1,10)], stats_list = ["Total","HP","Attack","Defense","Sp. Atk","Sp. Def","Speed"]):
    if type(typing) == str:
        typing = [typing]
    if type(gen) == int:
        gen = [gen]
    if type(stats_list) == str:
        stats_list = [stats_list]
    plt.plot(gen, [var_between_stats(typing, i, stats_list) for i in gen], 'o-')
    plt.xlabel("Generation")
    plt.ylabel("Average Variance")
    plt.title("Evolution of the average variance of stats through generations")
    plt.show()

plot_var_between_stats()
    