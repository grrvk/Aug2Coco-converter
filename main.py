from config import Settings
from data_process import _getDf
from loader import Loader


def main(working_directory, return_path: str | None, split_rate: float | None):
    settings = Settings(working_dir=working_directory, return_path=return_path, split_rate=split_rate)
    loader = Loader(settings)
    df = _getDf(settings.WORKING_DIR)
    if settings.SPLIT_RATE:
        loader.load_train_and_val(df)
    else:
        loader.load_train(df)
    print(f"Dataset generated successfully!")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Convert gen/aug dataset data to COCO format')
    parser.add_argument('--working_directory', metavar='path', required=True,
                        help='the path to directory with pictures and json file')
    parser.add_argument('--return_path', metavar='path', required=False,
                        help='path to place to save COCO dataset')
    parser.add_argument('--split_rate', metavar='N', type=float, required=False,
                        help='float between 0 and 1 for train/validation split')
    args = parser.parse_args()
    main(working_directory=args.working_directory, return_path=args.return_path,
         split_rate=args.split_rate)
