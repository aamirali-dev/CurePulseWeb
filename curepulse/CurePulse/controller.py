from .DataLoader.MongoDBLoader import MongoDBLoader
from .Preprocessor.DataPreprocessor import DataPreprocessor
from .Clustering.agglomerative import Agglomerative
from .DataExporter.MongoDBExporter import MongoDBExporter
from datetime import date as Date
import pandas as pd
import numpy as np 
import traceback

class Controller:
    def execute(self, date):
        scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores', 'Agent_Accent_Score', 'Agent_Language_Scores']
        date = str(date)
        loader = MongoDBLoader()
        processor = DataPreprocessor(loader.get_data(date))
        results = self.fit_transform(Agglomerative(), processor, scores, date)
        exporter = MongoDBExporter()
        exporter.export_results(results)
    
    def fit_transform(self, model, processor, scores, id):
        df = processor.select_data()
        for score in scores:
            # print(score)
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
                        labels = model.fit_transform_accent(data[key].values, self.get_n_clusters_by_key(key), self.get_cluster_name_by_key(key), labels=self.get_labels_by_key(key), model_name='kmeans')
                    else:
                        labels = model.fit_transform(data[key].values, self.get_n_clusters_by_key(key), self.get_cluster_name_by_key(key), labels=self.get_labels_by_key(key), linkage="average")
                    data[key].df[column_name] = labels
                    # print(data[key].df)
                except ValueError as e:
                    print(f'{score}:{key} has zero sampels on {id}')
            # print(data)
            results = pd.concat([data[key].df for key in data.keys()])
            # print(results[column_name].isna().sum())
            df = df.join(results[column_name].to_frame())
        df = df.fillna(0)
        return df

    def get_labels_by_key(self, key):
        labels = {
            0: [1, 2],
            1: [3, 3.5],
            2: [4, 4.5, 5], 
            'us': [3, 3.5, 4, 4.5, 5],
            'canada_and_england': [2, 3, 3.5, 4], 
            'others': [1, 2],
            'Agent_Language_Scores': [1, 2, 3, 3.5, 4, 4.5, 5],
            'Agent_Langauge_Score_Percentage': [1, 2, 3, 3.5, 4, 4.5, 5]
        }

        list_scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']
        aggregated_scores = [f'{score}_Agg' for score in list_scores]
        if key in aggregated_scores:
            return [1, 2, 3, 3.5, 4, 4.5, 5]
        return labels[key]
    
    def get_cluster_name_by_key(self, key):
        cluster_names = {
            0: 'Negative', 
            1: 'Neutral', 
            2: 'Positive', 
            'us': 'us', 
            'canada_and_england': 'canada_and_england', 
            'others': 'others',
            'Agent_Language_Scores': 'Agent_Language_Scores',
            'Agent_Langauge_Score_Percentage': 'Agent_Langauge_Score_Percentage'
        }
        list_scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']
        aggregated_scores = [f'{score}_Agg' for score in list_scores]
        if key in aggregated_scores:
            return key
        return cluster_names[key]
    
    def get_n_clusters_by_key(self, key):
        cluster_numbers = {
            0: 2, 
            1: 2, 
            2: 3, 
            'us': 5, 
            'canada_and_england': 4, 
            'others': 2, 
            'Agent_Language_Scores': 7,
            'Agent_Langauge_Score_Percentage': 7,
            }
        list_scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']
        aggregated_scores = [f'{score}_Agg' for score in list_scores]
        if key in aggregated_scores:
            return 7
        return cluster_numbers[key]
    


    def fit_transform_x(self, model, processor, scores, id):
        df = processor.select_data()
        for score in scores:
            # print(score)
            column_name = f'{score}_Star_Rating'
            try: 
                if score == 'Agent_Accent_Score':
                    data = processor.split_and_sort(df, score)
                    for key in data.keys():
                        try:
                            labels = model.fit_transform_accent(data[key].values, self.get_n_clusters_by_key(key), self.get_cluster_name_by_key(key), labels=self.get_labels_by_key(key), model_name='kmeans')
                            data[key].df[column_name] = labels
                        except ValueError as e:
                            print(f'{score}:{key} has zero sampels on {id}')
                    results = pd.concat([data[key].df for key in data.keys()])
                    print(results)
                else:
                    data = df[score].values
                    labels = model.fit_transform(data.reshape(-1, 1), self.get_n_clusters_by_key(score), self.get_cluster_name_by_key(score), labels=self.get_labels_by_key(score))
                    results = df[score].to_frame()
                    results[column_name] = labels
                    print(results)
            except Exception as e:
                traceback.print_exc()
                print(f'No data found for {score} on {id}')
                continue
            # print(results[column_name].isna().sum())
            df = df.join(results[column_name].to_frame())
        df = df.fillna(0)
        return df


