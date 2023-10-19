from pymongo import MongoClient
from datetime import timedelta

class MongoDbDailyDataLoader:
    def __init__(self) -> None:
        self.username = "ai_bootcamp"
        self.password = 'CureMD123'
        self.db_name = 'AI_Bootcamp_Project8'
        self.host = '172.16.101.152'
        self.port = '27017'
        self.collection_name = 'Calls_Data'
        self.con = None
        self.db = None
        self.collection = None

    def _init_database(self):
        if self.collection is None:
            self._get_collection()

    def _get_connection(self):
        if self.con is None:
            self.con = MongoClient(host=self.host, username=self.username, password=self.password, authSource=self.db_name) 

    def _get_collection(self):
        if self.con is None:
            self._get_connection()
            self.db = self.con[self.db_name]
            self.collection = self.db[self.collection_name] 

    def _close_connection(self):
        self.con.close()

    def get_data(self, date):
        self._init_database()
        data = list(self.collection.find({'Date': date}))
        if len(data) <= 0:
            raise ValueError(f'No data is present for {date}')
        self._close_connection()
        return data
    
class MongoDbRangeBasedDataLoader(MongoDbDailyDataLoader):
    def __init__(self, numdays) -> None:
        self.numdays = numdays
        super().__init__()

    def get_data(self, start_date):
        self._init_database()

        data = []
        for i in range(self.numdays):
            try:
                date = str(start_date + timedelta(days=i))
                todays_data = list(self.collection.find({'Date': date}))
                if len(todays_data) <= 0:
                    print(f'No data is present for {date}')
                else:
                    data += todays_data
            except Exception as e:
                print(f'Task: {e}')
        self._close_connection()
        return data

class MongoDbWeeklyDataLoader(MongoDbRangeBasedDataLoader):
    def __init__(self) -> None:
        super().__init__(7)

    def get_data(self, start_date):
        return super().get_data(start_date) 
