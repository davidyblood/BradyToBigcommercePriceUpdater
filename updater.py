# purpose: this is the main body of program to run

import logging
import bigcommerce


def bigcommerceTesting():
    products, myerrors = bigcommerce.getProductSku('5060-29-PDM')
    if len(myerrors) > 0:
        logging.info(myerrors)
        print('myerrors: ')
        print(myerrors)
        logging.info(str(myerrors))
    else:
        print()
        print('products:')
        for i in products:
            logging.info(i)
            break
        print('-----------------------------------')

if __name__=='__main__':
    logging.basicConfig(filename='program.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('')

    #bigcommerceTesting()