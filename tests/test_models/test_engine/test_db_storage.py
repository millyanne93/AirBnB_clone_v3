#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from unittest.mock import patch
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Setup db and initialize sorage"""
        cls.storage = db_storage.DBStorage()

    @patch('models.engine.db_storage.DBStorage.reload')
    def test_reload(self, mock_reload):
        """Test reload method"""
        self.storage.reload()
        mock_reload.assert_called_once()

    @classmethod
    def tearDownClass(cls):
        """Remove session instances"""
        del cls.storage

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_existing_object(self):
        """Test get existing object"""
        new_user = User(email='example@example.com',
                        password='password',
                        first_name='John',
                        last_name='Doe')
        new_user.save()
        obj_id = new_user.id
        get_user = self.storage.get(User, obj_id)
        self.assertEqual(get_user.id, obj_id)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_non_existing_object(self):
        """Test get non existing object"""
        get_user = self.storage.get(User, "Fake id")
        self.assertIsNone(get_user.id, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_all_objects(self):
        """Test counting all objects"""
        old_count = self.storage.count()
        new_user = User(email='example2@example.com',
                        password='password2',
                        first_name='Jonnie',
                        last_name='Max')
        new_user.save()
        new_count = self.storage.count()
        self.assertEqual(old_count, new_count + 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_objects_of_user_class(self):
        """Test count objects of a class"""
        old_count = self.storage.count(User)
        new_user = User(email='example3@example.com',
                        password='password3',
                        first_name='Alex',
                        last_name='Jones')
        new_user.save()
        new_count = self.storage.count(User)
        self.assertEqual(old_count, new_count + 1)
