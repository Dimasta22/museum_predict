import pathlib
from dotenv import dotenv_values


BASE_DIR = pathlib.Path(__file__).parent.parent
config = dotenv_values(".env")


class Config:
    UPLOAD_FOLDER = str(BASE_DIR / 'src' / 'static' / 'uploads')
    SECRET_KEY = config['SECRET_KEY']
