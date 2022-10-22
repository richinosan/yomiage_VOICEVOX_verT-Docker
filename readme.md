# yomiage_VOICEVOX(verT-20220924)-Docker

by かみみや

forked by タクト

Docker Image forked by Richinosan

## 概要

DiscordのチャットをVOICEVOX・COEIROINK・LMROID・SHAREVOXで読み上げるソフトです。

python読める＆docker実行できる人向けです。

コマンド一覧は[command_list.html](command_list.html)を参照してください。

## 機能紹介

1. チャットの読み上げ
2. 単語の読み仮名登録
3. ユーザー毎に使用ボイスを変える
4. ボイスチャット入室時の通知（オンオフ切り替え可能）
5. 時報機能（オンオフ切り替え可能）


## ファイル構造(重要度順)

1. **readme.md**
   - これです。使い方などかいているのでお読みください。
2. **readme.html**
   - exe版を利用する場合はこちらをお読みください
3. **前バージョンからの移行方法.txt**
   - 以前のバージョンを使っていた場合はこれを参考にしてデータ（単語帳など）を引き継いでください
4. **discordbot.exe**
   - 実行ファイル
5. **discordbot.py**
   - コマンドプロンプトから実行する場合はこちらを使ってください
6. **setting.ini**
   - 各種設定ファイルです。今のところ「ソフトウェア別に使用するかどうか」「デフォルト話者とスタイルの設定」「データファイルの場所」を設定できます。
7. **TOKEN.txt**
   - BOTのアクセストークンを保存するファイル
8. **command_list.html**
   - 実装されているコマンドの確認
9. **Synthax_setting.csv**
   - コマンドおよびコメントの先頭の文字を設定するファイル
10. **for_developer**
   - ソースファイル
11. **data**
   - 単語帳などが保存されるファイル。開く必要はあまりないです。
12. **get_speakers_from_VOICEVOX.sh**
   - VOICEVOXから話者の情報を取得するshファイル。通常は編集する必要はありません。
13. **output_json_from_VOICEVOX.sh**
   - VOICEVOXでjsonファイルを作成するshファイル。通常は編集する必要はありません。
14. **output_voice_from_VOICEVOX.sh**
   - VOICEVOXで音声を作成するshファイル。通常は編集する必要はありません。
15. **tmp**
    - 一時的に出力されるファイル（VOICEVOXで出力した音声ファイル等）が保存されます。開く必要は全くないです。

## docker-compose.ymlのEnvironment

1. **TZ**
   - タイムゾーンです。デフォルトではAsia/Tokyoにセットされています。

2. **TOKEN**
   - botで使用するトークンです。環境変数を設定しない場合、TOKEN.txtを参照します。

3. **COMMAND_SYNTHAX**
   - コマンドの接頭辞です。環境変数を設定しない場合、Synthax_setting.csvを参照します。

4. **COMMENT_SYNTHAX**
   - コメント文を表すシンタックスです。環境変数を設定しない場合、Synthax_setting.csvを参照します。

5. **OTHER_BOTS_SYNTHAX**
   - 他のbotの接頭辞です。コンマ区切りで複数設定できます。ここで指定された接頭辞がつくコマンドに対して読み上げを行いません。環境変数を設定しない場合、Synthax_setting.csvを参照します。

6. **USE_VOICEVOX**
   - VOICEVOXのboolです。使用する場合はTrueに設定します。環境変数を設定しない場合、setting.iniを参照します。

7. **USE_COEIROINK**
   - COEIROINKのboolです。使用する場合はTrueに設定します。環境変数を設定しない場合、setting.iniを参照します。
   
8. **USE_LMROID**
   - LMROIDのboolです。使用する場合はTrueに設定します。環境変数を設定しない場合、setting.iniを参照します。

9. **USE_SHAREVOX**
   - SHAREVOXのboolです。使用する場合はTrueに設定します。環境変数を設定しない場合、setting.iniを参照します。

