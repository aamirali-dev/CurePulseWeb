import numpy as np
from sklearn.cluster import AgglomerativeClustering, KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from typing import Literal
from scipy.spatial.distance import cdist


class Agglomerative:

    def fit_transform(self, data, n_clusters,cluster_name,linkage:Literal["ward", "average", "single", "complete"]='ward',
                        labels=None, model_name : Literal["kmeans", "dbscan", "agglomerative"] = "agglomerative"):
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
                # cluster_labels = [labels[0] if label == 0 else labels[1] for label in cluster_labels]
            else:
                # cluster_labels = [3 for _ in cluster_labels]
                cluster_labels *= 0
                cluster_labels += 3
            
            original_distortion = self.calculate_distortion(data, cluster_labels)
            # print("Label:", cluster_name)
            # print(f"Original distortion (Model: {model_name}):", original_distortion)
            
            centroids = self.calculate_centroids(data, cluster_labels)
            # print(f"Centroids (Model: {model_name}):", centroids)
            
            centroid_distances = self.calculate_centroid_distances(centroids)
            # print(f"Centroid distances (Model: {model_name}):", centroid_distances)
            
            silhouette_scores = self.calculate_silhouette_scores(data, cluster_labels)
            # print(f"Silhouette scores (Model: {model_name}):", silhouette_scores)
            # print()
            if cluster_labels[0] == 2 or cluster_labels[0] == 4:
                total = sum(labels)
                cluster_labels = (total - cluster_labels)
                # cluster_labels = [total - label for label in cluster_labels]
            return cluster_labels
        else:
            return np.array([labels[0]])

    def calculate_distortion(self, data, cluster_labels):
        cluster_distortions = []
        for label in np.unique(cluster_labels):
            cluster_data = data[cluster_labels == label]
            centroid = np.mean(cluster_data, axis=0)
            distortion = np.sum(np.linalg.norm(cluster_data - centroid, axis=1) ** 2)
            cluster_distortions.append(distortion)
        
        return cluster_distortions

    def calculate_centroids(self, data, cluster_labels):
        centroids = [np.mean(data[cluster_labels == label], axis=0) for label in np.unique(cluster_labels)]
        return centroids

    def calculate_centroid_distances(self, centroids):
        centroid_distances = cdist(centroids, centroids)
        np.fill_diagonal(centroid_distances, np.inf)
        return centroid_distances

    def calculate_silhouette_scores(self, data, cluster_labels):
        if len(np.unique(cluster_labels)) == 1:
            return [0.0]
        else:
            silhouette_scores = []
            unique_labels = np.unique(cluster_labels)
            
            for label in unique_labels:
                cluster_mask = [x == label for x in cluster_labels]
                if cluster_mask.count(True) > 1:
                    score = silhouette_score(data, cluster_labels, sample_size=None, metric='euclidean')
                    silhouette_scores.append(score)
                else:
                    silhouette_scores.append(0.0)
            
            return silhouette_scores

    def should_merge_clusters(self, centroid_distances, silhouette_scores):
        return False