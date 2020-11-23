import os
from pathlib import Path
import backup_006_several_pathes
import importlib
import time
#import datetime
from datetime import datetime, timedelta

cwd = Path(__file__).parents[0]
os.chdir(cwd)

a = 0
while a == 0:
    print('searching for unreserved files in destination folder...' + ' at ' + str(datetime.now()))
    importlib.reload(backup_006_several_pathes)
    print('all files reserved.'+ str(datetime.now()))
    print('next check at ' + str(datetime.now() + timedelta(minutes=60)))
    time.sleep(3600)


