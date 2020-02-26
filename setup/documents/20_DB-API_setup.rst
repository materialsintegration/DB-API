=====================================
DB-APIセットアップ手順
=====================================



システム構成
==================================================


.. csv-table::
    :widths: 10, 20

    OS, CentOS 7.4
    node.js, v11.15.0


関連ソース
==================================================

<https://github.com/materialsintegration/DB-API/blob/master/setup/deploy/v1.0.zip>

.. csv-table::
    :header: ファイル, 内容
    :widths: 15, 40

    v1.0.zip, nodejs構成ファイル一式



セットアップ
==================================================

プロジェクト作成
--------------------------------------------------

予め関連ファイルを格納するディレクトリを作成し、移動しておく。


::

    $ npm init


| * 以降はカレントディレクトリがプロジェクトディレクトリとなる。



デプロイ
--------------------------------------------------

上記のnodejs構成ファイル一式をプロジェクトフォルダ下におき、解凍する。



関連パッケージインストール
--------------------------------------------------

| プロジェクトフォルダ下の、package.jsonファイルのあるフォルダに移動する。
| 以下コマンド実行する。

::

    $ npm install


| * コマンド実行前にnode_modulesディレクトリがある場合は削除しておくこと。
| * 事前に作成済みのシステムがあれば、そのpackage.jsonのあるディレクトリにおいて
|   上記コマンドで環境コピーが可能


DB関連設定
--------------------------------------------------

デプロイコードに予め設定されている検索DBの接続設定を確認し、必要に応じ編集する。


| (nodejs/DBAPI/app/db/Mysql.js)
| (nodejs/DBAPI/app/db/Postgresql.js)

::

    const confs = {
        'NIMS_material' :
        {
            host      : 'xx.xx.xx.xx',
            user      : 'hogehoge',
            password  : '',
            database  : 'database',
            connectionTimeout : 10000, // timeout(msec)
            supportBigNumbers : true, // support bigint, decimal
            connectionLimit : 20, // conn instance number at a time
            removeNodeErrorCount: 3 // retry count
        },
    ...


| * DB接続は、nodejsサーバが該当DBに接続可能なネットワーク環境であることが前提。
| * confs変数に定義されているDB毎の接続情報(host, user, password, database)を編集する。
| * 各DBの接続情報については、DB管理者に確認のこと。



ポート設定
--------------------------------------------------

| サービスで使用するポートの設定を行う。
| 直接ポート開放せずに、何のサービスで開放しているかを明示するためサービスファイルを作成する。


::

    # vi /etc/firewalld/services/nodejs.xml
    #
    > <?xml version="1.0" encoding="utf-8"?>
    > <service>
    >     <short>nodejs</short>
    >     <description>nodejs Server</description>
    >     <port protocol="tcp" port="3300"/>
    > </service>
    #
    # firewall-cmd --reload


* ポート番号は任意


デフォルトゾーンにサービス登録し、反映させる。


::

    # firewall-cmd --permanent --zone=public --add-service=nodejs
    # firewall-cmd --reload
    # firewall-cmd --list-all # (確認用)




サービス起動
--------------------------------------------------

プロジェクトルートディレクトリで以下コマンド実行する。


::

    $ NODE_ENV=production node app.js


サービスがフロントエンドで実行される。



動作確認
--------------------------------------------------

ローカルサイトでブラウザを起動し、以下のURLにアクセスする。


http://<サーバID>:<ポート>/dbapi/v1/get?db=NIMS_material&table=material&mimetype=json&sql=select * from material


データが表示されればOK


