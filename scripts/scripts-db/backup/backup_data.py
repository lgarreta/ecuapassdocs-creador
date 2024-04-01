#!/usr/bin/env python

# backup_data.py

import json, datetime

from django.apps import apps
from init_django import *

class CustomJSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.date):
			return obj.isoformat()
		return super().default(obj)

def backup_data(file_path):
	data = {}
	for model in apps.get_app_config ("appdocs").get_models():
		model_name = model._meta.model_name
		print ("-- Backup for model:", model_name)
		data[model_name] = list(model.objects.all().values())
	
	with open(file_path, 'w') as file:
		json.dump(data, file , cls = CustomJSONEncoder)

init_django ()
backup_data('backup.json')

