import numpy as np
from sklearn.cluster import AgglomerativeClustering, KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from typing import Literal
from scipy.spatial.distance import cdist
from .ModelScoreMixin import ModelScoreMixin
from .TransformerMixin import TransformerMixin


class Agglomerative(ModelScoreMixin, TransformerMixin):
    def __init__(self, n_clusters,cluster_name,linkage:Literal["ward", "average", "single", "complete"]='ward',
                        model_name : Literal["kmeans", "dbscan", "agglomerative"] = "agglomerative"):
        self.n_clusters = n_clusters
        self.cluster_name = cluster_name
        self.linkage = linkage
        self.model_name = model_name

    def fit_transform(self, data, labels=None):
        clustering_models = {
            'kmeans': KMeans(n_clusters=self.n_clusters),
            'dbscan': DBSCAN(eps=0.5, min_samples=5),
            'agglomerative': AgglomerativeClustering(n_clusters=self.n_clusters, linkage=self.linkage)
        }
        
        if data.shape[0] > 1:
            clustering_model = clustering_models[self.model_name.lower()]
            cluster_labels = clustering_model.fit_predict(data)

            original_distortion = self.calculate_distortion(data, cluster_labels)
            centroids = self.calculate_centroids(data, cluster_labels)
            centroid_distances = self.calculate_centroid_distances(centroids)
            silhouette_scores = self.calculate_silhouette_scores(data, cluster_labels)
            
            # if we are dealing with language, we have to apply language transformation otherwise apply default transformations
            # problem is that we are labelling user rating from 1 to 5 hence our labels are ordinal but 
            # all the clustering models return labels randomly
            if len(labels) == 7:
                return self.transform_language_labels(data, labels, cluster_labels)
            return self.transform_labels(data, labels, cluster_labels)
           
        else:
            if self.labels[0]==1:
                return np.array([labels[1]])
            return np.array([labels[0]])
        
    def fit_transform_accent(self, data, labels=None):
        score_list = data
        # kmeans = KMeans(n_clusters=n_clusters)
        kmeans = AgglomerativeClustering(n_clusters=self.n_clusters, linkage=self.linkage)
        score_list = score_list.reshape(-1, 1)
        kmeans.fit(score_list)
        cluster_labels = kmeans.labels_
        return self.transform_accent_labels(data, labels, cluster_labels)

    def should_merge_clusters(self, centroid_distances, silhouette_scores):
        return False
