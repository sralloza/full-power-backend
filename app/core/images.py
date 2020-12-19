import imghdr
import mimetypes

from fastapi import HTTPException, status
from pydantic import ValidationError

from app.schemas.image import ImageCreateInner


def process_image_content(image_content: bytes) -> ImageCreateInner:
    image_type = imghdr.what(None, h=image_content)
    if image_type is None:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Image type could not be identified"
        )

    mime_type = mimetypes.guess_type("dummy." + image_type, strict=False)[0]
    if mime_type is None:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Image mimetype could not be identified [%r]" % image_type,
        )

    try:
        image = ImageCreateInner(
            content=image_content, image_type=image_type, mime_type=mime_type
        )
    except ValidationError as exc:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=exc.errors()
        )
    return image
