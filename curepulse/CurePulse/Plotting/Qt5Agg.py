
import matplotlib.pyplot as plt
import numpy as np

class Qt5Agg:
        
    def plot_3d_clusters_interactive(self, data, cluster_labels):
        plt.switch_backend('Qt5Agg')
        fig = plt.figure()
        
        ax = fig.add_subplot(111, projection='3d')
        unique_labels = np.unique(cluster_labels)
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        for i, label in enumerate(unique_labels):
            cluster_data = data[cluster_labels == label]
            percentage = len(cluster_data) / len(data) * 100
            ax.scatter(
                cluster_data[:, 0], cluster_data[:, 1], cluster_data[:, 2],
                label=f'Rating: {label} Star ({percentage:.2f}%)',
                color=colors[i],
                marker='o',
                s=40,
                alpha=1.0,
                edgecolor='k',
                linewidths=1,
            )

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_zlim(0, 1)
        ax.set_xlabel('Negative Sentiment')
        ax.set_ylabel('Neutral Sentiment')
        ax.set_zlabel('Positive Sentiment')
        ax.legend()
        plt.show(block=True)
