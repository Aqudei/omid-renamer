#!/bin/python3
import argparse
import json
import time
import os
import logging
import re
import IM_Common
import sys
import json
import argparse
import shutil

logger = None

DoneList = dict()


def name_match(name):
    for search in args.lookup_names:
        if name.startswith(search):
            return True
    return False


def DoRename(config, lookup_names):
    renames_count = 0

    folder = config['FileDir']

    logging.info('***')
    logging.info('***')
    logging.info('***')
    logging.info('*** Started Process to Rename Files')

    for File in sorted(os.listdir(folder), reverse=True):
        original_file = os.path.join(folder, File)
        if not os.path.isfile(original_file):
            continue

        new_name = IM_Common.trim_date(File)
        fn, _ = os.path.splitext(new_name)

        for name in lookup_names:

            destination = os.path.join(folder, new_name)
            clean_name = os.path.basename(destination)
            if not fn.startswith(name) or new_name == name or clean_name in DoneList:
                continue

            # if os.path.isfile(destination):
            #     # Skip existing file
            #     continue

            logger.info("Renamed {} to {}".format(
                original_file, destination))
            # os.rename(original_file, destination)
            shutil.move(original_file, destination)
            renames_count = renames_count + 1
            DoneList[clean_name] = File

    if renames_count == 0:
        logger.debug("No item was renamed!")
    else:
        logger.debug("A total of {} items were renamed".format(renames_count))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'lookup_names', type=str)
    args = parser.parse_args()

    lookup_names = [a.strip() for a in args.lookup_names.split(",")]

    if not os.path.isfile(IM_Common.ConfigFileLocation):
        print("Cannot find configuration file {}".format(
            IM_Common.ConfigFileLocation))
        sys.exit()

    with open(IM_Common.ConfigFileLocation, 'rt') as fp:
        config = json.load(fp)

    # Setup Logger
    loggingFormat = '%(asctime)s - %(message)s'
    logging.basicConfig(filename=config['LogDoc'], level=logging.DEBUG,
                        format=loggingFormat)

    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())

    logger.debug("Using lookup names: %s", lookup_names)
    DoRename(config, lookup_names)
