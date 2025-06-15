import os


# 'elastyczna' sciezka do plikow
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(*parts, own_path=False):
    if own_path: return os.path.join(BASE_DIR, *parts)
    return os.path.join(BASE_DIR, "images", *parts)
