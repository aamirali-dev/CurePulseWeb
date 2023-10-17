"""
In this file, we define the DataPreprocessor class, which is used to preprocess the data from the database.
"""

from pymongo import MongoClient
import numpy as np
import pandas as pd
from collections import namedtuple


Data = namedtuple('Data', ['df', 'values'])

class DataPreprocessor:
    """
    This class is used to preprocess the data from the database.
    The data is stored in a pandas DataFrame, and the DataPreprocessor class is used to select the data and sort it.
    """
    def __init__(self, data):
        self.data = pd.DataFrame(data).set_index('_id')

    def select_data(self, columns_to_keep = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']):
        """_summary_
        This function is used to select the data from the database.
        Args:
            columns_to_keep (list, optional): _description_. Defaults to ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores'].

        Returns:
            _type_: _description_
        """
        return self.data

    def split_and_sort(self, data : dict, key : str) -> dict:
        """_summary_
        This function is used to split and sort the data.
        Args:
            data (dict): _description_
            key (str): _description_

        Returns:
            dict: _description_
        """
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
        return sorted_lists_dict

    def split_accent_data(self, data : dict) -> dict:
        """_summary_
        This function is used to split the accent data.
        Args:
            data (dict): _description_

        Returns:
            dict: _description_
        """
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


    