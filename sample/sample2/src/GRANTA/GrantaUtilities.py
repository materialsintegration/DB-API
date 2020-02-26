# -*- coding: utf-8 -*-

# ****************************************************
# * GRANTA_Utilities.py
# *
# *    GRANTA MI toolkit utility
# *
# *  2019/12/10  T.Noguchi  create
# *  
# *  
# *
# ****************************************************

import os
import sys
from getpass import getpass

import GRANTA_MIScriptingToolkit as gdl

# =======================================
# config
# =======================================


# =======================================
# local function
# =======================================
default_url = 'http://granta-mi.nims.go.jp/mi_servicelayer'


# =======================================
# modules
# =======================================
# セッションを作成する
# 有効な引数の指定がない場合、ユーザー名、パスワードはインタラクティブに入力する
def getSession(url, user, password):
    '''
    [args]
        url            : GRANTA MI url
        user           : GRANTA user
        password       : GRANTA password

    [return]
        GRANTA_MI.session
    '''

    #param
    granta_url = url if url != '' else default_url
    granta_user = user
    granta_password = password
    granta_domain = ''

    if (granta_user == ''):
        msg = 'GRANTA login user:'
        granta_user = input(msg)
    if (granta_password == ''):
        msg = 'GRANTA login pass:'
        granta_password = getpass(prompt=msg)

    session = gdl.GRANTA_MISession(url=granta_url, username=granta_user, \
        password=granta_password, domain=granta_domain)

    return session


# DB名をキーとした辞書を返す
# session = セッション
# return = DB一覧(key:DB名, value:DB詳細(辞書))
# name = DB名
# DBKey = データベースキー
def getDatabaseList(session):

    databaseList = {}

    # データベースの一覧取得
    browseService = session.browseService
    databases = browseService.GetDatabases().databases

    for database in databases:
        databaseList.setdefault("{0}".format(database.name), {"name": database.name, "DBKey": database.DBKey})

    return databaseList


# Table名をキーとした辞書を返す
# session = セッション
# dbKey = データベースキー
# return = Table一覧(key:Table名, value:Table詳細(辞書))
# name = テーブル名
# detail = テーブル詳細
def getTableList(session, dbKey):

    tableList = {}

    # データベースの一覧取得
    browseService = session.browseService
    # テーブルの一覧表示
    tables = browseService.GetTables(gdl.GetTables(DBKey=dbKey)).tableDetails

    for table in tables:
        tableList.setdefault("{0}".format(table.tableReference.name),
                             {"name": table.tableReference.name, "detail": table})

    return tableList


# DB, table, attributeの一覧を返す
# session = セッション
# return = DBオブジェクトリスト(db, table, attribute, type, unit)
# name = オブジェクト
# detail = 
def getDBobjects(session):

    # get databases
    browseService = session.browseService
    browse = gdl.BrowseService(session.mi_session)

    databases = browseService.GetDatabases().databases

    list_obj = []
    for d in databases:
        db = d.name
        dbkey = d.DBKey
        tables = browseService.GetTables(gdl.GetTables(DBKey=dbkey)).tableDetails
        for t in tables:
            table = t.tableReference.name

            attrreq = gdl.GetAttributeDetailsRequest(\
                    attributeReferences=t.attributeReferences)
            attrres = browse.GetAttributeDetails(attrreq)

            for attrdetail in attrres.attributeDetails:
                dic_sub = {}
                if not attrdetail.isMeta:
                    dic_sub['db'] = db
                    dic_sub['table'] = table
                    dic_sub['attribute'] = attrdetail.name
                    dic_sub['type'] = attrdetail.type
                    dic_sub['unit'] = attrdetail.databaseUnit

                    list_obj.append(dic_sub)

    return list_obj


# テーブルの詳細を取得する
# dbKey = DBKey
# tableName = テーブル名
def getTableDetail(session, dbKey, tableName):
    '''
    [args]
        session        : GRANTA session
        dbKey          : DBKey
        tableName      : table name

    [return]
        tableDetail object

    '''

    browseService = session.browseService
    tables = browseService.GetTables(gdl.GetTables(DBKey=dbKey)).tableDetails

    tableDetail = None

    for table in tables:
        if table.tableReference.name == tableName:
            tableDetail = table
            break

    return tableDetail


