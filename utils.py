import os


def _mkdir(path):
    if os.path.exists(path) is False:
        os.mkdir(path)
    else:
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                os.remove(os.path.join(path, filename))