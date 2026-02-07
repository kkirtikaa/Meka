import cloudinary
import cloudinary.uploader
import cloudinary.api
from config import Config

# -----------------------------------
# Cloudinary configuration
# -----------------------------------
cloudinary.config(
    cloud_name=Config.CLOUD_NAME,
    api_key=Config.CLOUD_API_KEY,
    api_secret=Config.CLOUD_API_SECRET,
    secure=True
)

# -----------------------------------
# Upload image to Cloudinary
# -----------------------------------
def upload_image(image_file):
    """
    image_file: FileStorage object from Flask (request.files['image'])
    returns: secure image URL
    """

    try:
        result = cloudinary.uploader.upload(
            image_file,
            folder="meka_uploads",   # Cloudinary folder name
            resource_type="image"
        )

        return result["secure_url"]

    except Exception as e:
        print("Cloudinary upload error:", e)
        return None