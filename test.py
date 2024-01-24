import clustering_stats as cs

def add_cluster_to_usage(df_clusters,df_usage):
    df_usage = df_usage.merge(df_clusters[['cluster_number']], left_index=True, right_index=True)
    return df_usage

def main(list_gens, mode):
    stats_gen = cs.import_stats()
    print(stats_gen.head())
    df_clusters, clusters = cs.calc_clusters_gen(list_gens, stats_gen, mode)
    df_usage = cs.import_usage()
    df_usage = add_cluster_to_usage(df_clusters,df_usage)
    mean_usage = cs.mean_usage_by_cluster(clusters, df_usage)
    return mean_usage

main([1,2,3,4,5,6,7,8,9],'HAC')