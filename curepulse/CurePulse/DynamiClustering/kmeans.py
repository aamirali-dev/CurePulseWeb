from pymongo import MongoClient
import numpy as np
import pandas as pd

class MongoDBLoader:
    def __init__(self) -> None:
        self.username = "ai_bootcamp"
        self.password = 'CureMD123'
        self.db_name = 'AI_Bootcamp_Project8'
        self.host = '172.16.101.152'
        self.port = '27017'
        self.collection_name = 'Calls_Data'

    def get_data(self, date='2023-09-08'):
        con = MongoClient(host=self.host, username=self.username, password=self.password, authSource=self.db_name)
        db = con[self.db_name]
        collection = db[self.collection_name]
        data = list(collection.find({'Date': date}))
        con.close()
        return data


class DataPreprocessor:
    def __init__(self, data):
        self.data = pd.DataFrame(data).set_index('_id')

    def select_data(self, columns_to_keep = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']):
        if isinstance(self.data[columns_to_keep], pd.Series):
            return self.data[columns_to_keep].to_frame()
        return self.data[columns_to_keep]

    def split_and_sort(self, data, key):
        from collections import namedtuple

        lists_by_max_index = {}
        for (id, row) in data[key].items():
            max_index = np.argmax(row)
            if max_index not in lists_by_max_index:
                lists_by_max_index[max_index] = []
            lists_by_max_index[max_index].append((id, row))
        
        sorted_lists_dict = {max_index: sorted(sublists, key=lambda x: x[1][max_index], reverse=True) for max_index, sublists in lists_by_max_index.items()}
        sorted_lists_dict = {index: pd.DataFrame(sublist, columns=['_id', key]).set_index('_id') for index, sublist in sorted_lists_dict.items()}
        Data = namedtuple('Data', ['df', 'values'])
        sorted_lists_dict = {index: Data(df,np.array([item[0] for item in df.values])) for index, df in sorted_lists_dict.items()}
        
        for i, sublist in sorted_lists_dict.items():
            print(f"List Number {i}:")
            print("Total Calls:", len(sublist))
            print("Percent of Total Calls:", round(len(sublist) / len(data) * 100, 2), "%")
            print(sublist)
            print()
    
        return sorted_lists_dict

    def process_data(self, data, key):
        pass 

loader = MongoDBLoader()
processor = DataPreprocessor(loader.get_data('2023-09-08'))
data = processor.select_data('Client_Tone_Scores')
# data = processor.split_and_sort(processor.select_data(), 'Client_Tone_Scores')
sentiment_probs = np.array([item[0] for item in data.values])


import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D  # Import 3D plotting

# Determine the optimal number of clusters using the Gap Statistic
def calculate_gap_statistic(data, max_clusters=5, n_bootstrap=5):
    gaps = []
    for k in range(1, max_clusters + 1):
        gap = 0
        for _ in range(n_bootstrap):
            kmeans = KMeans(n_clusters=k)
            kmeans.fit(data)
            original_inertia = kmeans.inertia_

            random_data = np.random.rand(*data.shape)
            kmeans.fit(random_data)
            random_inertia = kmeans.inertia_

            gap += np.log(random_inertia / original_inertia)
        gap /= n_bootstrap
        gaps.append(gap)
    return gaps

gap_values = calculate_gap_statistic(sentiment_probs, max_clusters=5, n_bootstrap=5)

# Find the optimal number of clusters as the index of the maximum Gap Statistic
optimal_n_clusters = np.argmax(gap_values) + 1  # Add 1 because indices are 0-based
print('Best number of clusters: ', optimal_n_clusters)
# Create K-Means model with the optimal number of clusters
kmeans = KMeans(n_clusters=optimal_n_clusters)
cluster_assignments = kmeans.fit_predict(sentiment_probs)

# Visualize the results in a 3D scatter plot
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Extract individual dimensions from sentiment_probs
x = sentiment_probs[:, 0]
y = sentiment_probs[:, 1]
z = sentiment_probs[:, 2]

ax.scatter(x, y, z, c=cluster_assignments, cmap='viridis', s=100, label='Clusters')
ax.set_xlabel('Negative Probability')
ax.set_ylabel('Neutral Probability')
ax.set_zlabel('Positive Probability')
ax.set_title('Customer Call Sentiment Clustering (3D)')
plt.legend()
plt.show()

print("Optimal Number of Clusters:", optimal_n_clusters)
