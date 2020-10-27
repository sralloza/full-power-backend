from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def dict(self):
        """Returns the attributes of self as a dict, like pydantic.Model."""

        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
