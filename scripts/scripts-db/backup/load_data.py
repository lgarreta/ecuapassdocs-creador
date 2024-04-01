#!/usr/bin/env python

import json
from django.apps import apps
from init_django import *

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        for model_name, model_data in data.items():
            model = apps.get_model(app_label='appdocs', model_name=model_name)
            model.objects.bulk_create(model(**entry) for entry in model_data)

#--------------------------------------------------------------------
# Main
#--------------------------------------------------------------------
init_django ()
load_data ('backup.json')
