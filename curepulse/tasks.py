"""_summary_: 
This file contains the celery task that updates the database with the latest data from the CurePulse API.
"""

from datetime import date as Date
from celery import shared_task
from CurePulse.controller import Controller
import traceback

@shared_task
def update_database():
	"""_summary_
 	This function is used to update the database with the latest data from the CurePulse API.
	"""
	try:
		date = str(Date(2023,9,14))
		controller = Controller()
		controller.execute(date)
	except Exception:
		traceback.print_exc()
  
update_database()