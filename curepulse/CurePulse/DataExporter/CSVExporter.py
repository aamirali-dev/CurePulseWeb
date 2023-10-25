import pandas as pd
import numpy as np

class CSVExporter:
    def __init__(self) -> None:
        self.filename = 'stats.csv'
        self.list_scores = ['Agent_Tone_Scores', 'Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Text_Scores']
        self.ratings = [1, 2, 3, 3.5, 4, 4.5, 5]
        self.current_score = None

    def extract_min(self, df):
        return self.extract_averages(df.head(10))

    def extract_max(self, df):
        return self.extract_averages(df.tail(10))

    def extract_averages(self, df):
        df = np.array([value for value in df.values])
        averages = np.average(df, axis=0)
        return averages

    def export_results(self, results: pd.DataFrame):
        df = pd.DataFrame(self.ratings, columns=['Rating'])
        df = df.set_index('Rating')
        clus_names = {
            "Negative" : 0,
            "Neutral" : 1,
            "Positive" : 2,
        }
        for score in self.list_scores:
            self.current_score = score
            column_name = f'{score}_Star_Rating'
            value_counts = results[column_name].value_counts().to_frame()
            value_counts.columns = [f'{score}_Count']
            # results[f'{score}_Single'] = results[score].apply(self.transform_list_to_single_value)
            results[score] = results[score].apply(self.transform_dict_to_list)
            rating_range = results.groupby(by=[column_name]).apply(self.split_array_to_columns, array_column_name=score, column_name=column_name)
            # print(rating_range)
            # print(rating_range.columns)
            # dadsa
            rating_range = rating_range.reset_index(level=0, drop=True)
            # print("Rating Range Columns")
            # print(rating_range.columns)
            # print("Value Counts Columns")
            # print(value_counts.columns)
            # print("Rating Range Index")
            # print(rating_range.index)
            # print("Value Counts Index")
            # print(value_counts.index)
            # print("Rating Range")
            # print(rating_range)
            # print("Value Counts")
            # print(value_counts)
            df = df.join(value_counts)
            df = df.join(rating_range)
            df = df.fillna(0.0)
        # print(df.T)
        # print(df.columns)
        cols = ['Agent_Accent_Score', 'Agent_Langauge_Score_Percentage']
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
        value_counts = results[~results['Agent_Accent_Language'].isin(['england', 'canada', 'us'])][column_name].value_counts().to_frame()
        value_counts.columns = [f'{score}_OTHER_Count']
        rating_range = results[~results['Agent_Accent_Language'].isin(['england', 'canada', 'us'])].groupby(by=[column_name])[score].agg(['min', 'max'])
        rating_range.columns = [f'{score}_OTHER_Min', f'{score}_OTHER_Max']
        df = df.join(value_counts)
        df = df.join(rating_range)

        score = cols[1]
        column_name = f'{score}_Star_Rating'
        value_counts = results[column_name].value_counts().to_frame()
        value_counts.columns = [f'{score}_Count']
        rating_range = results.groupby(by=[column_name])['Agent_Langauge_Score_Percentage'].agg(['min', 'max'])
        rating_range.columns = [f'{score}_Min', f'{score}_Max']
        df = df.join(value_counts)
        df = df.join(rating_range)
        df = df.fillna(0.0).applymap(lambda x: self.round_array(x) if isinstance(x, list) else round(x, 5))
        df.to_csv(self.filename)
    
    def split_array_to_columns(self, grouped_df, column_name, array_column_name):
        def split_array(row):
            return row[array_column_name][0], row[array_column_name][1], row[array_column_name][2]
        grouped_df[f'{array_column_name}_Negative'], grouped_df[f'{array_column_name}_Neutral'], grouped_df[f'{array_column_name}_Positive'] = zip(*grouped_df.apply(split_array, axis=1))
        max_values = grouped_df.groupby(column_name)[[f'{array_column_name}_Negative', f'{array_column_name}_Neutral', f'{array_column_name}_Positive']].max()
        min_values = grouped_df.groupby(column_name)[[f'{array_column_name}_Negative', f'{array_column_name}_Neutral', f'{array_column_name}_Positive']].min()
        max_values.reset_index(inplace=True)
        min_values.reset_index(inplace=True)
        result = pd.merge(max_values, min_values, on=column_name, suffixes=('_max', '_min'))
        result = result.set_index(column_name)
        new_column_order = [f'{array_column_name}_Negative_min', f'{array_column_name}_Negative_max', f'{array_column_name}_Neutral_min', f'{array_column_name}_Neutral_max', f'{array_column_name}_Positive_min', f'{array_column_name}_Positive_max']
        result.reset_index(inplace=True)
        result.set_index(column_name, inplace=True)
        result = result[new_column_order]
        # print(result.columns)
        # print(result.T)
        # print(result.index)
        # print(result.shape)
        # asds
        return result
    
    def round_array(self, arr):
        return [round(x, 5) for x in arr]
    
    def transform_list_to_single_value(self, input):
        if len(input) == 0:
            return 0
        if isinstance(input, dict):
            input = list(input.values())
        idx = np.argmax(input)
        return input[idx]
    
    def transform_dict_to_list(self, input):
        if isinstance(input, dict):
            input = list(input.values())
        return input
    
        
