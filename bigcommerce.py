# purpose: all functions related to getting and setting prices on bigcommerce.py

import requests
import json

STOREID = "sme7h"
TOKEN = "102albp9dekp7ewfo0xs1mh3cf6nwyp"
URL1 = "https://api.bigcommerce.com/stores/"
CATALOG = "/v3/catalog/"
HEADERS = {
        'accept': "application/json",
        'content-type': "application/json",
        'x-auth-token': TOKEN
    }


def getRequests(typeRequest, searchType, params=None):
    # typeReqeust is "GET", "PUT", etc
    # searchType is Variants, products, sku, etc

    # first build url
    url = URL1+STOREID+CATALOG+searchType

    # now get response based on whether there is params or not
    if params != None:
        response = requests.request(typeRequest, url, headers=HEADERS, params=params)
    else:
        response = requests.request(typeRequest, url, headers=HEADERS)

    return json.loads(response.text)


def getAllVariants(myErrors=[]):
    # this search will get all products and variants together
    data = None
    products = []
    querystring = {"limit":"5000"}
    data = getRequests("GET", searchType="variants", params=querystring)

    #pull products out of data
    for item in data['data']:
        products.append(item)

    # get next page of data until their is no more
    while 'next' in data['meta']['pagination']['links']:
        data = getRequests("GET", searchType="variants"+ data['meta']['pagination']['links']['next'], params=querystring)
        for item in data['data']:
            products.append(item)

    return products, myErrors


def findProductById(id, myErrors=[]):
    # searches products for a particular product id
    response = getRequests("GET", searchType="products/"+str(id))
    return response['data'], myErrors


def findSku(sku, myErrors=[]):
    # searches variants for a particular sku
    querystring = {"sku":sku}
    response = getRequests("GET", searchType="variants", params=querystring)
    return response['data'], myErrors


def getProductVariants(id, myErrors=[]):
    # retrieve variants for a particular product based on product id
    response = getRequests("GET", searchType="products/" + str(id)+ "/variants")
    return response['data'], myErrors


def getProductName(name, myErrors=[]):
    # retrieve a product based on product name
    response = getRequests("GET", searchType="products?name="+name)
    return response['data'], myErrors


def getProductSku(sku, myErrors=[]):
    # retrieve a product based on supplied sku
    response = getRequests("GET", searchType="products?sku="+sku)
    if response.get('data', None) == None:
        myErrors.append('response: ', response)
    return response['data'], myErrors


def getAllProducts(myErrors=[], limit='5000'):
    # retrieve all products from Bigcommerce
    data = None
    products = {}

    querystring = {"sort":"date_modified","limit":"5000"}
    data = getRequests("GET", searchType="products", params=querystring)

    #pull products out of data
    products = data['data']
    if int(limit) == 5000:
        # get next page of data until their is no more
        while 'next' in data['meta']['pagination']['links']:
            data = getRequests("GET", searchType="products"+ data['meta']['pagination']['links']['next'], params=querystring)
            for item in data['data']:
                products.append(item)

    return products, myErrors

    #querystring = {"date_modified":"True","direction":"desc"}


def updateProduct(item,myErrors=[]):
    # update a bigcommerce item based on supplied dictionary
    result = None
    url = "https://api.bigcommerce.com/stores/sme7h/v3/catalog/products/" + str(item['id'])
    payload = "{\"availability\":\"disabled\"}"

    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'x-auth-token': "102albp9dekp7ewfo0xs1mh3cf6nwyp",
        }

    response = requests.request("PUT", url, data=payload, headers=headers)
    result = json.loads(response.text)

    return result, myErrors


def deleteProduct(item):
    # delete a bigcommerce item based on item number
    result = None
    url = "https://api.bigcommerce.com/stores/sme7h/v3/catalog/products/" + str(item)

    headers = {
        'accept': "application/json",
        'content-type': "application/json",
        'x-auth-token': "102albp9dekp7ewfo0xs1mh3cf6nwyp",
        }

    response = requests.request("DELETE", url, headers=headers)
    result = response.text

    return result

