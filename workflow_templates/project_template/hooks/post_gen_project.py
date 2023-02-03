import os
from pathlib import Path
import shutil
import halerium_utilities as hu

print("assigning new ids")
# assign new card ids
hu.file.assign_new_card_ids_to_tree('./')


print("Move one directory up")
# To move directory one up
for f in os.listdir('./'):
    shutil.move(f, '../')

print("Delete obsolete dir")
path = Path('./').resolve()
shutil.rmtree(path)

print("Done")