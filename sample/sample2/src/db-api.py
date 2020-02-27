# -*- coding: utf-8 -*-

# ****************************************************
# * db-api_sample1.py
# *
# *    operate db-api sample1
# *
# *  2020/02/27  T.Noguchi  create
# *
# ****************************************************
#
import os
import sys
import time
import json
import codecs

import requests
import json

# -----------------------------------
# module variable
# -----------------------------------
# base info
api_refroot = 'http://hogehoge/db-api/v1/get/test'

# request param
target_db = 'GRANTA'
mimetype = 'csv'
test = 'tensile_test'

# codec
codec = 'utf-8'

# file
fout = 'db-api.csv'

# =======================================
# local function
# =======================================

# =======================================
# main
# =======================================

def main():
    stime = time.time()
    print('----- start ' + __file__ + ' script -----')    

    # ///////////////////////////////
    #  param
    # ///////////////////////////////
    query = 'mimetype=' + mimetype + '&test=' + test
    url = api_refroot + '/' + target_db + '/?' + query
    
    # ///////////////////////////////
    #  request
    # ///////////////////////////////
    session = requests.Session()
    session.trust_env = False

    response = session.get(url)

    # ///////////////////////////////
    #  save data
    # ///////////////////////////////
    with open(fout, 'w', encoding=codec) as f:
        f.write(response.text)


    print('\n')
    print("------------------------------")
    print("normal completion of " + __file__ + "!!!")
    etime = time.time()
    print ('total time:' + str(etime - stime))
    sys.exit()
    

if __name__== '__main__':
    main()


