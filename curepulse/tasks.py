import traceback 

from datetime import date as Date, timedelta
from celery import shared_task
from CurePulse.controller import Controller
import warnings
from CurePulse.DataLoader.MongoDBLoader import MongoDBLoader
from CurePulse.Preprocessor.DataPreprocessor import DataPreprocessor
from CurePulse.Clustering.agglomerative import Agglomerative
from CurePulse.DataExporter.CSVExporter import CSVExporter
warnings.simplefilter(action='ignore', category=FutureWarning)

# @shared_task
# def update_database():
# 	for i in range(10,11):
# 		try:
# 			date = str(Date(2023, 10, i))
# 			controller = Controller()
# 			print(date)
# 			controller.execute(date)
# 		except Exception as e:
# 			traceback.print_exc()
# 			print(f'Task: {e}')

@shared_task
def update_database_weekly():
	numdays = 7
	loader = MongoDBLoader()
	data = []
	for i in range(10,18):
		try:
			data += loader.get_data(str(Date(2023, 10, i)))
		except Exception as e:
			print(f'Task: {e}')
	print(len(data))
	processor = DataPreprocessor(data)
	scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores', 'Agent_Accent_Score', 'Agent_Langauge_Score_Percentage']
	controller = Controller()
	df = controller.fit_transform(Agglomerative(), processor, scores, "10-17 October")
	exporter = CSVExporter()
	exporter.export_results(df)

update_database_weekly()