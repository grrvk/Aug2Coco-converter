from config import settings
from utils import _mkdir, _getDf, _fillJson, _writeJson
import json


images_dataset_dir = f"{settings.DATASET_NAME}/images"
annotations_dataset_dir = f"{settings.DATASET_NAME}/annotations"
categories = json.loads(settings.CATEGORIES)

_mkdir(settings.DATASET_NAME)
_mkdir(images_dataset_dir)
_mkdir(annotations_dataset_dir)

WORKING_DIR = settings.WORKING_DIR

df_total = _getDf(WORKING_DIR)

data = _fillJson(WORKING_DIR, categories, df_total)
_writeJson(annotations_dataset_dir, data, "total")

print("total_labels.json generated successfully!")
