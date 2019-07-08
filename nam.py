#!/bin/python3
import argparse
import json
import time
import os
import logging
import re

def do_rename(config):
    
    regexs = [
        re.compile(r'\d+\-\d+\-\d+$'), 
        re.compile(r'\d+$')
    ]

    for folder in config['folders']:
        logger.debug("Monitoring {} . . .".format(os.path.abspath(folder)))
        for file in os.listdir(folder):
            original = os.path.join(folder,file)
            fn, ext = os.path.splitext(file)
            #import pdb; pdb.set_trace()
            for regex in regexs:
                if regex.search(fn) and os.path.isfile(original):
                    #import pdb; pdb.set_trace()
                    logger.debug("Renaming {}".format(original))
                    fn_new = regex.sub('',fn)
                    
                    destination = os.path.join(folder, fn_new + ext)
                    os.rename(original,destination)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--single', action='store_true')
    args = parser.parse_args()

    with open('./config.json', 'r') as fp:
        config = json.load(fp)

    # Setup Logger
    logging_format = '%(asctime)s - %(message)s'
    logging.basicConfig(filename=config['log_file'], level=logging.DEBUG,
                        format=logging_format)
    
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())

    if args.single:
        do_rename(config)
        exit()
    
    while True:
        do_rename(config)
        time.sleep(2)


    
    
