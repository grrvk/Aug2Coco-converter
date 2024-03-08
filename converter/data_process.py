import zipfile
from zipfile import ZipFile
import pandas as pd
import numpy as np
import json
import os


def _findJsonZip(path):
    """
    :param path: path to zip
    :return: json file name found in zip
    """
    with zipfile.ZipFile(path, "r") as zip_ref:
        json_files = [pos_json for pos_json in zip_ref.namelist() if (pos_json.endswith('.json') and
                                                                      (not pos_json.startswith('__MACOSX')))]
        if len(json_files) != 1:
            raise Exception(f"More than one JSON file to load from {path}")
        return json_files[0]


def _findJsonFolder(path):
    """
    :param path: path to folder
    :return: json file names found in folder
    """
    return [file for file in os.listdir(path) if file.endswith(".json") and not file.startswith('__MACOSX')]


def _getDf(dr):
    """
    :param dr: path to zip
    :return: dataframe of json file data
    """
    json_files = _findJsonZip(dr)
    with ZipFile(dr) as zipFile:
        with zipFile.open(json_files) as file:
            df = pd.read_json(file)
    return df


def _dfSplit(df, rate, starting_idx, last_batch=False):
    """
    :param df: dataframe from json
    :param rate: split rate set for split type
    :param starting_idx: image array index to start splitting from
    :param last_batch: is filling last folder
    :return: split dataframe, new starting_idx for nex split
    """
    image_names = np.array(list(set(df['image'].tolist())))

    if not last_batch:
        type_images = image_names[starting_idx:starting_idx+int(rate * image_names.size)]
        last_idx = starting_idx+int(rate * image_names.size)
    else:
        type_images = image_names[starting_idx:]
        last_idx = image_names.size

    type_df = df[df["image"].isin(type_images)]

    return type_df.reset_index(), last_idx


def _writeJson(dataset_path, split_type, data, load_type):
    """
    :param dataset_path: path to where write json
    :param split_type: train/val/test annotation
    :param data: data to dump
    :param load_type: creating new dataset or loading to existing
    :return: -
    """
    path = os.path.join(os.path.join(dataset_path, 'annotations'), split_type)
    if load_type:
        with open(path+"_labels.json", mode='r+', encoding='utf-8') as outfile:
            previous_data = json.load(outfile)
            previous_data['categories'].extend(data['categories'])
            previous_data['images'].extend(data['images'])
            previous_data['annotations'].extend(data['annotations'])
            outfile.close()
            data = previous_data
    with open(path+"_labels.json", "w") as outfile:
        json.dump(data, outfile, indent=4, default=str)
        outfile.close()


def load_check_json(path, split_type, upload, df, holder):
    """
    :param path: path from where load annotations json if exists
    :param split_type: train/val/test annotations type
    :param upload: uploading or creating new dataset
    :param df: dataframe of new data
    :param holder: constant dataset information holder
    :return: filtered dataframe, updated holder
    """
    json_path = os.path.join(os.path.join(path, 'annotations'), split_type)
    if upload and os.path.exists(f"{json_path}_labels.json"):
        with open(f"{json_path}_labels.json", "r") as json_file:
            json_data = json.load(json_file)
            images_json = list(image['file_name'] for image in json_data['images'])
            annotations_json = list(ann for ann in json_data['annotations'])

        df = df[~df["image"].isin(images_json)]

        holder.set_changes(imI=len(images_json), anI=len(annotations_json))
        return df, holder
    holder.set_changes()
    return df, holder

