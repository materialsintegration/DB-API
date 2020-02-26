=====================================
node.jsインストール手順
=====================================



システム構成
==================================================


    .. csv-table::
        :widths: 10, 20

        OS, CentOS 7.4
        nodejs, 11.x


セットアップ
==================================================

node.jsセットアップ
--------------------------------------------------

yumを使用してインストールする。


    ::

        # sudo yum install https://rpm.nodesource.com/pub_11.x/el/7/x86_64/nodesource-release-el7-1.noarch.rpm
        # sudo yum install nodejs -y


  * パッケージ管理ツールnpmを最新版にする。


    ::

        $ sudo npm update -g npm


  * npmは現在のユーザーのhomeディレクトリ以下にインストールされる。


  .. note::

    | npmでエラーが出る場合、proxy関連の設定に問題がある場合がある。
    | その場合、以下コマンド実行する。
    |
    | npm -g config set proxy "http://<server>:<port>/"
    | npm -g config set https-proxy "https://<server>:<port>/"
    | npm -g config set registry "http://registry.npmjs.org/"


