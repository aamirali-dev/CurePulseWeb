"""_summary_
This is the MongoDB Loader file which is used to load the data from the MongoDB.
"""

from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId


class MongoDBLoader:
    """_summary_
    This class is used to load the data from the MongoDB.
    """
    def __init__(self) -> None:
        """_summary_
        This is the constructor of the MongoDBLoader class.
        """
        self.db_name = 'AI_Bootcamp_Project8_Results'
        self.collection_name = 'Calls_Rating'
        self.con = MongoClient()
        self.db = self.con[self.db_name]
        self.collection = self.db[self.collection_name]

    def get_data(self, date : int, score : str) -> list(pd.DataFrame):
        """_summary_
        This function is used to get the data from the MongoDB.
        Args:
            date (int): _description_
            score (str): _description_

        Returns:
            list(pd.DataFrame): _description_
        """
        if score == 'Agent_Accent_Score':
            return self.get_accent_data(date, score)

        data = list(self.collection.find({'Date': date}, {score: True, f'{score}_Star_Rating': True}))
        df = pd.DataFrame(data).rename(columns={score: 'Score', f'{score}_Star_Rating': 'Star'})
        df['_id'] = df['_id'].apply(str)
        data = {'Date': date, 'ScoreName': [score], 'ClusteredData': df.to_dict(orient='records')}
        return data
    
    def get_data_point(self, obj_id : str) -> pd.DataFrame:
        """_summary_
        This function is used to get the data point from the MongoDB.
        Args:
            obj_id (str): _description_

        Returns:
            pd.DataFrame: _description_
        """
        data =  self.collection.find_one({'_id': ObjectId(str(obj_id))})
        data['obj_id'] = str(data['_id'])
        del data['_id']
        return data 
    
    def get_accent_data(self, date :int , score:str)->pd.DataFrame:
        """_summary_
        This function is used to get the data from the MongoDB.
        Args:
            date (int): _description_
            score (str): _description_

        Returns:
            pd.DataFrame: _description_
        """
        data = list(self.collection.find({'Date': date}, {score: True, f'{score}_Star_Rating': True, 'Agent_Accent_Language': True}))
        df = pd.DataFrame(data).rename(columns={score: 'Score', f'{score}_Star_Rating': 'Star', 'Agent_Accent_Language': 'Language'})
        df['_id'] = df['_id'].apply(str)
        data = {'Date': date, 'ScoreName': [score], 'ClusteredData': df.to_dict(orient='records')}
        return data

    


