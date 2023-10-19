import numpy as np


class TransformerMixin:
    """
    Clustering Models assign cluster labels randomly so we don't know which cluster will get which label
    But since we are dealing with rating from 1 to 5, it is important to assign labels from 1 to 5 in assending order of 
    values/points involved in clustering, that is why, we are writing these transformers.
    Also, since each feature might have different type of data, we have defined few different transformers for some features
    """

    def transform_labels(self, data, labels, cluster_labels):
        # replacing cluster labels from our labels
        cluster_labels = np.vectorize(lambda x: float(labels[x]))(cluster_labels)

        # applying transformations
        first = cluster_labels[0]
        last = cluster_labels[-1]
        if cluster_labels[0] == 2 or cluster_labels[0] == 3.0:
            total = sum(labels)
            cluster_labels = (total - cluster_labels)
        elif labels[0] == 4:
            cluster_labels = [labels[2] if x==first else labels[0] if x==last else labels[1] for x in cluster_labels]
        return cluster_labels


    def transform_accent_labels(self, data, labels, cluster_labels):
        # step: 1, get all the unique values along with their indices
        # step: 2, zip the values with indices and sort by their indices so we know which value came first hence we know the exact order of the labels
        # step: 3, finally, replace the labels of the cluster with our actual labels
        unique_values, unique_indices = np.unique(cluster_labels, return_index=True)
        unique_labels = list(zip(unique_values, unique_indices))
        unique_labels = sorted(unique_labels, key=lambda x: x[1])
        unique_labels = list(map(lambda x: x[0], unique_labels))
        cluster_labels = np.vectorize(lambda x: float(labels[unique_labels.index(x)]))(cluster_labels)

        return cluster_labels

    def transform_language_labels(self, data, labels, cluster_labels):
        # step: 1, get the list of labels, there are total 7 labels
        # step: 2, get the list of the average value against each label
        # step: 3, sort the dictionary using averages values we just recieved 
        # step: 4, at this stage, we know which cluster is the first and which one is second, so ultimate ordering of cluster
        # step: 5, finally, get the previous labels of the cluster and replace them with out new ordered labels
        label_averages = {}
        for label in np.unique(cluster_labels):
            current_data = data[cluster_labels==label]
            current_data = np.average(current_data, axis=0, keepdims=True)
            total = np.sum(current_data * 5)
            label_averages[label] = total
        label_averages = sorted(label_averages.items(), key=lambda x: x[1])
        label_averages_keys = list(map(lambda x: x[0], label_averages))
        cluster_labels = np.vectorize(lambda x: float(labels[label_averages_keys.index(x)]))(cluster_labels)
        return cluster_labels