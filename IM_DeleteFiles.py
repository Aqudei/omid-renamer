# Import libraries
import sys
import json
import os
import shutil
from datetime import datetime
from datetime import timedelta
from datetime import date
import logging
import IM_Common
import argparse

deleted_count = 0

parser = argparse.ArgumentParser()
parser.add_argument("lookup_names", type=str)
args = parser.parse_args()

lookup_names = [a.strip() for a in args.lookup_names.split(",")]


if not os.path.isfile(IM_Common.ConfigFileLocation):
    print("Config File: {} not found.".format(
        IM_Common.ConfigFileLocation))
    sys.exit(1)

# Import config file & parameters
with open(IM_Common.ConfigFileLocation, 'rt') as ConfigFile:
    ConfigData = json.load(ConfigFile)

ArchiveDir = ConfigData['ArchiveDir']
LogDoc = ConfigData['LogDoc']
TrackerDoc = ConfigData['ArchiveTrackerDoc']
ArchiveDays = int(ConfigData['ArchiveDays'])
FileDir = ConfigData['FileDir']

# Setup Logger
logging_format = '%(asctime)s - %(message)s'
logging.basicConfig(filename=LogDoc, level=logging.DEBUG,
                    format=logging_format)
logger = logging.getLogger()

logger.addHandler(logging.StreamHandler())


# Check for dependencies
if not os.path.exists(ArchiveDir):
    logger.info(
        'Did not find Archive Directory. Check if directory exists or if path is correct in ConfigFile, then rerun app.')
    sys.exit()

if not os.path.isfile(LogDoc):
    logger.info(
        'Did not find Log Document. Check if directory exists or if path is correct in ConfigFile, then rerun app.')
    sys.exit()

logging.debug('***')
logging.debug('***')
logging.debug('***')
logging.debug('*** Started Process to Delete Renamed Files')
logging.debug("Using Lookup Names: %s" % args.lookup_names)

for file in os.listdir(FileDir):
    if not IM_Common.name_match(file, lookup_names):
        continue

    # new_name = IM_Common.trim_date(file)
    # if new_name == file:
    #     continue

    fn = os.path.join(FileDir, IM_Common.trim_date(file))
    if not os.path.isfile(fn):
        continue

    os.remove(fn)
    deleted_count = deleted_count + 1
    logger.info("{} deleted".format(fn))


if deleted_count == 0:
    logger.debug("No item was deleted!")
else:
    logger.debug("A total of {} items were deleted!".format(deleted_count))
