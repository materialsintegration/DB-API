=====================================
DB-API 利用手順2
=====================================


概要
==================================================

| 本ドキュメントでは、DB-APIによるデータ検索の手順について説明する。


対象
==================================================

.. csv-table::
    :header: 項目, 内容, 備考
    :widths: 20, 20, 20

    検索対象, GRANTA DB, GRANTA社の商用材料DB。複数のDBからなる
    検索内容, 引張試験情報,



使用方法
==================================================

| 所定のURLにアクセスする。

::

    http://<db-apiサーバ名>/db-api/v1/get/test/GRANTA/?mimetype=csv&test=tensile_test


* サーバ名(アドレス)は管理者に確認のこと。
* クエリパラメータ(mimetype, test)には以下指定可能。

.. csv-table::
    :header: 項目, 内容, 備考
    :widths: 20, 20, 20

    mimetype, csv/json,
    test, tensile_test, 


| 結果として以下のデータを指定書式(csv/json)にて出力する。

.. csv-table::
    :header: 項目, 内容, 備考
    :widths: 20, 20, 20

    Database, GRANTAのDB名,
    recordGUID, GRANTAのレコードID,
    Ni[%], 組成Niの含有量(%),
    Al[%], 組成Alの含有量(%),
    B[%], 組成Bの含有量(%),
    C[%], 組成Cの含有量(%),
    Co[%], 組成Coの含有量(%),
    Cr[%], 組成Crの含有量(%),
    Fe[%], 組成Feの含有量(%),
    Mn[%], 組成Mnの含有量(%),
    Mo[%], 組成Moの含有量(%),
    Nb[%], 組成Nbの含有量(%),
    Ta[%], 組成Taの含有量(%),
    P[%], 組成Pの含有量(%),
    S[%], 組成Sの含有量(%),
    Si[%], 組成Siの含有量(%),
    Ti[%], 組成Tiの含有量(%),
    W[%], 組成Wの含有量(%),
    Zr[%], 組成Zrの含有量(%),
    Nb+Ta[%], 組成Nb+Taの含有量(%),
    vickers_hardness[HV], ビッカース硬さ(HV),
    tensile_strength[MPa], 引張強度(MPa),
    yield_strength[MPa], 降伏応力(MPa),
    proof_stress_comma2pct[MPa], 0.2%耐力(MPa),
    elongation[%], 伸び(%),


備考
==================================================

本件の検索処理には数分かかる。

