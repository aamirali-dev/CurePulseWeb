import numpy as np
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist


class ModelScoreMixin:
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