10. **FLAG_LIST_PATH**
   - flag_listのパスです。botにより異なるリストを設定するときに使用します。環境変数を設定しない場合、setting.iniを参照します。

11. **VOICE_LIST_PATH**
   - voice_listのパスです。botにより異なるリストを設定するときに使用します。環境変数を設定しない場合、setting.iniを参照します。
   
12. **WORD_LIST_PATH**
   - word_listのパスです。botにより異なるリストを設定するときに使用します。環境変数を設定しない場合、setting.iniを参照します。

13. **STYLE_SETTING_PATH**
   - style_settingのパスです。botにより異なるリストを設定するときに使用します。環境変数を設定しない場合、setting.iniを参照します。
   
14. **OTHER_VOICEVOX_APP**
   - その他VOICEVOX派生クライアントを使いたいときに入力します。カンマ区切りで複数クライアントを認識します。対応するOTHER_VOICEVOX_PORTを指定することが必須です。※利用先の利用規約を確認すること
   
15. **OTHER_VOICEVOX_PORT**
   - その他VOICEVOX派生クライアントを使いたいときに入力します。カンマ区切りで複数クライアントを認識します。対応するOTHER_VOICEVOX_APPを入力することが必須です。※利用先の利用規約を確認すること

16. **ALLOW_GUILDID**
   - コンマ区切りで複数設定できます。指定したサーバーID(GUILDID)以外でのjoinを無効化します。

## 注意

1. このソフトはWindows10・11上で使われることを想定しています。LinuxやMacで使う場合はshファイルまわりと音声のopus変換まわりをいじれば多分なんとかなります。
2. Pythonほぼ触ったことない + Discord bot作るの初めてで不慣れなところがあり一部コードが汚いかもしれないです。ごめんなさい。
3. 以前のバージョンのデータを引き継ぎたい場合は**データの引き継ぎ方.txt**をご覧ください
4. 同一ネットワーク内の他コンテナでportsをせずにVOICEVOXを起動する場合はshファイルのhost.docker.internalをサービス名に変更してください。

## 導入が必要なソフト

このソフトを利用するために以下のソフト類のインストールが必要です。

