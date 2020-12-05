from pathlib import Path

import pytest
from fastapi import HTTPException

from app.core.images import process_image_content
from app.schemas.image import ImageCreateInner

images_paths = sorted(
    Path(__file__).parent.with_name("test_data").joinpath("images").iterdir(),
    key=lambda x: x.name,
)
validators = {".ico": "type", ".png": True, ".jpeg": True, ".webp": "mime"}


@pytest.mark.parametrize("image_path", images_paths[:-1])
def test_process_image_content(image_path):
    image_content = image_path.read_bytes()
    is_valid = validators[image_path.suffix]

    if is_valid is not True:
        with pytest.raises(HTTPException) as exc:
            process_image_content(image_content)

        assert exc.value.status_code == 400
        if is_valid == "type":
            assert exc.value.detail == "Image type could not be identified"
        else:  # Mimetype error
            det = "Image mimetype could not be identified [%r]" % image_path.suffix[1:]
            assert exc.value.detail == det

        return

    image = process_image_content(image_content)
    assert isinstance(image, ImageCreateInner)
    assert image_path.suffix.replace(".", "") in image.image_type
    assert image_path.suffix.replace(".", "") in image.mime_type
    assert image.content == image_content


def test_process_image_content_too_large():
    image_path = images_paths[-1]
    image_content = image_path.read_bytes()

    with pytest.raises(HTTPException) as exc:
        process_image_content(image_content)
    assert exc.value.status_code == 413
