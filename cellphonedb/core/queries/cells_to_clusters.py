import logging

import pandas as pd


def call(meta, counts, genes):
    cellphone_counts = _filter_by_cellphone_genes(counts, genes)
    clusters = _create_clusters_structure(cellphone_counts, meta)

    return _clusters_ratio(clusters)


def _clusters_ratio(counts):
    all_cells_names = next(iter(counts.values())).index

    result = pd.DataFrame(None, all_cells_names)
    for cluster_name in counts:
        logging.info('Transforming Cluster %s' % cluster_name)
        cluster = counts[cluster_name]

        cells_names = cluster.columns.values
        number_cells = len(cells_names)
        cluster_count_value = cluster.apply(lambda row: sum(row.astype('bool')) / number_cells, axis=1)
        result[cluster_name] = cluster_count_value

    return result


def _filter_by_cellphone_genes(cluster_counts, genes):
    """
    Merges cluster genes with CellPhoneDB values
    :type cluster_counts: pd.DataFrame
    :rtype: pd.DataFrame
    """

    multidata_counts = pd.merge(cluster_counts, genes, left_index=True, right_on='ensembl')
    multidata_counts.rename(index=str, columns={'ensembl': 'gene'}, inplace=True)
    multidata_counts.set_index('gene', inplace=True)
    return multidata_counts


def _create_clusters_structure(counts, meta):
    logging.info('Creating Cluster Structure')
    cluster_names = meta['cell_type'].unique()

    logging.info(cluster_names)
    clusters = {}
    for cluster_name in cluster_names:
        cluster_cell_names = pd.DataFrame(meta.loc[(meta['cell_type'] == '%s' % cluster_name)]).index
        clusters[cluster_name] = counts.loc[:, cluster_cell_names]

    return clusters
