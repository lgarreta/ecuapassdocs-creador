#!/usr/bin/env python

import os, json, sys

import django
from django.apps import apps

from init_django import *

#--------------------------------------------------------------------
#--------------------------------------------------------------------
def show_data():
	data = {}
	#for model in apps.get_models():
	for model in apps.get_app_config ("appdocs").get_models():
		model_name = model._meta.model_name
		print (f"-- Model name: {model_name}")

#--------------------------------------------------------------------
# Main
#--------------------------------------------------------------------
init_django_settings ()
show_data()

