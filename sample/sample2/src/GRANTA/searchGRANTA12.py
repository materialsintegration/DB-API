# -*- coding: utf-8 -*-

# ****************************************************
# * searchGRANTA.py
# *
# *    GRANTA search script
# *
# *  2019/12/11  T.Noguchi  create
# *  
# *  
# *
# ****************************************************

import sys
import os
import glob
import re
import time
import itertools
import pandas as pd
from pint import UnitRegistry

import GRANTA_MIScriptingToolkit as gdl

from class_iniconf import Iniobj
import GrantaUtilities as gutil
import PythonUtilities as putil

# -----------------------------------
# module variable
# -----------------------------------
# config schema
DEFAULT_SCHEMA = {
    'authorize': ['user', 'pass'],
}

# パラメータ(MIシステム用)
outputFileName = "granta_mi.csv"

# export batch size(byte)
BATCH_SIZE = 10000

# pint exception
pint_exceptions = ['%']

# =======================================
# local function
# =======================================

# 現在連携で使用中の関数
# DBキー,Table詳細,取得するカラム情報（目的変数,説明変数）をパラメータとしてもらう
# dbName = データベース名
# dbKey = データベースキー
# tableDetail = テーブル詳細（GRANTA-MIで定義されているもの）
# paramColumns = 検索するカラム（目的変数、説明変数）
# outColumns = 出力カラム名
# outUnits = 出力単位
# outputFileName = 出力ファイル名
def searchGRANTA(session, dbName, dbKey, tableDetail, paramColumns, \
                 outColumns, outUnits, outputFileName):

    # テーブルの選択
    table_name = tableDetail.tableReference.name
    tableRef = gdl.TableReference(DBKey=dbKey, name=table_name)
    partialTableRef = gdl.PartialTableReference(tableName=table_name)

    # ---------------------------
    # 全件検索
    # ---------------------------
    print('(python)[get searchResults]')
    start = time.time()

    # ルート取得
    req = gdl.GetRootNode(tableRef)
    res = session.browseService.GetRootNode(req)

    root_node_ref = res.rootNode.recordReference

    # 子ノード取得
    req = gdl.GetChildNodes(recurse=True, populateGUIDs=True, \
                            parent=root_node_ref)
    res = session.browseService.GetChildNodes(req)

    # 全件検索
    recordRecs = recursive_node(res.treeRecords, [])
    recordRefs = [r.recordReference for r in recordRecs]

    # レコード状態検索
    tmp_recordRefs = []
    if len(recordRefs) != 0:
        for batch in _grouper(recordRefs, BATCH_SIZE):
            chunk_recordRefs = [r for r in batch]
            req = gdl.GetRecordVersionsRequest(records=chunk_recordRefs, \
                                               versions=0) 
            res = session.browseService.GetRecordVersions(req).recordStates
            tmp_recordRefs.extend([x.recordReference for x in res])
    #new_recordRefs = list(set([r.recordReference for r in res.recordStates]))
    new_recordRefs = list(set(tmp_recordRefs))

    print('(python)    len(recordRefs):', len(new_recordRefs))
    elapsed_time = time.time() - start
    print("(python)    elapsed_time:{0}".format(elapsed_time) + "[sec]")

    # テーブルのキー項目(recordGUID)を取得
    df = pd.DataFrame({'Database': [dbName for r in new_recordRefs], \
                       'recordGUID': [r.recordGUID for r in new_recordRefs]})
    #                   'states': [r.versionState for r in res.recordStates]})

    # ---------------------------
    # その他Attributeを検索
    # ---------------------------
    print('(python)[get recordDatas]')
    start = time.time()

    attributes = paramColumns
    recordGUID = []
    recordData = []
    # attributes.extend(paramOption)
    if len(recordRefs) != 0:
        attrRefs = [gdl.AttributeReference(name=a, DBKey=dbKey, \
                    partialTableReference=partialTableRef) \
                    for a in attributes if a != '']
        for batch in _grouper(new_recordRefs, BATCH_SIZE):
            chunk_recordRefs = [r for r in batch]
            request = gdl.GetRecordAttributesByRefRequest(\
                          recordReferences=chunk_recordRefs, \
                          populateGUIDs=True, \
                          attributeReferences=attrRefs)
            results = session.dataExportService.\
                      GetRecordAttributesByRef(request).recordData
            recordData.extend(results)
            recordGUID.extend([r.recordReference.recordGUID for r in results])


    print('(python)    len(recordData):', len(recordData))
    elapsed_time = time.time() - start
    print("(python)    elapsed_time:{0}".format(elapsed_time) + "[sec]")

    print('(python)[get attributes]')
    start = time.time()

    # レコードごとの属性値を抽出
    ureg = UnitRegistry()
    s = [None] * len(df)
    for i, attribute in enumerate(attributes):
        ss   = s.copy()
        ss_u = s.copy()
        if attribute != '':
            # make row data
            col = attribute
            Q_ = ureg.Quantity
            for idx, record in enumerate(recordData):
                # x <- AttributeValue
                attrValue = next((x for x in record.attributeValues \
                                  if x.attributeName == attribute), None)
                val, unitsymbol = gutil.getValue(attrValue)
                if val is not None and unitsymbol is not None:
                    # convert unit
                    try:
                        if unitsymbol in pint_exceptions:
                            ss[idx] = val
                        elif unitsymbol.replace(' ','') == '':
                            ss[idx] = val
                        else:
                            exchange_value = Q_(val, unitsymbol).to(outUnits[i])
                            ss[idx] = exchange_value.magnitude
                    except Exception as e:
                        print('(python)[warning] at val:', val, \
                                                 ' unit:', unitsymbol)
                        print('(python)cannot convert unit. skip operation..')
                        ss[idx] = val

        col = outColumns[i]
        df[col] = ss

    df['recordGUID'] = recordGUID

    elapsed_time = time.time() - start
    print("(python)    elapsed_time:{0}".format(elapsed_time) + "[sec]")
    
    # csv出力
    if (outputFileName != ''):
        df.to_csv(outputFileName, index=0)

    return df

