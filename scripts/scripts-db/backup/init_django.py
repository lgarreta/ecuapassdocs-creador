#!/usr/bin/env python

"""
Init djando ecupassdocs environment for working with 
current DB
"""
import os, sys
import django

def init_django_settings ():
	APP_PATH = "/home/lg/BIO/iaprojects/ecuapassdocs/ecuapassdocs-creador"
	sys.path.append (APP_PATH)
	os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "appdocs_main.settings")
	sys.path.append (f"{os.getcwd()}")
	django.setup ()

