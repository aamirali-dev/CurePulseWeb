"""_summary_
In this module, we have the MongoDBExporter class which is used to export the results to MongoDB.
"""
from pymongo import MongoClient
import pandas as pd

class MongoDBExporter:
    """_summary_
    This is the MongoDBExporter class which is used to export the results to MongoDB.
    """
    def __init__(self) -> None:
        self.db_name = 'AI_Bootcamp_Project8_Results'
        self.host = 'localhost'
        self.port = '27017'
        self.collection_name = 'Calls_Rating'

    def export_results(self, results : pd.DataFrame) -> None:
        """_summary_
        This function is used to export the results to MongoDB.
        Args:
            results (pd.DataFrame): The results dataframe
        """
        con = MongoClient()
        db = con[self.db_name]
        collection = db[self.collection_name]
        collection.insert_many(results.to_dict(orient='records'))
        con.close()