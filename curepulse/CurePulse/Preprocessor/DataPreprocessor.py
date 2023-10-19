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

        # Sort the lists by max_index and values in descending order
        sorted_lists_dict = {max_index: sorted(sublists, key=lambda x: x[1][max_index], reverse=True) for max_index, sublists in lists_by_max_index.items()}

        # Convert the sorted lists to DataFrames with '_id' as the index
        sorted_lists_dict = {index: pd.DataFrame(sublist, columns=['_id', key]).set_index('_id') for index, sublist in sorted_lists_dict.items()}

        # Convert the DataFrames to Data objects with '_id' and 'key' values
        sorted_lists_dict = {index: Data(df, np.array([item[0] for item in df.values])) for index, df in sorted_lists_dict.items()}

        return sorted_lists_dict


    def process_data(self, columns, new_columns, transformations):
        # take a list of transformations and apply them to the data
        for i in range(len(columns)):
            self.data[new_columns[i]] = self.data[columns[i]].apply(transformations[i])

    def split_accent_data(self, data):
        # Define column names for accent score and accent language
        score = 'Agent_Accent_Score'
        language = 'Agent_Accent_Language'

        # Select only the relevant columns in the data
        data = data[[score, language]]

        # Separate data into three groups based on accent language
        us = data.loc[data[language] == 'us']
        canada = data.loc[data[language] == 'canada']
        england = data.loc[data[language] == 'england']

        # Combine Canada and England data into a single group
        canada_and_england = pd.concat([canada, england])

        # Filter the remaining data for other languages
        others = data.loc[data[language] != 'us']
        others = others.loc[others[language] != 'canada']
        others = others.loc[others[language] != 'england']

        # Store the grouped data in a dictionary
        data = {'us': us, 'canada_and_england': canada_and_england, 'others': others}

        keys = ['us', 'canada_and_england', 'others']
        for key in keys:
            # Sort the data based on accent score
            data[key] = data[key].sort_values(score)

            # Format the data as required
            data[key] = Data(data[key], data[key][score].values.reshape(-1, 1))

        return data


    def select_language_data(self, data, key):
        # Step 1: Convert data associated with 'key' to a DataFrame
        df = data[key].to_frame()

        # Step 2: Expand 'Agent_Language_Scores' into separate columns so dict is converted into 6 seperate columns
        df = pd.concat([df.drop(['Agent_Language_Scores'], axis=1), df['Agent_Language_Scores'].apply(pd.Series)], axis=1)

        # Step 3: Create a copy of the DataFrame since we are adding another column which we don't want to get stored in the final results
        df_with_sum = df.copy()

        # Step 4: Calculate the sum of values across rows and add a 'SUM' column
        df_with_sum['SUM'] = df_with_sum.values.sum(axis=1, keepdims=True)

        # Step 5: Return the processed data as a dictionary
        return {key: Data(df_with_sum, df.values)}

    