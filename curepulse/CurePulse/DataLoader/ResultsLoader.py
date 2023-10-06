from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId


class MongoDBLoader:
    def __init__(self) -> None:
        self.db_name = 'AI_Bootcamp_Project8_Results'
        self.collection_name = 'Calls_Rating'
        self.con = MongoClient()
        self.db = self.con[self.db_name]
        self.collection = self.db[self.collection_name]



    def get_data(self, date, score):

        data = list(self.collection.find({'Date': date}, {score: True, f'{score}_Star_Rating': True}))
        df = pd.DataFrame(data).rename(columns={score: 'Score', f'{score}_Star_Rating': 'Star'})
        df.columns = ['_id', 'Score', 'Star']
        df['_id'] = df['_id'].apply(str)
        data = {'Date': date, 'ScoreName': [score], 'ClusteredData': df.to_dict(orient='records')}
        return data
    
    def get_data_point(self, _id):
        data =  self.collection.find_one({'_id': ObjectId(str(_id))})
        print(data)
        return data 
    


