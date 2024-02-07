import os, zipfile, json
from zipfile import ZipFile
import pandas as pd
from PIL import Image
from schemes import InfoClass, CategoryClass, ImageClass, AnnotationClass, JsonFileClass
from exceptions import JsonAmountException, CategoryTypeException, ItemMissingException


def _mkdir(path):
    if os.path.exists(path) is False:
        os.mkdir(path)
    else:
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                os.remove(os.path.join(path, filename))


def _findjson(path):
    with zipfile.ZipFile(path, "r") as zip_ref:
        json_files = [pos_json for pos_json in zip_ref.namelist() if (pos_json.endswith('.json') and
                                                                      (not pos_json.startswith('__MACOSX')))]
        if len(json_files) != 1:
            raise JsonAmountException
        return json_files[0]


def _findImages(path):
    with zipfile.ZipFile(path, "r") as zip_ref:
        image_files = [image_pos for image_pos in zip_ref.namelist() if
                       ((image_pos.endswith('.jpg') or image_pos.endswith('.png')
                        or image_pos.endswith('.jpeg')) and (not image_pos.startswith('__MACOSX')))]
        return image_files


def _getDf(dr):
    json_files = _findjson(dr)
    with ZipFile(dr) as zipFile:
        with zipFile.open(json_files) as file:
            df = pd.read_json(file)
    df = df.assign(x2=lambda x: x['x2'] - x['x1'],
              y2=lambda x: x['y1'] - x['y2'])
    df = df.rename(columns={"x2": "width", "y2": "height"})
    return df


def _setInfo():
    return InfoClass().__dict__


def _setCategories(cats):
    categories = []
    for i, cat in enumerate(cats):
        if type(cat) is tuple:
            sup = next((item for item in categories if item["name"] == cat[0]), None)
            category = CategoryClass(cat[1], i + 1, sup.get("id"))
        elif type(cat) is str:
            category = CategoryClass(cat, i + 1, None)
        else:
            raise CategoryTypeException
        categories.append(category.__dict__)
    return categories


def _setImages(dr):
    images = []
    images_paths = _findImages(dr)
    with ZipFile(dr) as zipFile:
        for i, image_path in enumerate(images_paths):
            with zipFile.open(image_path) as file:
                img = Image.open(file)
                image = ImageClass(i+1, img.width, img.height, image_path.split("/")[-1])
                images.append(image.__dict__)
    return images


def findCategoryId(array, item_name):
    item = next((item for item in array if item.get("name") == item_name), None)
    if not item:
        raise ItemMissingException
    return item.get("id")


def findImageId(array, item_name):
    item = next((item for item in array if item.get("file_name") == item_name), None)
    if not item:
        raise ItemMissingException
    return item.get("id")


def _setAnnotations(df, categories, images):
    annotations = []
    for index, row in df.iterrows():
        image_id = findImageId(images, row['image'])
        category_id = findCategoryId(categories, row['category'])
        segmentation = bbox = [row['x1'], row['y1'], row['width'], row['height']]
        annotation = AnnotationClass(
            index+1, image_id, category_id, segmentation, row['width']*row['height'],
            bbox, 0
        )
        annotations.append(annotation.__dict__)
    return annotations


def _fillJson(path, cats, df):
    info = _setInfo()
    categories = _setCategories(cats)
    images = _setImages(path)
    annotations = _setAnnotations(df, categories, images)

    data = JsonFileClass(info, categories, images, annotations)

    return data.__dict__


def _writeJson(path, data, filename):
    with open(f"{path}/{filename}_labels.json", "w") as outfile:
        json.dump(data, outfile, indent=4, default=str)




