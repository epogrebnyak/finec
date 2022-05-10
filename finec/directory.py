from pathlib import Path

import appdirs


def local_directory():
    return Path(appdirs.user_cache_dir())
