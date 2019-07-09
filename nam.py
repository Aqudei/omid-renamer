#!/bin/python3
import argparse
import json
import time
import os
import logging
import re


def do_rename(config):

    names = config['names']

    for folder in config['folders']:
        logger.debug("Processing {} . . .".format(os.path.abspath(folder)))
        for file in os.listdir(folder):
            original = os.path.join(folder, file)
            if not os.path.isfile(original):
                continue

            fn, ext = os.path.splitext(file)
            #import pdb; pdb.set_trace()
            for name in names:
                if fn.startswith(name) and not fn == name:
                    #import pdb; pdb.set_trace()
                    logger.debug("Renaming {}".format(original))

                    destination = os.path.join(folder, name + ext)
                    if os.path.exists(destination):
                        os.remove(destination)
   
                    os.rename(original, destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--loop', action='store_true')
    args = parser.parse_args()

    with open('./config.json', 'r') as fp:
        config = json.load(fp)

    # Setup Logger
    logging_format = '%(asctime)s - %(message)s'
    logging.basicConfig(filename=config['log_file'], level=logging.DEBUG,
                        format=logging_format)

    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())

    if not args.loop:
        do_rename(config)
        exit()

    while True:
        do_rename(config)
        time.sleep(2)
