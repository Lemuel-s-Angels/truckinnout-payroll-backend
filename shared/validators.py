import os

from django.core.exceptions import ValidationError
from django.utils import timezone
from PIL import Image


def validate_image(value):
    try:
        # Open the image using Pillow
        with Image.open(value) as img:
            image_type = img.format.lower()  # e.g., 'jpeg', 'png'

            # Pillow uses 'jpeg' for both .jpg and .jpeg
            valid_image_types = ["jpeg", "png", "gif", "bmp", "webp"]

            if image_type not in valid_image_types:
                raise ValidationError(
                    "Unsupported image format. Allowed types are: JPG, JPEG, PNG, GIF, BMP, and WebP."
                )

            # Check file extension matches content type
            ext = os.path.splitext(value.name)[1][1:].lower()

            if image_type == "jpeg":
                if ext not in ["jpg", "jpeg"]:
                    raise ValidationError(
                        "File extension mismatch. Expected .jpg or .jpeg"
                    )
            elif image_type != ext:
                raise ValidationError(
                    f"File extension mismatch. Expected .{image_type}"
                )

    except Exception:
        raise ValidationError("Invalid image file or corrupted data.")


def validate_date(value):
    if value < timezone.now().date():
        raise ValidationError("Date cannot be in the past")
