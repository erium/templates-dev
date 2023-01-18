import os
from pathlib import Path
import shutil
import halerium_utilities as hu

try:
    # assign new card ids
    hu.file.assign_new_card_ids_to_tree('./')


    # To move directory one up
    for f in os.listdir('./'):
        shutil.move(f, '../')

    path = Path('./').resolve()
    shutil.rmtree(path)
    
    raise Exception(str(path))

except Exception as exc:
    with open("../fail", "w") as f:
        f.write(repr(exc))
