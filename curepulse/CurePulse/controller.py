from .DataLoader.MongoDBLoader import MongoDbDailyDataLoader
from .Preprocessor.DataPreprocessor import DataPreprocessor
from .Clustering.agglomerative import Agglomerative
from .DataExporter.MongoDBExporter import MongoDBExporter
from datetime import date as Date
import pandas as pd
import numpy as np 
import traceback
from .ControllerDataMixin import ControllerDataMixin

class Controller(ControllerDataMixin):
    def __init__(self,
                 scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores', 'Agent_Accent_Score', 'Agent_Language_Scores'],
                 loader = MongoDbDailyDataLoader(),
                 exporter = MongoDBExporter()
                 ):
        self.scores = scores
        self.loader = loader
        self.exporter = exporter

    def execute(self, date):
        date = str(date)
        processor = DataPreprocessor(self.loader.get_data(date))
        results = self.fit_transform(Agglomerative(), processor, self.scores, date)
        self.exporter.export_results(results)
    
    def fit_transform(self, model_x, processor, scores, id):
        df = processor.select_data()
        for score in scores:
            try: 
                data = processor.split_and_sort(df, score)
            except Exception as e:
                traceback.print_exc()
                print(f'No data found for {score} on {id}')
                continue
            column_name = f'{score}_Star_Rating'
            for key in data.keys():
                try:
                    if score == 'Agent_Accent_Score':
                        model = Agglomerative(self.get_n_clusters_by_key(key), self.get_cluster_name_by_key(key), model_name='kmeans')
                        labels = model.fit_transform_accent(data[key].values, labels=self.get_labels_by_key(key))
                    else:
                        model = Agglomerative(self.get_n_clusters_by_key(key), self.get_cluster_name_by_key(key), model_name='agglomerative', linkage="average")
                        labels = model.fit_transform(data[key].values, labels=self.get_labels_by_key(key))
                    data[key].df[column_name] = labels
                except ValueError as e:
                    print(f'{score}:{key} has zero sampels on {id}')
            results = pd.concat([data[key].df for key in data.keys()])
            df = df.join(results[column_name].to_frame())
        df = df.fillna(0)
        return df

    def fit_transform_x(self, model_x, processor, scores, id):
        df = processor.select_data()
        for score in scores:
            column_name = f'{score}_Star_Rating'
            try: 
                if score == 'Agent_Accent_Score':
                    data = processor.split_and_sort(df, score)
                    for key in data.keys():
                        try:
                            model = Agglomerative(self.get_n_clusters_by_key(key), self.get_cluster_name_by_key(key), model_name='kmeans')
                            labels = model.fit_transform_accent(data[key].values, labels=self.get_labels_by_key(key))
                            data[key].df[column_name] = labels
                        except ValueError as e:
                            print(f'{score}:{key} has zero sampels on {id}')
                    results = pd.concat([data[key].df for key in data.keys()])
                else:
                    data = df[score].values
                    model = Agglomerative(self.get_n_clusters_by_key(score), self.get_cluster_name_by_key(score), model_name='kmeans')
                    labels = model.fit_transform(data.reshape(-1, 1), labels=self.get_labels_by_key(score))
                    results = df[score].to_frame()
                    results[column_name] = labels
            except Exception as e:
                traceback.print_exc()
                print(f'No data found for {score} on {id}')
                continue
            df = df.join(results[column_name].to_frame())
        df = df.fillna(0)
        return df
