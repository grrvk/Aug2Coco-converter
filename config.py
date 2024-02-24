import os
import shutil


# check is split rate [0,1], does path exist


def _mkdir(name):
    """
        :param name: path to directory to clear and create
        :return: None
    """

    if os.path.exists(name) is False:
        try:
            os.mkdir(name)
        except Exception as e:
            print('Failed to create directory %s. Reason: %s' % e)
    else:
        for filename in os.listdir(name):
            file_path = os.path.join(name, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


class Settings:
    """
        Settings class with directories and split rate
    """

    WORKING_DIR: str
    DATASET_DIR: str
    ANNOTATIONS_DIR: str
    TRAIN_DIR: str
    VAL_DIR: str
    SPLIT_RATE: float

    def create_directories(self, dataset_name: str, annotations_dir: str,
                           train_dir: str, split_rate: float | None):
        _mkdir(dataset_name)
        _mkdir(annotations_dir)
        _mkdir(train_dir)

        if split_rate:
            self.VAL_DIR = f"{self.DATASET_DIR}/val"
            _mkdir(self.VAL_DIR)

    def __init__(self, **kwargs):
        self.WORKING_DIR = kwargs.get('working_dir')

        dataset_name = f"{(self.WORKING_DIR.split('/')[-1]).split('.')[0]}_CocoFormat"
        self.DATASET_DIR = f"{kwargs.get('return_path')}/{dataset_name}" if kwargs.get('return_path') is not None \
            else dataset_name

        self.ANNOTATIONS_DIR: str = f"{self.DATASET_DIR}/annotations"
        self.TRAIN_DIR: str = f"{self.DATASET_DIR}/train"
        self.SPLIT_RATE = kwargs.get('split_rate')

        self.create_directories(self.DATASET_DIR, self.ANNOTATIONS_DIR, self.TRAIN_DIR, self.SPLIT_RATE)
