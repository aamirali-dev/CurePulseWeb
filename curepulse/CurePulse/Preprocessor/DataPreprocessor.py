from pymongo import MongoClient
import numpy as np
import pandas as pd
from collections import namedtuple


Data = namedtuple('Data', ['df', 'values'])

class DataPreprocessor:
    def __init__(self, data):
        self.data = pd.DataFrame(data).set_index('_id')

    def dict_to_list(self, x):
        if isinstance(x, dict):
            # print(list(x.values()))
            return list(x.values())
        return x
    
    def get_data(self):
        return self.data
    
    def select_data(self, column):
        if column == 'Agent_Accent_Score':
            return self.split_accent_data(data)
        if column == 'Agent_Langauge_Score_Percentage':
            return self.select_language_data(data, column)
        
        raw_data = self.data[column]
        raw_data = raw_data.apply(self.dict_to_list)
        raw_data = np.array(raw_data.values.tolist())
        factors = np.array([1, 5, 10])
        data = np.sum(raw_data * factors, axis=1)
        data = data.reshape(-1, 1)
        return self.data, data

    def split_and_sort(self, data, key):
        if key == 'Agent_Accent_Score':
            return self.split_accent_data(data)
        if key == 'Agent_Langauge_Score_Percentage':
            return self.select_language_data(data, key)

        lists_by_max_index = {}
        for (id, row) in data[key].items():
            try:
                if isinstance(row, dict):
                    row = list(row.values())
                max_index = np.argmax(row)
                if max_index not in lists_by_max_index:
                    lists_by_max_index[max_index] = []
                lists_by_max_index[max_index].append((id, row))
            except:
                continue
        sorted_lists_dict = {max_index: sorted(sublists, key=lambda x: x[1][max_index], reverse=True) for max_index, sublists in lists_by_max_index.items()}
        sorted_lists_dict = {index: pd.DataFrame(sublist, columns=['_id', key]).set_index('_id') for index, sublist in sorted_lists_dict.items()}
        sorted_lists_dict = {index: Data(df,np.array([item[0] for item in df.values])) for index, df in sorted_lists_dict.items()}
    
        return sorted_lists_dict

    def process_data(self, columns, new_columns, transformations):
        for i in range(len(columns)):
            self.data[new_columns[i]] = self.data[columns[i]].apply(transformations[i])

    def split_accent_data(self, data):
        score = 'Agent_Accent_Score'
        language = 'Agent_Accent_Language'
        data = data[[score, language]]
        us = data.loc[data[language]=='us']
        canada = data.loc[data[language]=='canada']
        england = data.loc[data[language]=='england']
        canada_and_england = pd.concat([canada, england])
        others = data.loc[data[language] != 'us']
        others = others.loc[others[language] != 'canada']
        others = others.loc[others[language] != 'england']

        data = {'us': us, 'canada_and_england': canada_and_england, 'others': others}
        keys = ['us', 'canada_and_england', 'others']
        for key in keys:
            data[key] = data[key].sort_values(score)
            data[key] = Data(data[key], data[key][score].values.reshape(-1, 1))
        return data
    
    def select_language_data(self, data, key):
        df = data[key].to_frame()
        df = pd.concat([df.drop(['Agent_Langauge_Score_Percentage'], axis=1), df['Agent_Langauge_Score_Percentage'].apply(pd.Series)], axis=1)
        df_with_sum = df.copy()
        df_with_sum['SUM'] = df_with_sum.values.sum(axis=1, keepdims=True)
        return {key: Data(df_with_sum, df.values)}
    
    