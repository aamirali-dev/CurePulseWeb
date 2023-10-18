from pymongo import MongoClient

class MongoDBLoader:
    def __init__(self) -> None:
        self.username = "ai_bootcamp"
        self.password = 'CureMD123'
        self.db_name = 'AI_Bootcamp_Project8'
        self.host = '172.16.101.152'
        self.port = '27017'
        self.collection_name = 'Calls_Data'

    def get_data(self, date):
        con = MongoClient(host=self.host, username=self.username, password=self.password, authSource=self.db_name)
        db = con[self.db_name]
        collection = db[self.collection_name]
        data = list(collection.find({'Date': date}))
        con.close()
        if len(data) <= 0:
            raise ValueError(f'No data is present for {date}')
        return data
