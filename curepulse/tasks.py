import traceback 

from datetime import date as Date, timedelta
from celery import shared_task
from CurePulse.controller import Controller
import warnings
from CurePulse.DataLoader.MongoDBLoader import MongoDbDailyDataLoader, MongoDbWeeklyDataLoader
from CurePulse.Preprocessor.DataPreprocessor import DataPreprocessor
from CurePulse.Clustering.agglomerative import Agglomerative
from CurePulse.DataExporter.CSVExporter import CSVExporter
warnings.simplefilter(action='ignore', category=FutureWarning)
import numpy as np 

@shared_task
def update_database():
	for i in range(10,11):
		try:
			date = str(Date(2023, 10, i))
			controller = Controller()
			controller.execute(date)
		except Exception as e:
			traceback.print_exc()
			print(f'Task: {e}')

@shared_task
def update_database_weekly():
	loader = MongoDbWeeklyDataLoader()
	data = loader.get_data(Date(2023, 10, 10))
	processor = DataPreprocessor(data)
	list_scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores']
	individial_scores = ['Agent_Accent_Score', 'Agent_Langauge_Score_Percentage']
	aggregated_scores = [f'{score}_Agg' for score in list_scores]
	transformations = [aggregate for _ in list_scores]
	processor.process_data(list_scores, aggregated_scores, transformations)
	controller = Controller()
	df = controller.fit_transform_x('agglomerative', processor, aggregated_scores + individial_scores, "10-17 October")
	exporter = CSVExporter()
	exporter.export_results(df) 

def aggregate(df):
	if isinstance(df, dict):
		df = list(df.values())
	df = np.sum(np.array(df) * np.array([1, 2, 4]))
	return df

# @shared_task
# def update_database_weekly():
# 	loader = MongoDbWeeklyDataLoader()
# 	data = loader.get_data(2023, 10, 10)
# 	processor = DataPreprocessor(data)
# 	scores = ['Client_Tone_Scores', 'Client_Text_Scores', 'Agent_Tone_Scores', 'Agent_Text_Scores', 'Agent_Accent_Score', 'Agent_Language_Scores']
# 	controller = Controller()
# 	df = controller.fit_transform(Agglomerative(), processor, scores, "10-17 October")
# 	exporter = CSVExporter()
# 	exporter.export_results(df) 

update_database_weekly()