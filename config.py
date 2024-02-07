import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATASET_NAME = str(os.getenv('DATASET_NAME'))
    CATEGORIES = os.getenv('CATEGORIES')
    WORKING_DIR = str(os.getenv('WORKING_DIR'))


settings = Settings()

