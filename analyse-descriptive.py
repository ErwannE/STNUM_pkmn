import pandas as pd 
import matplotlib.pyplot as plt 

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
plt.subplots(figsize=(8, 6))
dfs['gen01']['Total'].hist()
plt.show()