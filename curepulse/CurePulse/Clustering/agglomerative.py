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

            original_distortion = self.calculate_distortion(data, cluster_labels)
            
            centroids = self.calculate_centroids(data, cluster_labels)
            
            centroid_distances = self.calculate_centroid_distances(centroids)
            
            silhouette_scores = self.calculate_silhouette_scores(data, cluster_labels)
            
            if len(labels) == 7:
                return self.transform_language_labels(data, labels, cluster_labels)
            cluster_labels = np.vectorize(lambda x: float(labels[x]))(cluster_labels)
            first = cluster_labels[0]
            last = cluster_labels[-1]
            if cluster_labels[0] == 2 or cluster_labels[0] == 3.0:
                total = sum(labels)
                cluster_labels = (total - cluster_labels)
            elif labels[0] == 4:
                cluster_labels = [labels[2] if x==first else labels[0] if x==last else labels[1] for x in cluster_labels]
            return cluster_labels
        else:
            if labels[0]==1:
                return np.array([labels[1]])
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
    
    def fit_transform_accent(self, data, n_clusters,cluster_name,linkage:Literal["ward", "average", "single", "complete"]='ward',
                        labels=None, model_name : Literal["kmeans", "dbscan", "agglomerative"] = "agglomerative"):
        score_list = data
        # kmeans = KMeans(n_clusters=n_clusters)
        kmeans = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        score_list = score_list.reshape(-1, 1)
        kmeans.fit(score_list)
        cluster_labels = kmeans.labels_
        unique_values, unique_indices = np.unique(cluster_labels, return_index=True)
        unique_labels = list(zip(unique_values, unique_indices))
        unique_labels = sorted(unique_labels, key=lambda x: x[1])
        unique_labels = list(map(lambda x: x[0], unique_labels))
        cluster_labels = np.vectorize(lambda x: float(labels[unique_labels.index(x)]))(cluster_labels)

        return cluster_labels

    def transform_language_labels(self, data, labels, cluster_labels):
        label_averages = {}
        for label in np.unique(cluster_labels):
            current_data = data[cluster_labels==label]
            current_data = np.average(current_data, axis=0, keepdims=True)
            total = np.sum(current_data * 5)
            label_averages[label] = total
        label_averages = sorted(label_averages.items(), key=lambda x: x[1])
        label_averages_keys = list(map(lambda x: x[0], label_averages))
        cluster_labels = np.vectorize(lambda x: float(labels[label_averages_keys.index(x)]))(cluster_labels)
        # print(label_averages)
        # print(label_averages_keys)
        return cluster_labels