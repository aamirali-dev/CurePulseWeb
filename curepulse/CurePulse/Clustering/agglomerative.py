"""
In this module, we have the Agglomerative class which is used to cluster the data using Agglomerative Clustering.
"""

import numpy as np
from sklearn.cluster import AgglomerativeClustering, KMeans, DBSCAN
from typing import Literal


class Agglomerative:
    """_summary_
    This is the aggolomerative class which is used to cluster the data using Agglomerative Clustering.
    """

    def fit_transform(self, data : np.array, n_clusters : int, linkage : Literal["ward", "average", "single", "complete"] = 'ward',
                        labels = None, model_name : Literal["kmeans", "dbscan", "agglomerative"] = "agglomerative") -> np.array:
        """_summary_
        This function is sued to do clustering on the data using Agglomerative Clustering.
        Args:
            data (np.array): Array of data points, each consisting of three probabilities
            n_clusters (int): Numbe rof clusters
            linkage (Literal[&quot;ward&quot;, &quot;average&quot;, &quot;single&quot;, &quot;complete&quot;], optional): _description_. Defaults to 'ward'.
            labels (list, optional): The custom labels to be given to each cluster. Defaults to None.
            model_name (Literal[&quot;kmeans&quot;, &quot;dbscan&quot;, &quot;agglomerative&quot;], optional): The model used to do clustering. Defaults to "agglomerative".

        Returns:
            np.array: Labels of the clusters
        """
        clustering_models = {
            'kmeans': KMeans(n_clusters=n_clusters),
            'dbscan': DBSCAN(eps=0.5, min_samples=5),
            'agglomerative': AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        }
        if data.shape[0] > 1:
            clustering_model = clustering_models[model_name.lower()]
            cluster_labels = clustering_model.fit_predict(data)
            if len(labels) == 2:
                cluster_labels += labels[0]
            else:
                cluster_labels *= 0
                cluster_labels += 3

            if cluster_labels[0] == 2 or cluster_labels[0] == 4:
                total = sum(labels)
                cluster_labels = (total - cluster_labels)
            return cluster_labels
        else:
            return np.array([labels[0]])
    
    def fit_transform_accent(self, data : np.array, n_clusters : int, labels=None) -> np.array:
        """_summary_
        This function is sued to do clustering on the accent data using Agglomerative Clustering.
        Args:
            data (np.array): Array of data points, each consisting of three probabilities
            n_clusters (int): Numbe rof clusters
            linkage (Literal[&quot;ward&quot;, &quot;average&quot;, &quot;single&quot;, &quot;complete&quot;], optional): _description_. Defaults to 'ward'.
            labels (list, optional): The custom labels to be given to each cluster. Defaults to None.
        Returns:
            np.array: Labels of the clusters
        """
        score_list = data
        kmeans = KMeans(n_clusters=n_clusters)
        score_list = score_list.reshape(-1, 1)
        kmeans.fit(score_list)
        cluster_labels = kmeans.labels_
        first = cluster_labels[0]
        last = cluster_labels[-1]
        if len(labels) == 2:
            cluster_labels = [labels[0] if x==first else labels[1] for x in cluster_labels]
        else:
            cluster_labels = [labels[0] if x==first else labels[2] if x==last else labels[1] for x in cluster_labels]
        return cluster_labels