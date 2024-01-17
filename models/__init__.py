#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage


storage_type = os.environ.get('HBNB_TYPE_STORAGE', 'file')

if storage_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

"""Always reload after instantiation"""
storage.reload()