# 属性の値を取得する
# (属性のタイプ別に対応する)
# attrValue = 属性値
def getValue(attrValue):
    '''
    [args]
        attrValue      : attributeValue

    [return]
        value          : value
        unit           : unitsymbol
    '''

    value = None
    unit  = None
    dataType = attrValue.dataType if attrValue is not None else None

    if dataType == "RNGE":
        low = attrValue.rangeDataType.low if attrValue.rangeDataType.hasLow else 0.0
        high = attrValue.rangeDataType.high if attrValue.rangeDataType.hasHigh else 0.0

        value = max(low, high)
        unit  = attrValue.rangeDataType.unitSymbol
    elif dataType == "POIN":
        value = attrValue.pointDataType.points[0].value if attrValue else None
        unit  = attrValue.pointDataType.unitSymbol
    elif dataType == "INPT":
        value = attrValue.integerDataValue.value if attrValue else None
        unit  = None
    elif dataType == "STXT":
        value = attrValue.shortTextDataType.value if attrValue else None
    elif dataType == "LTXT":
        value = attrValue.longTextDataType.value if attrValue else None
    elif dataType == "DISC":
        value = attrValue.discreteDataValue.discreteValues[0].value if attrValue else None
    elif dataType == "LOGI":
        value = attrValue.logicalDataValue.value if attrValue else None
    elif dataType == "DATE":
        value = attrValue.dateDataType.value if attrValue else None
    elif dataType == "TABL":
        value = attrValue.tabularDataType.tabularDataRows if attrValue else None
    else:
        value = None
        unit  = None
    
    return value, unit


# GRANTA検索用の条件オブジェクト作成
# dbKey = DBキー
# tableName = テーブル名
# searchCondition = 検索条件
def makeSearchCriterion(dbKey, tableName, searchCondition):
    '''
    [args]
        dbKey          : DB key
        tableName      : table name
        searchCondition: search condition
    
    [return]
        searchCriterion object
    '''

    searchCriterion = None

    tableRef = gdl.PartialTableReference(tableName=tableName)
    attrRef  = gdl.AttributeReference(name=searchCondition["name"], DBKey=dbKey, \
        PartialTableReference=tableRef)
    
    # search condition
    if searchCondition["type"] == 0:
        # 値があることを確認
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            existsSearchValue=gdl.ExistsSearchValue())
    elif searchCondition["type"] == 1:
        # 値がないことを確認
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            doesNotExistSearchValue=gdl.DoesNotExistSearchValue())
    elif searchCondition["type"] == 2:
        # 範囲値を検索
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            betweenSearchValue=gdl.BetweenSearchValue(\
                lowEnd=gdl.LowEndSearchValue(value=searchCondition["value"][0]), \
                highEnd=gdl.HighEndSearchValue(value=searchCondition["value"][1])))
    elif searchCondition["type"] == 3:
        # 以上の検索
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            greaterThanSearchValue=gdl.GreaterThanSearchValue(\
                value=searchCondition["value"][0]))
    elif searchCondition["type"] == 4:
        # 以下の検索
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            lessThanSearchValue=gdl.LessThanSearchValue(\
                value=searchCondition["value"][0]))
    elif searchCondition["type"] == 5:
        # 完全一致
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            exactlySearchValue=gdl.ExactlySearchValue(\
                value=searchCondition["value"][0]))
    elif searchCondition["type"] == 6:
        # 一部含む
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            containsSearchValue=gdl.ContainsSearchValue(searchCondition["value"][0]))
    elif searchCondition["type"] == 7:
        # 含まない
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            doesNotContainSearchValue=gdl.DoesNotContainSearchValue(searchCondition["value"][0]))
    elif searchCondition["type"] == 8:
        # 全てを含む
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            containsAllSearchValue=gdl.ContainsAllSearchValue(searchCondition["value"]))
    elif searchCondition["type"] == 9:
        # いずれかを含む
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            containsAnySearchValue=gdl.ContainsAnySearchValue(searchCondition["value"]))
    elif searchCondition["type"] == 10:
        # 日付期間
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            betweenDateTimeSearchValue=gdl.BetweenDateTimeSearchValue(\
                lowEnd=gdl.LowEndSearchValue(value=searchCondition["value"][0]), \
                highEnd=gdl.HighEndSearchValue(value=searchCondition["value"][1])))
    elif searchCondition["type"] == 11:
        # 表カラムに値を含む
        searchCriterion = gdl.RecordSearchCriterion(searchAttribute=attrRef, \
            tabularColumnContainsSearchValue=gdl.TabularColumnContainsSearchValue(\
                colName=searchCondition["value"][0], \
                value=searchCondition["value"][1]))

    return searchCriterion






