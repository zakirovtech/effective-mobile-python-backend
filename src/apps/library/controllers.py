from dataclasses import asdict
import typing

from apps.library.models import Book
from helpers.controllers import BaseController, OpsMixin
from helpers.utils import strict, validate_id


class BookController(OpsMixin, BaseController):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    @strict
    def create(self, title: str, author: str, year: int) -> typing.Union[typing.Dict, None]:
        """Create one book in database"""
        try:
            id = max(self._queryset.keys(), default=0) + 1
            book = Book(id, title, author, year)
        except ValueError as  e:
            self.logger.warning(f"Failed create a book instance with error: [{e}]")
            return None
        else:
            book_map = asdict(book)
            self._queryset[book_map["id"]] = book_map
            self._update_db()
            return book_map
    
    @strict
    def delete(self, id: int) -> int:
        """Delete a book instance"""
        try:
            validate_id(id, self._queryset)
        except (TypeError, IndexError) as e:
            self.logger.warning(f"Failed delete a book with error: [{e}]")
            return -1
        else:
            del self._queryset[id]
            self._update_db()
            self.logger.info(f"Book with id: [{id}] is deleted successfully")
            return 0
    
    def get_all(self) -> typing.Dict:
        """Return all book instances"""
        return self._queryset
    
    def change_status(self, id: int, status: typing.Literal["in_stock", "issued"]) -> bool:
        """Change a book instance`s status"""
        book = self._queryset.get(id)
        
        if book:
            book["status"] = status
            self._update_db()
            self.logger.info(f"Book with id: [{id}] changed status to: [{status}]")
            return True
        else:
            self.logger.info(f"Book with id {id} not found.")
            return False

    def search(self, **kwargs) -> typing.Union[typing.List, None]:
        """Search a book instance by title, author or year"""
        if not kwargs:
            self.logger.warning("Provide at least one argument.")
            return None

        books = []

        for _, book in self._queryset.items():
            if all(book.get(key) == value for key, value in kwargs.items()):
                self.logger.info(f"Found a book by filter: {list(kwargs.values())} => {book}")
                books.append(book)

        if not books:
            self.logger.info(f"Cannot find any book by the provided filter: {list(kwargs.values())}")

        return books
    