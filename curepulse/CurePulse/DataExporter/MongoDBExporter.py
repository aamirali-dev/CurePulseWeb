from pymongo import MongoClient


class MongoDBExporter:
    def __init__(self) -> None:
        self.db_name = 'AI_Bootcamp_Project8_Results'
        self.host = 'localhost'
        self.port = '27017'
        self.collection_name = 'Calls_Rating'

    def export_results(self, results):
        con = MongoClient()
        db = con[self.db_name]
        collection = db[self.collection_name]
        collection.insert_many(results.to_dict(orient='records'))
        con.close()