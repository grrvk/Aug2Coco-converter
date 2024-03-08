import os
import shutil


def _mkdir(name):
    """
        :param name: path to directory to clear and create
        :return: None
    """

    if os.path.exists(name) is False:
        try:
            os.mkdir(name)
        except Exception as e:
            print('Failed to create directory. Reason: %s' % e)
    else:
        for filename in os.listdir(name):
            file_path = os.path.join(name, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to create directory. Reason: %s' % e)


class Settings:
    """
        Settings class with directories and split rate
    """

    WORKING_DIR: str
    DATASET_DIR: str

    SPLIT_TYPES: list = []
    SPLIT_RATE: dict = {"train": 0, "val": 0, "test": 0}
    UPLOAD: bool = False

    def __init__(self, **kwargs):
        self.UPLOAD = True if kwargs.get("upload") else False
        self.splitParams(kwargs.get('split_type'), kwargs.get('split_rate'))

        working_dir_path = kwargs.get('working_dir')
        if (working_dir_path is None or not os.path.exists(working_dir_path)
                or os.path.splitext(os.path.basename(working_dir_path))[1] != '.zip'):
            raise Exception('Path to data to convert is invalid')
        self.WORKING_DIR = working_dir_path

        return_dir_path = kwargs.get('return_path')
        if self.UPLOAD:
            self.load(return_path=return_dir_path)
        else:
            self.create(return_path=return_dir_path)

    def __repr__(self):
        return (f"Config: workig_dir = {self.WORKING_DIR}, \n"
                f"dataset_dir = {self.DATASET_DIR}, \n"
                f"split_folders = {self.SPLIT_TYPES}, \n"
                f"split_rate = {self.SPLIT_RATE}, \n"
                f"is_uploading = {self.UPLOAD} \n")

    def create_directories(self, dataset_folder: str, dir_names: list):
        if not self.UPLOAD:
            _mkdir(dataset_folder)
        if not os.path.exists(os.path.join(dataset_folder, 'annotations')):
            _mkdir(os.path.join(dataset_folder, 'annotations'))
        for split_type in dir_names:
            _mkdir(os.path.join(dataset_folder, split_type))

    def load(self, return_path: str | None):
        print('Uploading dataset')
        if return_path is None or not os.path.exists(return_path):
            raise Exception('Path to folder of dataset to load into is invalid')
        self.DATASET_DIR = return_path
        dir_list = os.listdir(self.DATASET_DIR)
        dirs_to_create = [n for n in self.SPLIT_TYPES if not (n in dir_list)]
        self.create_directories(self.DATASET_DIR, dirs_to_create)

    def create(self, return_path: str | None):
        print('Creating dataset')
        dataset_name = f"{os.path.splitext(os.path.basename(self.WORKING_DIR))[0]}_CocoFormat"
        self.DATASET_DIR = os.path.join(return_path, dataset_name) if return_path is not None and os.path.exists(
            return_path) \
            else os.path.join(os.path.dirname(self.WORKING_DIR), dataset_name)

        self.create_directories(self.DATASET_DIR, self.SPLIT_TYPES)

    def splitParams(self, types, rates):
        split_types = [t for t in types.split('/')]
        split_rates = [t for t in rates.split('/')]

        if len(split_types) != len(split_rates):
            raise Exception('Every split type (train, val, etc) must have split rate (0.1, 0.3, etc)')

        for i, split_type in enumerate(split_types):
            if split_type in list(self.SPLIT_RATE.keys()):
                try:
                    rate = float(split_rates[i])

                    if rate < 0 or rate > 1:
                        raise Exception(f'Split rate {rate} for {split_type} is not value from 0 to 1')
                    self.SPLIT_RATE[f'{split_type}'] = rate
                except:
                    raise Exception(f'Tried to pass to {split_type} split not float or integer value {split_rates[i]}')

        if sum(self.SPLIT_RATE.values()) != 1:
            raise Exception('Summ of split rates must be 1')

        self.SPLIT_TYPES = [t for t in list(self.SPLIT_RATE.keys()) if self.SPLIT_RATE.get(f'{t}') != 0]
