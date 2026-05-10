import os

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


class Config:

    SECRET_KEY = "secwebmailsecretkey"

    # Dossiers
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        'uploads'
    )

    CONVERSION_FOLDER = os.path.join(
        BASE_DIR,
        'conversions'
    )

    # Taille max upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Extensions autorisées
    ALLOWED_EXTENSIONS = {
        'pem',
        'der'
    }