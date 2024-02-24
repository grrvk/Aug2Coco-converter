import json
from zipfile import ZipFile
from PIL import Image
from schemes import InfoClass, CategoryClass, ImageClass, AnnotationClass, JsonFileClass
from exceptions import CategoryTypeException, ItemMissingException


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


def _setImages(settings, image_paths, is_train):
    images = []
    with ZipFile(settings.WORKING_DIR) as zipFile:
        for i, image_path in enumerate(image_paths):
            with zipFile.open(f"{(settings.WORKING_DIR.split('/')[-1]).split('.')[0]}/{image_path}") as file:
                img = Image.open(file)
                if is_train:
                    img.save(f"{settings.TRAIN_DIR}/{image_path}")
                else:
                    img.save(f"{settings.VAL_DIR}/{image_path}")
                image = ImageClass(i+1, img.width, img.height, image_path.split("/")[-1])
                images.append(image.__dict__)
    return images


def findObjectId(array, item_name, sorter):
    item = next((item for item in array if item.get(sorter) == item_name), None)
    if not item:
        raise ItemMissingException
    return item.get("id")


def _setAnnotations(df, categories, images):
    annotations = []
    for index, row in df.iterrows():
        image_id = findObjectId(images, row['image'], "file_name")
        category_id = findObjectId(categories, row['category'], "name")
        segmentation = row['segmentation']
        area = row['area']
        bbox = row['bbox']
        annotation = AnnotationClass(
            index+1, image_id, category_id, segmentation, area,
            bbox, 0
        )
        annotations.append(annotation.__dict__)
    return annotations


def _fillJson(settings, df, is_train=True):
    info = _setInfo()
    categories = _setCategories(list(set(df['category'].tolist())))
    images = _setImages(settings, list(set(df['image'].tolist())), is_train)
    annotations = _setAnnotations(df, categories, images)

    data = JsonFileClass(info, categories, images, annotations)

    return data.__dict__


def _writeJson(path, data, filename):
    with open(f"{path}/{filename}_labels.json", "w") as outfile:
        json.dump(data, outfile, indent=4, default=str)







