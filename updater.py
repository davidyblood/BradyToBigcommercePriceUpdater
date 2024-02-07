# purpose: this is the main body of program to run

import logging

if __name__=='__main__':
    logging.basicConfig(filename='program.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('')