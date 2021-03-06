#!/bin/python3
import argparse
import json
import time
import os
import logging
import re
import Check_Common
import sys

DoneList = set()


def DoRename(config):

    names = config['Renames']
    folder = config['FileDir']

    logger.debug("Processing {} . . .".format(os.path.abspath(folder)))
    for file in sorted(os.listdir(folder)):
        original = os.path.join(folder, file)
        if not os.path.isfile(original):
            continue

        fn, ext = os.path.splitext(file)
        _, ext2 = os.path.splitext(fn)

        for name in names:
            destination = os.path.join(folder, name + ext2 + ext)
            if not fn.startswith(name) or fn == name or destination in DoneList:
                continue

            if os.path.isfile(destination):
                os.remove(destination)

            logger.debug("Renaming {} to {}".format(
                original, destination))
            os.rename(original, destination)
            DoneList.add(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--loop', action='store_true')
    args = parser.parse_args()

    if not os.path.isfile(Check_Common.ConfigFileLocation):
        print("Cannot find configuration file {}".format(
            Check_Common.ConfigFileLocation))
        sys.exit()

    with open(Check_Common.ConfigFileLocation, 'rt') as fp:
        config = json.load(fp)

    # Setup Logger
    loggingFormat = '%(asctime)s - %(message)s'
    logging.basicConfig(filename=config['LogDoc'], level=logging.DEBUG,
                        format=loggingFormat)

    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())

    if not "Renames" in config:
        logger.debug(
            "Please add 'Renames' key in your configuration so I will know what files to be rename.")
        sys.exit()

    if not args.loop:
        DoneList.clear()
        DoRename(config)
    else:
        # Pass argument "loop" if you want the script to run
        # in a loop mode (Usage: python nam.py --loop)
        while True:
            DoneList.clear()
            DoRename(config)
            time.sleep(2)
