=====================================
DB-APIサービス化手順
=====================================



システム構成
==================================================


    .. csv-table::
        :widths: 10, 20

        OS, CentOS 7.4
        node.js, v11.15.0


設定手順
==================================================

systemd環境設定
--------------------------------------------------

systemd環境設定ファイルを生成する。


::

    # vi /etc/sysconfig/nodejs_env
    #
    > NODE_ENV=production


サービス設定ファイル
--------------------------------------------------

サービス設定ファイルを生成する。


::

    # vi /etc/systemd/system/nodejs.service
    > [Unit]
    > Description=nodejs server
    > After=syslog.target network.target
    > 
    > [Service]
    > Type=simple
    > ExecStart=/home/misystem/.nvm/versions/node/v12.3.0/bin/node --max_old_space_size=8192 /home/misystem/nodejs/DBAPI/app/app.js <= プロジェクトのスタートアプリを指定
    > WorkingDirectory=/home/misystem/nodejs/DBAPI/app <= nodejsのプロジェクトフォルダ以下のインデックスファイルの場所を指定
    > KillMode=process
    > Restart=always
    > User=misystem
    > Group=misystem
    > EnvironmentFile=/etc/sysconfig/nodejs_env
    > 
    > [Install]
    > WantedBy=multi-user.target


systemctl登録
--------------------------------------------------

systemctlに登録する。


::

    # systemctl enable nodejs
    # systemctl start nodejs


動作確認
--------------------------------------------------

以下コマンド実行する。

::

    # systemctl status nodejs
    >
    > ● nodejs.service - nodejs server
    >   Loaded: loaded (/etc/systemd/system/nodejs.service; enabled; vendor preset: disabled)
    >   Active: active (running) since Wed 2020-01-22 14:40:02 JST; 5 days ago
    >   Main PID: 21728 (node)
    > ...


上記のようにActive: activeと表示されていればOK.


