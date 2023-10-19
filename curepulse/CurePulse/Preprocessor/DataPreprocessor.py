from pymongo import MongoClient
import numpy as np
import pandas as pd
from collections import namedtuple


Data = namedtuple('Data', ['df', 'values'])

class DataPreprocessor:
    def __init__(self, data):
        self.data = pd.DataFrame(data).set_index('_id')

    def select_data(self, columns_to_keep = None):
        return self.data

    def split_and_sort(self, data, key):
        if key == 'Agent_Accent_Score':
            return self.split_accent_data(data)
        if key == 'Agent_Language_Scores':
            return self.select_language_data(data, key)

        lists_by_max_index = {}
        # print(key)
        for (id, row) in data[key].items():
            try:
                if isinstance(row, dict):
                    row = list(row.values())
                max_index = np.argmax(row)
                if max_index not in lists_by_max_index:
                    lists_by_max_index[max_index] = []
                lists_by_max_index[max_index].append((id, row))
                # print(row, max_index)
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
        df = pd.concat([df.drop(['Agent_Language_Scores'], axis=1), df['Agent_Language_Scores'].apply(pd.Series)], axis=1)
        df_with_sum = df.copy()
        df_with_sum['SUM'] = df_with_sum.values.sum(axis=1, keepdims=True)
        return {key: Data(df_with_sum, df.values)}

# us: 3 - 5 
# eng + cad: 2-4 (not 4.5)
# others: 1 - 2

    