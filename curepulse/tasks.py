from datetime import date as Date
from celery import shared_task
from CurePulse.controller import Controller

@shared_task
def update_database():
	for i in range(8, 25):
		try:
			date = str(Date(2023, 9, i))
			controller = Controller()
			controller.execute(date)
		except Exception as e:
			print(e)
			pass 

update_database()