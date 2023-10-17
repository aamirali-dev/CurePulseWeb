"""_summary_: 
This file contains the celery task that updates the database with the latest data from the CurePulse API.
"""

from datetime import date as Date
from celery import shared_task
from CurePulse.controller import Controller

@shared_task
def update_database():
	"""_summary_
 	This function is used to update the database with the latest data from the CurePulse API.
	"""
	today_date = Date.today()
	try:
		date = str(today_date)
		controller = Controller()
		controller.execute(date)
	except Exception as e:
		print(e)
		pass 

update_database()