import traceback 
import random
import pandas as pd
import numpy as np
import math
from datetime import date as Date, timedelta
from celery import shared_task
from CurePulse.controller import Controller
import warnings
from CurePulse.DataLoader.MongoDBLoader import MongoDBLoader
from CurePulse.Preprocessor.DataPreprocessor import DataPreprocessor
from CurePulse.Clustering.agglomerative import Agglomerative
from CurePulse.DataExporter.CSVExporter import CSVExporter
warnings.simplefilter(action='ignore', category=FutureWarning)

@shared_task
def update_database_weekly():
    def dict_to_list(x):
        if isinstance(x, dict):
            return list(x.values())
        return x
    
    def write_to_csv(df, filename = 'results.csv'):
        df.to_csv(filename, index=False)
        
    
    def sorted_data(df, score, type, order = [True, True]):
        select_df = df[[score,f'{score}_Star_Rating']].copy()
        select_df[score] = select_df[f'{score}'].apply(dict_to_list)
        select_df[['Negative', 'Neutral', 'Positive']] = select_df[score].apply(pd.Series)
        select_df = select_df.drop(columns=[score])
        select_df = select_df.sort_values(by=[f'{score}_Star_Rating', type], ascending=order)
        write_to_csv(select_df)
        return select_df
    
    def describe(df, score):
        grouped = df.groupby([f'{score}_Star_Rating'])
        for category, group in grouped:
            print("\nCategory:", category)
            select_df = group[[score,f'{score}_Star_Rating']].copy()
            select_df[score] = select_df[f'{score}'].apply(dict_to_list)
            select_df[['Negative', 'Neutral', 'Positive']] = select_df[score].apply(pd.Series)
            select_df = select_df.drop(columns=[score])
            print(select_df.sort_values(by=['Positive'], ascending=False))
            
    def fit_data(data):
        processor = DataPreprocessor(data)
        scores = ['Agent_Text_Scores', 'Agent_Tone_Scores','Client_Tone_Scores', 'Client_Text_Scores']
        controller = Controller()
        df_one = controller.fit_transform(Agglomerative(), processor, scores, "10-17 October")
        processor = DataPreprocessor(data)
        scores = ['Agent_Accent_Score', 'Agent_Langauge_Score_Percentage']
        controller = Controller()
        df_two = controller.fit_transform(Agglomerative(), processor, scores, "10-17 October")
        columns_to_add = df_two.iloc[:, -2:]
        df = pd.concat([df_one, columns_to_add], axis=1)
        return df
    
    loader = MongoDBLoader()
    data = []
    for i in range(10,26):
        try:
            data += loader.get_data(str(Date(2023, 10, i)))
        except Exception as e:
            print(f'Task: {e}')

    sorting_order = {
        'Negative' : [True, False],
        'Neutral' : [True, False],
        'Positive' : [False, True],
    }
    
    percentages = {
        "Tone" : {
            "Negative" : random.uniform(0.08,0.12),
            "Negative_Total" : 0.25,
            "Neutral" : random.uniform(0.4,0.5),
            "Neutral_Total" : 0.5,
            "Positive" : [random.uniform(1,3), random.uniform(3, 5)],
            "Positive_Total" : 15,
        },
        "Text" : {
            "Negative" : random.uniform(0.04,0.06),
            "Negative_Total" : 0.15,
            "Neutral" : random.uniform(0.4,0.5),
            "Neutral_Total" : 0.5,
            "Positive" : [random.uniform(3.75,6.25), random.uniform(6.25, 8.75)],
            "Positive_Total" : 25,
        }
    }
    
    
    df = fit_data(data)
    scores = ['Agent_Text_Scores', 'Agent_Tone_Scores']
    type_of_score = ['Text', 'Tone']
    for score, type in zip(scores, type_of_score):        
        sorted_df = sorted_data(df, score, 'Negative', sorting_order['Negative'])
        rand = percentages[type]['Negative']
        new_ratings = pd.Series([1] * int(rand * sorted_df.shape[0]) + [2] * int((percentages[type]['Negative_Total'] - rand) * sorted_df.shape[0]))
        sorted_df[f'{score}_Star_Rating'] = 0
        sorted_df = sorted_df.sort_values(by=['Negative'], ascending=False)
        sorted_df[f'{score}_Star_Rating'].iloc[0:len(new_ratings)] = new_ratings
        df[f'{score}_Star_Rating'] = sorted_df[f'{score}_Star_Rating']
        condition = (sorted_df['Negative'] == 0) & (sorted_df[f'{score}_Star_Rating'] == 2)
        df.loc[condition, f'{score}_Star_Rating'] = 0
        
        sorted_df = sorted_data(df, score, 'Positive', sorting_order['Positive'])
        num1 = percentages[type]['Positive'][0]
        num2 = percentages[type]['Positive'][1]
        num3 = percentages[type]['Positive_Total'] - num1 - num2
        new_ratings = pd.Series([4] * int(num3 / 100 * sorted_df.shape[0]) + [4.5] * int(num2 / 100 * sorted_df.shape[0]) + [5] * int(num1 / 100 * sorted_df.shape[0]))
        sorted_df[f'{score}_Star_Rating'].iloc[-len(new_ratings):] = new_ratings
        df[f'{score}_Star_Rating'] = sorted_df[f'{score}_Star_Rating']
        
        sorted_df = sorted_data(df, score, 'Neutral', sorting_order['Neutral'])
        available = (sorted_df[f'{score}_Star_Rating'] == 0).sum()
        rand = percentages[type]['Neutral']
        new_ratings = pd.Series([3.5] * int(rand * available) + [3] * (available - int(rand * available)))
        sorted_df[f'{score}_Star_Rating'].iloc[0:len(new_ratings)] = new_ratings
        df[f'{score}_Star_Rating'] = sorted_df[f'{score}_Star_Rating']
        
        sorted_df = sorted_data(df, score, 'Negative', sorting_order['Negative'])
        print(df[f'{score}_Star_Rating'].value_counts())
            
    exporter = CSVExporter()
    exporter.export_results(df)
        
    print("Total Values:", len(data))
    
update_database_weekly()
