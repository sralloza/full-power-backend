import imghdr
import mimetypes

from fastapi import HTTPException
from pydantic import ValidationError

from app.schemas.image import ImageCreateInner


def process_image_content(image_content: bytes) -> ImageCreateInner:
    image_type = imghdr.what(None, h=image_content)
    if image_type is None:
        raise HTTPException(400, "Image type could not be identified")

    mime_type = mimetypes.guess_type("dummy." + image_type, strict=False)[0]
    if mime_type is None:
        raise HTTPException(
            400, "Image mimetype could not be identified [%r]" % image_type
        )

    try:
        image = ImageCreateInner(
            content=image_content, image_type=image_type, mime_type=mime_type
        )
    except ValidationError as exc:
        raise HTTPException(413, detail=exc.errors())
    return image
