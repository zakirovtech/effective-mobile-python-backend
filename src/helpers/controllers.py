import json
import os
import logging
import typing 

from config import settings


class BaseController:
    def __init__(self, dbpath=settings.DB_PATH) -> None:
        self.logger = logging.getLogger("streamLogger")
        self.dbpath = dbpath
        self._queryset = self.preload_db()

    def preload_db(self) -> typing.Dict:
        """Load the database from a JSON file and create a dictionary by id."""
        if not os.path.exists(self.dbpath):
            self.logger.info("Database is initialized successfully")
            return {}
        try:
            with open(self.dbpath, "r", encoding="utf-8") as db_json:
                books = json.load(db_json)
                self.logger.info("Database is loaded successfully")
                return {int(book): books[book] for book in books}
        except Exception as e:
            self.logger.error(f"Failed load database: {e}")
        else:
            self.logger.info("Database loaded successfully.")


    def _update_db(self) -> None:
        """Update the database file."""
        try:
            with open(self.dbpath, "w", encoding="utf-8") as db:
                json.dump(self._queryset, db, indent=4, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Failed to update database: {e}")
        else:
            self.logger.info("Database updated successfully.")


class OpsMixin:
    def create(self, *args, **kwargs):
        pass

    def bulk_create(self, *args, **kwargs):
        pass
        
    def delete(self, *args, **kwargs):
        pass
    
    def get_all(self, *args, **kwargs):
        pass
    
    def change_status(self, *args, **kwargs):
        pass

    def search(self, *args, **kwargs):
        pass
