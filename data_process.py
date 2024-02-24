import zipfile
from zipfile import ZipFile
import pandas as pd
from exceptions import JsonAmountException
import numpy as np


def _findjson(path):
    with zipfile.ZipFile(path, "r") as zip_ref:
        json_files = [pos_json for pos_json in zip_ref.namelist() if (pos_json.endswith('.json') and
                                                                      (not pos_json.startswith('__MACOSX')))]
        if len(json_files) != 1:
            raise JsonAmountException
        return json_files[0]


def _getDf(dr):
    json_files = _findjson(dr)
    with ZipFile(dr) as zipFile:
        with zipFile.open(json_files) as file:
            df = pd.read_json(file)
    return df


def _dfSplit(df, split):
    image_names = np.array(list(set(df['image'].tolist())))
    train_images, val_images = np.split(image_names,
                                        [int(split*image_names.size)])
    train_df = df[df["image"].isin(train_images)]
    val_df = df[df["image"].isin(val_images)]
    return train_df.reset_index(), val_df.reset_index()