# ノードの再帰検索
# tree_records = 検索対象ツリーノード
# recs = 再帰データ保存用リスト
# level = 階層レベル
def recursive_node(tree_records, recs, level=0):
    treerecs = recs

    for tree_record in tree_records:
        tmp_recs = None
        if tree_record.children:
            tmp_recs = recursive_node(tree_record.children, treerecs, level + 1)

        else:
            if tree_record.type == 'Record':
                treerecs.extend([tree_record])

    return treerecs

# データ分割
# iterable = オブジェクト(イテラブル)
# n = バッチサイズ(byte)
def _grouper(iterable, n):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

# =======================================
# main
# =======================================

def main():
    stime = time.time()
    print('(python)----- start ' + __file__ + ' script -----')

    # init
    in_conf = ''
    in_schema = ''
    in_mime = 'csv'
    args = sys.argv
    
    for index, arg in enumerate(args):
        if (index == 1):
            in_conf = args[1]
        if (index == 2):
            in_schema = args[2]
        if (index == 3):
            in_mime = args[3]

    if (in_conf == '') or (in_schema == ''):
        print('(python)command argument is invalid.')
        print('(python)[usage]')
        print('(python)  python ' + __file__ + ' <conf_file> <schema_file>')
        sys.exit()

    # output file name(for DB-API)
    #std_in = sys.stdin.readline()
    #if std_in != '':
    #    outputFileName = std_in.rstrip('\n')

    # ///////////////////////////////
    #  read config file
    # ///////////////////////////////    
    config = None
    config = Iniobj(in_conf, DEFAULT_SCHEMA)

    user      = config.get('authorize', 'user')
    password  = config.get('authorize', 'pass')

    # show configure
    print('(python)[conf file]')
    print('(python)user        : ' + user)
    #print('(python)outputFile  : ' + outputFileName)

    # ///////////////////////////////
    #  read schema file
    # ///////////////////////////////
    df_schema = pd.read_csv(in_schema, header=[0,1])
    df_schema = putil.multi_headers(df_schema)
    df_schema.fillna('', inplace=True)

    schema_cols = list(df_schema.columns)
    outform_cols = df_schema.iloc[:, 1].values.tolist()
    database_names = [ x[0] for x in schema_cols[2:]]
    table_names = [x[1] for x in schema_cols[2:]]

    attr_names = {}
    for i, db_name in enumerate(database_names):
        attr_names[db_name] = df_schema[db_name, table_names[i]].values.tolist()

    # output units
    units = [re.findall(r'\[.*?\]$', x)[-1].replace('[', '').replace(']', '') \
             for x in outform_cols]

    # create output dataframe
    df_out = pd.DataFrame(columns=['recordGUID'] + outform_cols)

    # ///////////////////////////////
    # process each list
    # ///////////////////////////////
    for idx, database_name in enumerate(database_names):
        print('(python)database:', database_name)

        #fout = ''
        fout = database_name + '.' + in_mime

        # session
        # note)
        #   reconnect each database session to avoid server error 
        url = ''
        session = gutil.getSession(url, user, password)

        # databases
        browseService = session.browseService
        databases = browseService.GetDatabases().databases

        # *******************************
        # database param
        # *******************************
        # get database
        obj_names = [x.name for x in databases]

        database = None
        if (database_name in obj_names):
            database = databases[obj_names.index(database_name)]
        else:
            print('(python)database ' + database_name + ' is not exist')
            print('(python)check your schema file')
            sys.exit()
        dbkey = database.DBKey

        # *******************************
        # table param
        # *******************************
        # get table
        tables=browseService.GetTables(gdl.GetTables(DBKey=dbkey)).tableDetails

        obj_names = [x.tableReference.name for x in tables]

        table = None
        if (table_names[idx] in obj_names):
            table = tables[obj_names.index(table_names[idx])]
        else:
            print('(python)table ' + table_names[idx] + ' is not exist')
            print('(python)check your schema file')
            sys.exit()

        # *******************************
        # attributes param
        # *******************************
        # get attrs
        #attrs = []
        #browse = gdl.BrowseService(session.mi_session)

        '''
        # search attrs
        attrreq = gdl.GetAttributeDetailsRequest(\
                attributeReferences=table.attributeReferences)
        attrres = browse.GetAttributeDetails(attrreq)

        for attrdetail in attrres.attributeDetails:
            if not attrdetail.isMeta:
                attrs.append({'name': attrdetail.name, \
                              'type': attrdetail.type, \
                              'unit': attrdetail.databaseUnit})
        '''
        attrlist = attr_names[database_name]
        # set nan attrs to output attrs
        #attrlist = [attr_names[idx][i] \
        #            if attr_names[idx][i] != '' else outform_cols[i] \
        #            for i in range(len(attr_names[idx]))]

        # *******************************
        # get dataset
        # *******************************
        tableDetail = gutil.getTableDetail(session, dbkey, \
                                          table.tableReference.name)
        df_sdb = searchGRANTA(session, database_name, dbkey, tableDetail, \
                              attrlist, outform_cols, units, fout)

        # concat
        #outform_cols.insert(0, 'recordGUID')
        #df_sdb.columns = ['recordGUID'] + outform_cols
        df_tmp = pd.concat([df_out, df_sdb], sort=False)
        df_out = df_tmp

    # sort columns
    new_outform_cols = ['Database', 'recordGUID']
    new_outform_cols.extend(outform_cols)
    df_out = df_out[new_outform_cols]

    # drop all nan row
    df_out.dropna(subset=outform_cols, how='all', inplace=True)

    # output all data
    #df_out.to_csv(outputFileName, index=0)
    #df_out.to_csv(sys.stdout, index=0)
    if (in_mime == 'csv'):
        df_out.to_csv(sys.stdout, index=0)
    elif (in_mime == 'json'):
        df_out.to_json(sys.stdout, orient='records')

    print('\n')
    print("(python)------------------------------")
    print("(python)normal completion of " + __file__ + "!!!")
    etime = time.time()
    print ('(python)total time:' + str(etime - stime))
    sys.exit()


if __name__=="__main__":
    main()

