from config import Settings
from data_process import _dfSplit
from json_process import _fillJson, _writeJson


class Loader:
    SETTINGS: Settings = None

    def __init__(self, settings: Settings):
        self.SETTINGS = settings

    def load_train(self, df):
        data = _fillJson(self.SETTINGS, df)
        _writeJson(self.SETTINGS.ANNOTATIONS_DIR, data, "train")

    def load_train_and_val(self, df):
        train_df, val_df = _dfSplit(df, self.SETTINGS.SPLIT_RATE)
        train_data = _fillJson(self.SETTINGS, train_df)
        val_data = _fillJson(self.SETTINGS, val_df, is_train=False)
        _writeJson(self.SETTINGS.ANNOTATIONS_DIR, val_data, "val")
        _writeJson(self.SETTINGS.ANNOTATIONS_DIR, train_data, "train")