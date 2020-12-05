from pydantic import BaseModel, conbytes


class ImageBase(BaseModel):
    content: conbytes(max_length=1024 ** 2 * 2)


class ImageCreate(ImageBase):
    pass


class ImageCreateInner(ImageBase):
    image_type: str
    mime_type: str


class ImageCreateResult(BaseModel):
    id: int
    image_type: str
    mime_type: str

    class Config:
        orm_mode = True


class ImageUpdate(ImageCreate):
    content: conbytes(max_length=1024 ** 2 * 2) = None  # type: ignore
    image_type: str = None  # type: ignore
    mime_type: str = None  # type: ignore


class ImageInDB(ImageBase):
    id: int
    image_type: str
    mime_type: str

    class Config:
        orm_mode = True
