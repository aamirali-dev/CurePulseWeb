import pandas as pd
import numpy as np

class CSVExporter:
    def __init__(self) -> None:
        self.filename = 'stats.csv'
        self.list_scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']
        self.ratings = [1, 2, 3, 3.5, 4, 4.5, 5]

    def export_results(self, results: pd.DataFrame):
        stats = {}
        df = pd.DataFrame(self.ratings, columns=['Rating'])
        df = df.set_index('Rating')
        for score in self.list_scores:
            column_name = f'{score}_Star_Rating'
            value_counts = results[column_name].value_counts().to_frame()
            value_counts.columns = [f'{score}_Count']
            results[score] = results[score].apply(self.transform_list_to_single_value)
            rating_range = results.groupby(by=[column_name])[score].agg(['min', 'max'])
            rating_range.columns = [f'{score}_Min', f'{score}_Max']
            df = df.join(value_counts)
            df = df.join(rating_range)
            print(df.index)
        
        cols = ['Agent_Accent_Score', 'Agent_Language_Scores']
        score = cols[0]
        column_name = f'{score}_Star_Rating'
        value_counts = results[results['Agent_Accent_Language']=='us'][column_name].value_counts().to_frame()
        value_counts.columns = [f'{score}_US_Count']
        rating_range = results[results['Agent_Accent_Language']=='us'].groupby(by=[column_name])[score].agg(['min', 'max'])
        rating_range.columns = [f'{score}_US_Min', f'{score}_US_Max']
        df = df.join(value_counts)
        df = df.join(rating_range)

        score = cols[0]
        column_name = f'{score}_Star_Rating'
        value_counts = results[results['Agent_Accent_Language'].isin(['england', 'canada'])][column_name].value_counts().to_frame()
        value_counts.columns = [f'{score}_BR_CA_Count']
        rating_range = results[results['Agent_Accent_Language'].isin(['england', 'canada'])].groupby(by=[column_name])[score].agg(['min', 'max'])
        rating_range.columns = [f'{score}_BR_CA_Min', f'{score}_BR_CA_Max']
        df = df.join(value_counts)
        df = df.join(rating_range)

        score = cols[0]
        column_name = f'{score}_Star_Rating'
        print('printing truth faleu0')
        # print(not results['Agent_Accent_Language']==('us' or 'england' or 'canada'))
        value_counts = results[~results['Agent_Accent_Language'].isin(['england', 'canada', 'us'])][column_name].value_counts().to_frame()
        value_counts.columns = [f'{score}_OTHER_Count']
        rating_range = results[~results['Agent_Accent_Language'].isin(['england', 'canada', 'us'])].groupby(by=[column_name])[score].agg(['min', 'max'])
        rating_range.columns = [f'{score}_OTHER_Min', f'{score}_OTHER_Max']
        df = df.join(value_counts)
        df = df.join(rating_range)
        cols = ['Agent_Accent_Score', 'Agent_Language_Scores']

        score = cols[1]
        column_name = f'{score}_Star_Rating'
        value_counts = results[column_name].value_counts().to_frame()
        value_counts.columns = [f'{score}_Count']
        rating_range = results.groupby(by=[column_name])['Agent_Langauge_Score_Percentage'].agg(['min', 'max'])
        rating_range.columns = [f'{score}_Min', f'{score}_Max']
        df = df.join(value_counts)
        df = df.join(rating_range)
        df = df.fillna(0.0).round(decimals=2)
        df.to_csv(self.filename)
    
    def transform_list_to_single_value(self, input):
        if len(input) == 0:
            return 0
        if isinstance(input, dict):
            input = list(input.values())
        idx = np.argmax(input)
        return input[idx]
    
        
