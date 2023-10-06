from DataLoader.MongoDBLoader import MongoDBLoader
from Preprocessor.DataPreprocessor import DataPreprocessor
from Clustering.agglomerative import Agglomerative
from Plotting.Qt5Agg import Qt5Agg
from DataExporter.MongoDBExporter import MongoDBExporter
from datetime import date as Date
import numpy as np
import pandas as pd

class Controller:
    def execute(self):
        scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']
        date = str(Date(2023, 9, 18))
        loader = MongoDBLoader()
        processor = DataPreprocessor(loader.get_data(date))
        df = processor.select_data()
        model = Agglomerative()
        for score in scores:
            data = processor.split_and_sort(df, score)
            column_name = f'{score}_Star_Rating'
            for key in data.keys():
                labels = model.fit_transform(data[key].values, 2, self.get_cluster_name_by_key(key), labels=self.get_labels_by_key(key))
                data[key].df[column_name] = labels
            results = pd.concat([data[key].df for key in data.keys()])
            df = df.join(results[column_name].to_frame())
        exporter = MongoDBExporter()
        exporter.export_results(df)
        

    def get_labels_by_key(self, key):
        labels = {0: [1, 2], 1: [3], 2: [4, 5]}
        return labels[key]
    
    def get_cluster_name_by_key(self, key):
        cluster_names = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
        return cluster_names[key]

controller = Controller()
controller.execute()