1. Docker Engineのインストール
   [このサイト](https://docs.docker.com/engine/install/)を参考にしてください。
   
2. VOICEVOXのインストール
   [このサイト](https://voicevox.hiroshiba.jp/)から最新版をダウンロードしてください。


## 起動方法


1. 上の導入が必要なソフトをすべてインストールします。

2. このフォルダ(yomiage_VOICEVOX_verT-Docker)をわかりやすい場所に置きます。

3. DiscordのBotを作成し、招待します。（すでにチャットルームにBotを招待している場合は省略）[このサイト](https://note.com/exteoi/n/nf1c37cb26c41)の**1. Discord上のBotの作成**にある記述を参考にしてください。

   1. https://discord.com/developers/applications を開きます。
   2. 右上にあるNew Applicationを押す。適当な名前を入れてCreateを押します。
   3. 管理画面が開かれる。左のメニューのBotを押し、Add Botを押す。→Yes, do it!を選択（開かれない場合はDeveloper Portalから作成したアプリケーションを選択する）
   4. するとBuild-A-Botのところになんか出てくる。そのTOKENのところにあるCopyを押すとBotのTOKENがコピーできる。**のちに必要となるので保存しておく。**
   5. **そのしたのPUBLIC BOT, REQUIRES OAUTH2 CODE GRANTをオフ、Presence Intent, Server Members Intent, MESSAGE CONTENT INTENTという項目をオンにする。(灰色がオフ、青色がオン）**
   6. 左のメニューのOAuth2→URL Generatorを開きます。 SCOPESでbotにチェックを入れます。
   7. BOT PERMISSIONSという項目が出てくると思うのでRead Messages/ViewChannels, Send Messages, Connect, Speakにチェックを入れてください。
   8. 一番下にあるGENERATED URLにあるリンクを開くとサーバー招待画面が出てくるので、追加したいサーバーを選択して認証します 。

3. アクセストークンを設定する（すでに設定していたら省略）

   docker-compose.ymlをテキストエディタで開いて、3-4)でenvironment:TOKEN:にコピーしていたTOKENを保存してください。

4. VOICEVOXを起動します。

5. コマンドプロンプトを起動します。 (Win+Rで"ファイル名を指定して実行"を開いて"cmd"を打ち込んだら出てくると思います）

6. チェンジディレクトリでこのフォルダの中身まで移動します。
   cd ディレクトリ名で移動できます。（https://eng-entrance.com/windows-command-cd を参照）例えば以下のようにする。

   ```bash
   $ cd C:\discord_bot\yomiage_VOICEVOX_verT-Docker
   ```

7. コマンドプロンプトに以下を打ち込み、実行します。

   ```bash
   $ docker-compose up --build
   ```

8. おつかれさまでした。

## 使用方法

1. Botを参加させたいボイスチャンネルに入室しておきます。
2. 読み上げ対象にしたいテキストチャンネル上で"!join"と打ち込みます。

## 終了方法

1. "!leave"でボイスチャンネルからBOTを退場させておきます
2. コマンドプロンプト上で"ctrl + C"をおこなって終了させます

## エラーが出た時

- アクセスが拒否されました

  ウイルスセキュリティソフトに引っかかっている可能性がある。許可する。

- Bot TOKENが設定されていません

  設定して下さい。[**起動方法4)**を参照]

- Discord BotのPrivileged Intents が有効になっていません云々のメッセージ

  BOTの設定に問題があるので確認する [**起動方法2-5)**を参照]

## 前バージョンからの引き継ぎ方法

前バージョンのyomiage_VOICEVOXのうち

1. data
2. SE
3. SE_list.csv

の3つをこのファイルに上書き保存する。

## SEの追加方法

例)dededeに音声を追加したい場合

1. wavファイルを用意する
2. dedede.wavという名前にして,SEフォルダの中に入れる
3. SE_list.csvをひらき（メモ帳で開ける）, 一番下にdededeを追加する。

## その他

1. ほかのBOTとコマンドが被ってしまっている場合はdocker-compose.ymlのenvironment:からCOMMAND_SYNTHAX、OTHER_BOTS_SYNTHAXの中身を適当に変更してください。
2. このBOTは改変版です。バグ報告や機能要望等は[改変者のTwitter](https://twitter.com/Richinosan)等にお願いします。


## 利用規約的なやつ

1. 本ソフトはオープンソースです。お金を払いたい場合はVOICEVOX様にどうぞ

   [VOICEVOX支援先](https://hiho.fanbox.cc/)

2. ソースコードの改変はご自由にどうぞ。
   ただし、改変したものを配布する場合は改変したことが分かるようにファイル名を変更して、更新履歴に変更点を追記してください。

3. VOICEVOX及び各キャラの利用規約をよく読んでから使用してください。<br>
   [VOICEVOX HP](https://voicevox.hiroshiba.jp/) <br>
   [COEIROINK HP](https://coeiroink.com/) <br>
   [LMROID HP](https://lmroidsoftware.wixsite.com/nhoshio) <br>
   [SHAREVOX HP](https://www.sharevox.app/) <br>
   [東北ずん子利用の手引き](https://zunko.jp/guideline.html)<br>
   
4. 本ソフトウェアにより生じた損害・不利益について、製作者は一切の責任を負いません。

5. 改善して欲しい点などあれば言ってください。
   ある程度リクエストは受け付けたいと思っていますが、製作者に技術がないのであまり期待しないでください。

6. 何かあればTwitterかDiscordまで<br>
   Twitter: @Kamimiya_yade<br>Discord: https://discord.gg/CMrDukD8DZ

## 更新履歴

- 20211202(かみみや)

  とりあえず動くようになった

- 20211203(かみみや) 

  時報・入退室管理機能の追加

  チャットが混雑した時に読み上げがスタックする問題の解決

  イラスト動画投稿を知らせる機能の追加

  URLが貼られたときの処理を追加した

  添付ファイルがあるときの処理を追加した

  BOTが参加したチャンネル名を取得できるようにした

- 20211204(かみみや)    

  ソースコードを整理した

  設定ファイル（discordbot_setting.py）を作成した

  一時的に出力されるファイルをtmpフォルダに保存するようにした

  単語リストまわりの改善をおこなった

- 20211205(かみみや)

  !wlist_showでword_list.csvをdiscord上で表示すると文字化けしていたのでencoding=utf-8に変更した。

  voice_list.csvの更新がうまくできていなかったので修正した

  読み上げ文字数制限を加えた

  command_list.txtの内容を修正した

- 20211206(かみみや)

  readme.mdの更新。(機能紹介とかなしみ欄を追加した）

  ボイスチャンネルの接続人数の確認

  ボイスチャンネルから人がいなくなったら自動!leaveするようにした

  名前読み上げモードを実装した

  word_listについて, キーの文字列長さ順にソートするようにした。

- 20211207(かみみや)

  文字数制限を超えた時、（文字数制限までのセリフ）＋（超えました）で返すようにする

  再生時間に対する制限も加えた。

  音声再生中もコマンドに反応できるようにした

- 20211208(かみみや)

  exeファイル化に成功した。

  TOKENの指定方法を変えた。

  各種設定について、変更が保存されるようにした。

  SEが再生できるようになった。

- 20211211(かみみや)

  すこしコードの整理をした。

  メッセージ付きで添付ファイルを送った際にメッセージが読み上げられるようにした。

  改行が入ったメッセージをちゃんと読み上げられるようにした。

- 20211214(かみみや)

  自分以外のbotのメッセージを読み上げないようにした。

  SE付きのメッセージについて、読みを改善した

  素材置き場に素材が置かれた時にメッセージを出すようにした。

  ソースコードの整理を行った。

  TOKENの設定をTOKEN.txtから行うようにした。

- 20211231(かみみや)

  readmeをhtml化した。
  雨晴はうのボイスを使えるようにした
  現在入室しているチャンネルの名前をステータス上に表示するようにした
  コードブロック、スポイラーを読み飛ばすようにした
  メンション付きメッセージも読むようにした

- 20220130(かみみや)

  コード内容の刷新
  使用ライブラリをpycordに変えた。
  !helpコマンドの挙動を変えた。
  ミュート機能を削除した。
  
- 20220313(かみみや)

  read_nameが機能しない問題を解決
  
  0.11.1で追加されたボイスを使えるようにした

- 20220315(かみみや)

  BOTの入退室通知機能について、誤って名前が同じボイスルームの入退出情報を知らせてしまう問題を解決

- 20220416(かみみや)

  テキストチャットの情報管理をチャンネル名ではなくチャンネルidで管理するように変更
  
- 20220611(かみみや)

  0.12.3までのボイスを追加
  
  使用ライブラリをdiscord.pyに戻した。
  
  #部屋名、@名前を読み上げるようにした
  
  BOT待機時ステータス画面に'待機中をプレイ中'と表示されるようにした。
  
- 20220628(かみみや)

  botが入室しているボイスチャンネル名の表示のオンオフを切り替えられるようにした

- 20220902(かみみや)

  単語数制限が反映されない問題を解決
  
  ボイス（剣崎）を使用可にした
  
- 20220923(タクト)

  話者を動的に取得するようにした

  voice_list.csvの様式が変更になった(前バージョンのものは初回起動時に現在の様式に更新されます)

  COEIROINK、LMROID、SHAREVOXに対応した

- 20220924(タクト)

  スタイル毎に話速・音高・抑揚・音量を持てるようにした

- 20221002(タクト)

  設定ファイルの名称変更

  各種リストのロケーションを設定ファイル側で持つようにした（同一サーバーで複数のbotを運営する用）

  word_list.csvの更新時に余計な空行が発生しないようにした

- 20221019(Richinosan)

   docker-composeに対応
