# %%
from pathlib import Path

import appdirs


def local_directory() -> Path:
    return Path(appdirs.user_cache_dir())


#%%
print(local_directory()) 

