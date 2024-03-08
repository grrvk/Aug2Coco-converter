from converter.settings import Settings
from converter.data_process import _getDf
from converter.loader import Loader


def convert(working_directory_path: str, return_path: str | None,
            split_type, split_rate, upload: bool = False):
    settings = Settings(working_dir=working_directory_path, return_path=return_path,
                        split_type=split_type, split_rate=split_rate,
                        upload=upload)
    print(settings)

    loader = Loader(settings)
    df = _getDf(settings.WORKING_DIR)
    loader.load(df)

    print(f"Dataset generated successfully!")
