from pymongo import MongoClient
import numpy as np
import pandas as pd
from collections import namedtuple


Data = namedtuple('Data', ['df', 'values'])

class DataPreprocessor:
    def __init__(self, data):
        self.data = pd.DataFrame(data).set_index('_id')

    def select_data(self, columns_to_keep = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']):
        return self.data

    def split_and_sort(self, data, key):
        if key == 'Agent_Accent_Score':
            return self.split_accent_data(data)

        lists_by_max_index = {}
        for (id, row) in data[key].items():
            max_index = np.argmax(row)
            if max_index not in lists_by_max_index:
                lists_by_max_index[max_index] = []
            lists_by_max_index[max_index].append((id, row))
        
        sorted_lists_dict = {max_index: sorted(sublists, key=lambda x: x[1][max_index], reverse=True) for max_index, sublists in lists_by_max_index.items()}
        sorted_lists_dict = {index: pd.DataFrame(sublist, columns=['_id', key]).set_index('_id') for index, sublist in sorted_lists_dict.items()}
        sorted_lists_dict = {index: Data(df,np.array([item[0] for item in df.values])) for index, df in sorted_lists_dict.items()}
        
        # for i, sublist in sorted_lists_dict.items():
        #     print(f"List Number {i}:")
        #     print("Total Calls:", len(sublist))
        #     print("Percent of Total Calls:", round(len(sublist) / len(data) * 100, 2), "%")
        #     print(sublist)
        #     print()
    
        return sorted_lists_dict

    def process_data(self, data, key):
        pass 

    def split_accent_data(self, data):
        data = data[['Agent_Accent_Score', 'Agent_Accent_Language']]
        us = data.loc[data['Agent_Accent_Language']=='us']
        canada = data.loc[data['Agent_Accent_Language']=='canada']
        others = data.loc[data['Agent_Accent_Language'] != 'us']
        others = others.loc[others['Agent_Accent_Language'] != 'canada']
        data = {
            'us': Data(us, us['Agent_Accent_Score'].values),
            'canada': Data(canada, canada['Agent_Accent_Score'].values),
            'others': Data(others, others['Agent_Accent_Score'].values),
        }
        return data


    