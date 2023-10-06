from .DataLoader.MongoDBLoader import MongoDBLoader
from .Preprocessor.DataPreprocessor import DataPreprocessor
from .Clustering.agglomerative import Agglomerative
from .DataExporter.MongoDBExporter import MongoDBExporter
from datetime import date as Date
import pandas as pd
import numpy as np 

class Controller:
    def execute(self, date):
        scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores', 'Agent_Accent_Score']
        date = str(date)
        loader = MongoDBLoader()
        processor = DataPreprocessor(loader.get_data(date))
        df = processor.select_data()
        model = Agglomerative()
        for score in scores:
            data = processor.split_and_sort(df, score)
            column_name = f'{score}_Star_Rating'
            for key in data.keys():
                if score == 'Agent_Accent_Score':
                    print('agent scores')
                    labels = model.fit_transform(data[key].values, self.get_n_clusters_by_key(key), self.get_cluster_name_by_key(key), labels=self.get_labels_by_key(key), model_name='kmeans')
                    print(date)
                    print(key)
                    print(np.unique(labels))
                else:
                    labels = model.fit_transform(data[key].values, 2, self.get_cluster_name_by_key(key), labels=self.get_labels_by_key(key))
                data[key].df[column_name] = labels
            results = pd.concat([data[key].df for key in data.keys()])
            df = df.join(results[column_name].to_frame())
        exporter = MongoDBExporter()
        exporter.export_results(df)
        

    def get_labels_by_key(self, key):
        labels = {0: [1, 2], 1: [3], 2: [4, 5], 'us': [3, 4, 5], 'canada_and_england': [2, 3, 4], 'others': [1, 2]}
        return labels[key]
    
    def get_cluster_name_by_key(self, key):
        cluster_names = {0: 'Negative', 1: 'Neutral', 2: 'Positive', 'us': 'us', 'canada_and_england': 'canada_and_england', 'others': 'others'}
        return cluster_names[key]
    
    def get_n_clusters_by_key(self, key):
        cluster_numbers = {'us': 3, 'canada_and_england': 3, 'others': 2}
        return cluster_numbers[key]
    

    

