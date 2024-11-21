import json
import os
import unittest

from apps.library.controllers import BookController
from config import settings


class TestBookControler(unittest.TestCase):
    def setUp(self) -> None:
        self.rollback_setting = False
        self.initial_data = {
            1: {"id": 1, "title": "The Godfather", "author": "Mario Puzo", "year": 1965, "status": "in_stock"},
            2: {"id": 2, "title": "Mamasita", "author": "Pons", "year": 2021, "status": "issued"},
        }

        with open(settings.TEST_DB_PATH, "w", encoding="utf-8") as test_db:
            json.dump(self.initial_data, test_db, indent=4, ensure_ascii=False)

        self.controller = BookController(dbpath=settings.TEST_DB_PATH)
        self.dataset = self.controller.get_all()
        self.last_key = list(self.dataset.keys())[-1]
        
        self.addon_data = {
            "title": "Test Book 1", "author": "Test Author 1", "year": 2024
            }
        
        self.wrong_type_data = {
            "title": 1, "author": "Test Author 1", "year": 2024
        }

        self.wrong_date_data = {
            "title": "Test Title 1", "author": "Test Author 1", "year": 0
        }
          
    def tearDown(self) -> None:
        if os.path.exists(self.controller.dbpath) and self.rollback_setting:
            os.remove(self.controller.dbpath)

    def test_get_all(self):
        self.assertEqual(self.dataset, self.initial_data)

    def test_create(self):
        self.controller.create(**self.addon_data)
        
        updated_dataset = self.controller.get_all()
        new_key = list(self.dataset.keys())[-1]

        self.assertNotEqual(self.last_key, new_key)
        self.assertEqual(self.last_key + 1, new_key)
        
        data = updated_dataset[new_key]

        self.assertEqual(data["status"], "in_stock")
        self.assertEqual(data["title"], self.addon_data["title"])
        self.assertEqual(data["author"], self.addon_data["author"])
        self.assertEqual(data["year"], self.addon_data["year"])

        self.assertRaises(TypeError, self.controller.create, **self.wrong_type_data)
        
        with self.assertLogs("streamLogger", level="WARNING") as log:
            self.controller.create(**self.wrong_date_data)
            self.assertIn("Incorrect 'year' format.", log.output[0])

    def test_delete(self):
        self.controller.delete(self.last_key)
        
        updated_dataset = self.controller.get_all()
        current_key = list(updated_dataset.keys())[-1]
        
        self.assertNotEqual(self.last_key, current_key)
        with self.assertLogs("streamLogger", level="WARNING") as log:
            self.controller.delete(self.last_key)
            self.assertIn("Provided id does not exist", log.output[0])
    
    def test_change_status(self):
        self.controller.change_status(self.last_key, status="in_stock")
        updated_data = self.controller.get_all()

        self.assertEqual(updated_data[self.last_key]["status"], "in_stock" )
    
    def test_search(self):
        result = self.controller.search()

        self.assertEqual(result, None)

        result = self.controller.search(**self.addon_data)
        self.assertEqual(result, [])

        self.controller.create(**self.addon_data)
        result = self.controller.search(**self.addon_data)[0]
        result.pop("id")
        result.pop("status")
        self.assertEqual(result, self.addon_data)
