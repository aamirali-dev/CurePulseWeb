from .DataLoader.MongoDBLoader import MongoDBLoader
from .Preprocessor.DataPreprocessor import DataPreprocessor
from .Clustering.agglomerative import Agglomerative
from .DataExporter.MongoDBExporter import MongoDBExporter
import pandas as pd
import numpy as np 
import traceback
from collections import Counter

class Controller:
    def execute(self, date):
        scores = ['Agent_Tone_Scores', 'Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Text_Scores', 'Agent_Accent_Score', 'Agent_Langauge_Score_Percentage']
        date = str(date)
        loader = MongoDBLoader()
        processor = DataPreprocessor(loader.get_data(date))
        results = self.fit_transform(Agglomerative(), processor, scores, date)
        exporter = MongoDBExporter()
        exporter.export_results(results)
    
    def fit_transform(self, model, processor, scores, id):
        df = processor.get_data()
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
                        labels = model.fit_transform_accent(data[key].values, self.get_n_clusters_by_key(key), self.get_cluster_name_by_key(key), labels=self.get_labels_by_key(key), model_name='kmeans')
                    else:
                        labels = model.fit_transform(data[key].values, self.get_n_clusters_by_key(key), self.get_cluster_name_by_key(key), labels=self.get_labels_by_key(key), linkage="ward")
                    data[key].df[column_name] = labels
                except ValueError as e:
                    print(f'{score}:{key} has zero sampels on {id}')
            results = pd.concat([data[key].df for key in data.keys()])
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
    
    def fit_transform_data(self, data, scores):
        processor = DataPreprocessor(data)
        for score in scores:
            orig_data, data = processor.select_data(score)
            mu = np.mean(data)
            sigma = np.std(data)
            grade_ranges = [
            (mu + 2 * sigma, 5.0),
            (mu + 1.25 * sigma, 4.5),
            (mu + 0.625 * sigma, 4.0),
            (mu - 0.625 * sigma, 3.5),
            (mu - 1.25 * sigma, 3.0),
            (mu - 2 * sigma, 2.0),
            (float('-inf'), 1.0)
            ]
            grade_values = []

            for value in data:
                for threshold, grade in grade_ranges:
                    if value >= threshold:
                        grade_values.append(grade)
                        break
            orig_data[f'{score}_Star_Rating'] = grade_values
            # grade_ranges = {}
            # for grade in set(grade_values):
            #     grade_data = [data[i] for i in range(len(grade_values)) if grade_values[i] == grade]
            #     min_score = min(grade_data)
            #     max_score = max(grade_data)
            #     grade_ranges[grade] = (min_score, max_score)
            # print("Maximum" , np.max(data))
            # print("Minimum", np.min(data))
            # grade_counts = Counter(grade_values)
            # for grade, count in grade_counts.items():
            #     print(f"Grade {grade}: {count} times")
            # for grade, (min_score, max_score) in grade_ranges.items():
            #     print(f"Grade {grade}: Range from {min_score} to {max_score}")
        return orig_data
