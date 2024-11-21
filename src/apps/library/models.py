from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    status: str = field(init=False)

    # _id_counter: ClassVar[int] = 0

    def __post_init__(self) -> None:
        self.validate_fields()
        # self.increment_counter()
        self.status = "in_stock"
    
    # @classmethod
    # def increment_counter(cls) -> None:
    #     cls._id_counter += 1

    def validate_fields(self) -> None:
        if not self.author.strip():
            raise ValueError("Field 'author' can not be empty.")
        
        if not self.title.strip():
            raise ValueError("Field 'title' can not be empty.")
        
        if len(str(self.year)) != 4:
            raise ValueError("Incorrect 'year' format.")
