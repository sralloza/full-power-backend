from typing import Optional

from pydantic import BaseModel, validator


class FileBase(BaseModel):
    name: str

    @validator("name")
    def validate_id(cls, value, field):
        if value.count(".") == 0:
            raise ValueError("Must contain at least one dot")

        primary, secondary = value.split(".", 1)
        if primary not in ["health", "vitamins"]:
            raise ValueError(
                f"Primary key must be 'health' or 'vitamins', not {primary!r}"
            )

        if primary == "vitamins" and secondary.count(".") != 0:
            raise ValueError("Vitamin's secondary key can't contain dots")

        if primary == "health":
            if secondary.count(".") != 1:
                raise ValueError("Health's secondary key must contain excactly one dot")

            _, health_type = secondary.split(".")
            if health_type not in ["act", "understand"]:
                raise ValueError(
                    f"Health type must be 'act' or 'understand', not {health_type!r}"
                )

        return value


class FileCreate(FileBase):
    content: str
    title: str


class FileCreateInner(FileCreate):
    id: str
    lang: str


class FileCreateResult(FileBase):
    name: str
    title: str
    lang: str

    class Config:
        orm_mode = True


class FileUpdate(FileBase):
    name: Optional[str]
    content: Optional[str]
    title: Optional[str]
    lang: Optional[str]


class FileUpdateInner(FileUpdate):
    id: Optional[str]


class FileInDB(FileBase):
    content: str
    lang: str
    title: str
    id: str

    class Config:
        orm_mode = True


class FileResult(FileCreateResult):
    content: str


class FileDelete(FileBase):
    lang: str
