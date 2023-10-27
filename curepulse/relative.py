import traceback 
import numpy as np
import pandas as pd
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
    
    loader = MongoDBLoader()
    data = []
    for i in range(10,26):
        try:
            data += loader.get_data(str(Date(2023, 10, i)))
        except Exception as e:
            print(f'Task: {e}')
    scores = ['Agent_Text_Scores', 'Agent_Tone_Scores','Client_Tone_Scores', 'Client_Text_Scores']
    controller = Controller()
    df_one = controller.fit_transform_data(data, scores)
    
    processor = DataPreprocessor(data)
    scores = ['Agent_Accent_Score', 'Agent_Langauge_Score_Percentage']
    controller = Controller()
    df_two = controller.fit_transform(Agglomerative(), processor, scores, "10-17 October")
    columns_to_add = df_two.iloc[:, -2:]
    df = pd.concat([df_one, columns_to_add], axis=1)
    s = 'Agent_Tone_Scores'
    grouped = df.groupby([f'{s}_Star_Rating'])
    for category, group in grouped:
        print("Category:", category)
        select_df = group[[s,f'{s}_Star_Rating', f'{s}_Val']].copy()
        select_df[s] = select_df[f'{s}'].apply(dict_to_list)
        select_df[['Negative', 'Neutral', 'Positive']] = select_df[s].apply(pd.Series)
        select_df = select_df.drop(columns=[s])
        print(select_df.sort_values(by=['Positive'], ascending=False))
    exporter = CSVExporter()
    exporter.export_results(df)

update_database_weekly()
