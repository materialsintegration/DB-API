=====================================
DB-API 
=====================================

各種材料DB(RDB, 商用DB, その他)について、データを取り出すための共通API。


概要
==================================================

| DB-APIの仕様、サンプルスクリプトとその使用方法を提示する。
| 利用可能なDBとそこから抽出できる情報、出力書式など。



使い方
==================================================

| 一般的なRESTful APIと同様に、所定のurlにパラメータを指定してリクエストする。

::

    http://hogehoge/db-api/v1/get/test/NIMS_material/?mimetype=csv&test=creep_rupture_test


| ここではいくつかの検索ロジックをDB-APIに組み込んでいる。
| それらにsample1から5について個別に説明している。



詳細
==================================================

| 各sample1～6の説明を参照のこと。

<https://github.com/materialsintegration/DB-API/tree/master/sample>

| スクリプトからの呼び出しサンプルとして、pythonでのサンプルコードを提示している。
| (python 3.6以上での対応となる)


