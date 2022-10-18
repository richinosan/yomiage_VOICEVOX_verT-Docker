
# 設定ファイルの読み込み
from __future__ import generators
import discord
import os
import csv
import re
import asyncio
import queue
import sys
import traceback
import configparser
from for_developer.discordbot_setting import *
from for_developer.voice_generator import VoiceVoxVoiceGenerator

# 関数の定義
# 以下、引数のmessage_tmpはdiscord.message型を入れる。
# 非同期関数 (async関数) はawaitで呼び出すこと。

# 単語帳 (dict) を単語の長さ順にソートする
def sort_dict(dict):
    keys = sorted(dict.keys(), key=len, reverse=True)
    for k in keys:
        dict[k] = dict.pop(k)


# 単語帳 (dict) を単語の長さ順にソートして書き換える
def revise_dict(dict, file):
    # キーの文字長順でソートする
    sort_dict(dict)
    # word_list.csvを更新する
    with open(file, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        for k, v in dict.items():
            writer.writerow([k, v])


# 他の音源が再生されている間スリープする
async def already_playing_plz_sleep(message_tmp):
    while True:
        if message_tmp.guild.voice_client is None:
            break
        else:
            if message_tmp.guild.voice_client.is_playing():
                await asyncio.sleep(0.05)
            else:
                break

# データ書き込み
def output_data(filename, listname):
    with open(filename, 'w', encoding='utf-8') as f:  
        writer = csv.writer(f)
        for k, v in listname.items():
            writer.writerow([k, v])
    return

# チャンネル情報クラス
class room_information():
    def __init__(self, bot = None, TEXT_ROOM_ID=0, TEXT_ROOM_NAME='', VOICE_ROOM_ID=0, VOICE_ROOM_NAME='', GUILD_ID=0):
        self.bot = None
        self.game = discord.Game('待機中')
        self.text_room_id = TEXT_ROOM_ID
        self.text_room_name = TEXT_ROOM_NAME
        self.voice_room_id = VOICE_ROOM_ID
        self.voice_room_name = VOICE_ROOM_NAME
        self.guild_id = GUILD_ID
        # 各種ファイル
        self.vlist_file = ""            # ユーザ毎のボイスリスト
        self.flist_file = ""            # フラグリスト
        self.wlist_file = ""            # 単語帳リスト
        self.style_setting_file = ""    # スタイル別設定値ファイルのパス
        # 各種リスト
        self.generators = {}  # 使用するソフトウェアとその情報
        self.voice_dict = {}  # 使用ボイスの管理
        self.style_setting_dict = {} # スタイル別各種設定の管理
        self.word_dict = {}  # 単語帳の管理
        self.flag_valid_dict = {command_inform_someone_come: inform_someone_come, command_inform_tmp_room: inform_tmp_room,
                                command_time_signal: time_signal,
                                command_read_name: read_name, command_number_of_people: number_of_people,
                                command_auto_leave: auto_leave, 
                                command_word_count_limit: word_count_limit}
        self.image_list = {}  # 画像と呼び出しコマンドの管理
        # キュー処理用
        self.speaking_queue = queue.Queue()
        self.now_loading = False
        # ソフトごとの使用設定
        self.use_voicevox = False
        self.use_coeiroink = False
        self.use_lmroid = False
        self.use_sharevox = False
        # デフォルト値
        self.default_generator = ""
        self.default_speaker = ""
        self.default_style = ""

    def text_room_id_exist(self):
        if self.text_room_id == 0:
            return False
        else:
            return True

    # 人数カウント+自動退出
    async def count_number_of_people(self, text_channel, voice_channel):
        user_count = sum(1 for member in voice_channel.members if not member.bot)
        await text_channel.send('>現在' + str(user_count) + '人接続しているのだ')
        if(user_count == 0 and self.flag_valid_dict[command_auto_leave]):
            await text_channel.send('>誰もいなくなったみたいだから僕もそろそろ抜けるのだ')
            await voice_channel.guild.voice_client.disconnect()
            # 切断に成功したことの報告
            print(self.voice_room_name + "から切断しました")
            # チャンネル情報を初期化
            self.text_room_name = ''
            self.text_room_id = 0
            self.voice_room_name = ''
            self.voice_room_id = 0
            self.guild_id = 0

    # sentenceで得たメッセージをVOICEVOXで音声ファイルに変換しそれを再生する
    def play_voice(self, sentence, message_tmp):
        # チャットの内容をutf-8でエンコードする
        text = sentence.encode('utf-8')

        # HTTP POSTで投げられるように形式を変える
        arg = ''
        for item in text:
            arg += '%'
            arg += hex(item)[2:].upper()

        # batファイルを呼び起こしてwavファイルを作成する
        try:
            if message_tmp.author.id in self.voice_dict.keys():
                voice_data = self.voice_dict.get(message_tmp.author.id)
                parameter_dict = self.style_setting_dict[(voice_data[1], voice_data[2])]
                self.generators[voice_data[0]].generate(voice_data[1], voice_data[2], arg, parameter_dict)
            else:
                parameter_dict = self.style_setting_dict[(self.default_speaker, self.default_style)]
                self.generators[self.default_generator].generate(self.default_speaker, self.default_style, arg, parameter_dict)
        except Exception as e:
            print(type(e))
            traceback.print_exc()
        
        # wavの再生
        # ffmpegがインストールされていない場合エラーを出す。
        try:
            tmp = discord.FFmpegOpusAudio(voice_file)
        except discord.errors.ClientException:
            print(" ")
            print(" ")
            print("[エラーメッセージ(by かみみや)]")
            print("ffmpegがインストールされていないです（またはPathが通っていないです）")
            print("そのため、音声再生ができません。")
            print("詳しくはreadmeの導入が必要なソフト1.をご覧ください")
            print(" ")
            print(" ")
        
        try:
            tmp = discord.FFmpegOpusAudio(voice_file)
            message_tmp.guild.voice_client.play(tmp)
        except:
            print("再生時エラー")
        return

    # 他の読み込み処理が行われている間スリープする
    async def already_loading_plz_sleep(self):
        while True:
            if self.now_loading:
                await asyncio.sleep(0.05)  
            else:       
                break 

    # 投げられたメッセージの辞書置換から再生までまとめた関数
    async def plz_speak(self, sentence, message_tmp):
        # 読み上げ制限
        if len(sentence) > int(self.flag_valid_dict[command_word_count_limit]):
            sentence = sentence[0:int(self.flag_valid_dict[command_word_count_limit]) - 1] + "以下略"
            
        # 音声の再生
        for item in re.split('\n|;', sentence):
            # word_dictに含まれる場合は置換する
            for key in self.word_dict.keys():
                item = item.replace(key, self.word_dict[key])
            # 他の音源が再生されている間スリープする
            await already_playing_plz_sleep(message_tmp)
            
            if ('http' in item) or ('https' in item):
                self.play_voice("URLが貼られたのだ", message_tmp)  # 音声の再生
            else:
                self.play_voice(item, message_tmp)  # 音声の再生

    # キューに投げ込まれた文章を逐次再生する
    async def queuing(self, message_tmp):
        while not self.speaking_queue.empty():
            item = self.speaking_queue.get()
            await self.plz_speak(item, message_tmp)
            
    # キューを初期化する
    def queue_clear(self):
        while not self.speaking_queue.empty():
            self.speaking_queue.get()
            self.now_loading = False

    async def reload(self):        
        # setting.iniの読み込み
        ini = configparser.ConfigParser()
        ini.read('./setting.ini', 'UTF-8')
        self.use_voicevox = True if ini.get('Using Setting', 'UseVOICEVOX') == 'True' else False
        self.use_coeiroink = True if ini.get('Using Setting', 'UseCOEIROINK') == 'True' else False
        self.use_lmroid = True if ini.get('Using Setting', 'UseLMROID') == 'True' else False
        self.use_sharevox = True if ini.get('Using Setting', 'UseSHAREVOX') == 'True' else False
        self.default_generator = ini.get('Default Value Setting', 'DefaultGenerator')
        self.default_speaker = ini.get('Default Value Setting', 'DefaultSpeaker')
        self.default_style = ini.get('Default Value Setting', 'DefaultStyle')
        self.vlist_file = ini.get('Data Location', 'VoiceList')
        self.flist_file = ini.get('Data Location', 'FlagList')
        self.wlist_file = ini.get('Data Location', 'WordList')
        self.style_setting_file = ini.get('Data Location', 'StyleSetting')

        # ソフトウェア情報の読み込み
        self.generators = {}
        if self.use_voicevox:
            self.createVoiceVoxGenerator('VOICEVOX', '50021')
        if self.use_coeiroink:
            self.createVoiceVoxGenerator('COEIROINK', '50031')
        if self.use_lmroid:
            self.createVoiceVoxGenerator('LMROID', '50073')
        if self.use_sharevox:
            self.createVoiceVoxGenerator('SHAREVOX', '50025')
        
        if not any(self.generators):
            print("音声合成ソフトウェアの初期化に失敗しました。プログラムを終了します。")
            sys.exit(1)

        # スタイルごとの情報の読み取り
        # TODO そのうちスタイル別にオブジェクトを持たせ、ここでは管理しないようにする
        with open(self.style_setting_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row or row[0] == 'name':
                    continue
                
                parameter_dict = {}
                parameter_dict['speed'] = float(row[2])
                parameter_dict['pitch'] = float(row[3])
                parameter_dict['intonation'] = float(row[4])
                parameter_dict['volume'] = float(row[5])
                self.style_setting_dict[(row[0], row[1])] = parameter_dict
            
        for generator in self.generators.values():
            for speaker in generator.getSpeakersDict().values():
                for style_name in speaker.getStylesDict().keys():
                    if not (speaker.getName(), style_name) in self.style_setting_dict.keys():
                        parameter_dict = {}
                        parameter_dict['speed'] = 1.2
                        parameter_dict['pitch'] = 0.0
                        parameter_dict['intonation'] = 1.0
                        parameter_dict['volume'] = 1.0
                        self.style_setting_dict[(speaker.getName(), style_name)] = parameter_dict

        self.writeStyleSettingDict()

        # voice_dict情報を読み込む
        with open(self.vlist_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue

                if len(row) == 2:
                    # voice_dictの行の要素数が2、つまりかみみやさんのバージョンの場合
                    # デフォルトソフトウェアの話者のIDから、話者名とスタイル名を取得する
                    # 見つからなかった場合や例外が発生した場合はデフォルト話者を設定しておく
                    try:
                        speaker_with_id = self.generators[self.default_generator].getSpeakerWithStyleId(int(row[1]))
                        if not speaker_with_id is None:
                            self.voice_dict[int(row[0])] = [self.default_generator, speaker_with_id.getName(), speaker_with_id.getStyleNameWithId(int(row[1]))]
                        else:
                            self.voice_dict[int(row[0])] = [self.default_generator, self.default_speaker, self.default_style]
                    except Exception as e:
                        print(type(e))
                        traceback.print_exc()
                        self.voice_dict[int(row[0])] = [self.default_generator, self.default_speaker, self.default_style]
                elif len(row) == 4:
                    self.voice_dict[int(row[0])] = [row[1], row[2], row[3]]
                else:
                    continue
        self.writeVoiceDict()

        # word_dict情報を読み込む
        with open(self.wlist_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                self.word_dict[row[0]] = row[1]
        # flag_list情報を読み込む
        with open(self.flist_file,'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue  # rowが空の場合はスキップ
                if row[0] in self.flag_valid_dict.keys(): # 設定項目がflag_valid_dictに含まれる場合
                    if row[1] == 'True':
                        self.flag_valid_dict[row[0]] = True
                    elif row[1] == 'False':
                        self.flag_valid_dict[row[0]] = False
                    else:
                        self.flag_valid_dict[row[0]] = float(row[1])
            f.close()
            
        print('更新完了')
    
    # VOICEVOXとその派生ソフトウェアのオブジェクトを作成して返す
    # エラー時にgeneratorsにオブジェクトを格納させないためのコンストラクタのラッパ
    def createVoiceVoxGenerator(self, name:str, port:str):
        try:
            tmpVVGenerator = VoiceVoxVoiceGenerator(name, port)
            self.generators[name] = tmpVVGenerator
        except Exception as e:
            print(name + "の初期化に失敗しました。")
            print(name + "が起動されていない可能性があります。")
            print(type(e))
            traceback.print_exc()

    # コマンドを実行する
    async def execute_commands(self, message_tmp):
        # ボイスチャンネルに接続
        if message_tmp.content == command_join:
            # message_tmpの送信者がいるボイスチャンネルに接続
            await message_tmp.author.voice.channel.connect()
            # 接続先のチャンネル情報を記録
            self.text_room_name = str(message_tmp.channel)
            self.text_room_id = int(message_tmp.channel.id)
            self.voice_room_name = str(message_tmp.author.voice.channel)
            self.voice_room_id = int(message_tmp.author.voice.channel.id)
            self.guild_id = message_tmp.guild.id
            # statusの更新
            self.game = discord.Game(self.voice_room_name)
            if self.flag_valid_dict[command_inform_tmp_room]:
                await self.bot.change_presence(status=None, activity=self.game)
            # 接続に成功したことの報告
            print(self.voice_room_name + "に接続しました")
            await message_tmp.channel.send(comment_dict['message_join'])

        # ボイスチャンネルから切断
        elif message_tmp.content == command_leave:
            # statusの初期化
            self.game = discord.Game("待機中")
            if self.flag_valid_dict[command_inform_tmp_room]:
                await self.bot.change_presence(status=None, activity=self.game)
            # ボイスチャンネルから切断
            await message_tmp.guild.voice_client.disconnect()
            # 切断に成功したことの報告
            print(self.voice_room_name + "から切断しました")
            await message_tmp.channel.send(comment_dict['message_leave'])
            # チャンネル情報を初期化
            self.text_room_name = ''
            self.text_room_id = 0
            self.voice_room_name = ''
            self.voice_room_id = 0
            self.guild_id = 0
            
        # helpコマンド
        elif message_tmp.content == command_help:
            await message_tmp.channel.send(help_message)
        elif message_tmp.content == command_hello:
            await message_tmp.channel.send(version_info)
        
        # ボイスの変更
        elif message_tmp.content.startswith(command_chg_my_voice):
            voice_tmp = message_tmp.content.split()
            if len(voice_tmp) == 3:
                # generatorsを前から順番に探す
                for generator in self.generators.values():
                    if generator.hasStyle(voice_tmp[1], voice_tmp[2]):
                        self.voice_dict[message_tmp.author.id] = [generator.getName(), voice_tmp[1], voice_tmp[2]]
                        await message_tmp.channel.send(comment_dict['message_chg_voice'])
                        self.writeVoiceDict()
                        return
                await message_tmp.channel.send(comment_dict['message_not_actualized'] + "\n" + comment_dict['message_prompt_command'])
            elif len(voice_tmp) == 4:
                # ソフト名を指定して対応するボイスを探す
                if voice_tmp[3] in self.generators.keys():
                    generator = self.generators[voice_tmp[3]]
                    if generator.hasStyle(voice_tmp[1], voice_tmp[2]):
                        self.voice_dict[message_tmp.author.id] = [generator.getName(), voice_tmp[1], voice_tmp[2]]
                        await message_tmp.channel.send(comment_dict['message_chg_voice'])
                        self.writeVoiceDict()
                    else:
                        await message_tmp.channel.send(comment_dict['message_not_actualized_in_software'] + "\n" + comment_dict['message_prompt_command'])
                else:
                    await message_tmp.channel.send(comment_dict['message_invalid_software'] + "\n" + comment_dict['message_prompt_command'])
            else:
                await message_tmp.channel.send(comment_dict['message_err'])

        # ワードリストの追加
        elif message_tmp.content.startswith(command_wlist):
            wlist_tmp = message_tmp.content.split()
            if (len(wlist_tmp) == 4) and (wlist_tmp[1] == "add"):                # エラーチェック
                self.word_dict[wlist_tmp[2]] = wlist_tmp[3]
                await message_tmp.channel.send(comment_Synthax + wlist_tmp[2] + "を" + wlist_tmp[3] + "として追加しました")
                revise_dict(self.word_dict, self.wlist_file)
                return
            elif (len(wlist_tmp) == 3) and (wlist_tmp[1] == "delete"):           # エラーチェック
                self.word_dict.pop(wlist_tmp[2])
                await message_tmp.channel.send(comment_Synthax + wlist_tmp[2] + "を削除しました")
                revise_dict(self.word_dict, self.wlist_file)
                return
            elif (len(wlist_tmp) == 2) and (wlist_tmp[1] == "show"):             # エラーチェック
                await message_tmp.channel.send(file=discord.File(self.wlist_file))
                return
            else:  # 例外処理
                await message_tmp.channel.send(comment_dict['message_err'])
        
        # スタイル別の読み上げ時の値の設定
        elif message_tmp.content.startswith(command_chg_voice_setting):
            command_tmp = message_tmp.content.split()
            # 要素数エラー
            if len(command_tmp) != 5:
                await message_tmp.channel.send(comment_Synthax + command_chg_voice_setting + " 話者名 スタイル名 変更するパラメータ 変更後の値 と入力してください")
                await message_tmp.channel.send(comment_Synthax + "変更するパラメータには speed, pitch, intonation, volume が指定できます")
                return
            
            # スタイル情報辞書に話者とスタイルの組み合わせが存在しない場合エラー
            if not (command_tmp[1], command_tmp[2]) in self.style_setting_dict.keys():
                await message_tmp.channel.send(comment_Synthax + "指定された話者とスタイルの組み合わせが存在しません")
                return
            
            # 各種状態の変更
            try:
                value_tmp = '{:3}'.format(command_tmp[4])
                if command_tmp[3].lower() == 'speed':
                    if float(value_tmp) < 0.5 or 2.0 < float(value_tmp):
                        await message_tmp.channel.send(comment_Synthax + 'speedは0.5から2.0の範囲で指定してください')
                    else:
                        self.style_setting_dict[(command_tmp[1], command_tmp[2])]['speed'] = float(value_tmp)
                        await message_tmp.channel.send(comment_Synthax + command_tmp[1] + " " + command_tmp[2] + "の読み上げスピードを" + command_tmp[4] + 'に設定しました')
                        self.writeStyleSettingDict()
                elif command_tmp[3].lower() == 'pitch':
                    if float(value_tmp) < -0.15 or 0.15 < float(value_tmp):
                        await message_tmp.channel.send(comment_Synthax + 'pitchは-0.15から0.15の範囲で指定してください')
                    else:
                        self.style_setting_dict[(command_tmp[1], command_tmp[2])]['pitch'] = float(value_tmp)
                        await message_tmp.channel.send(comment_Synthax + command_tmp[1] + " " + command_tmp[2] + "の音高を" + command_tmp[4] + 'に設定しました')
                        self.writeStyleSettingDict()
                elif command_tmp[3].lower() == 'intonation':
                    if float(value_tmp) < 0.0 or 2.0 < float(value_tmp):
                        await message_tmp.channel.send(comment_Synthax + 'intonationは0.0から2.0の範囲で指定してください')
                    else:
                        self.style_setting_dict[(command_tmp[1], command_tmp[2])]['intonation'] = float(value_tmp)
                        await message_tmp.channel.send(comment_Synthax + command_tmp[1] + " " + command_tmp[2] + "の抑揚を" + command_tmp[4] + 'に設定しました')
                        self.writeStyleSettingDict()
                elif command_tmp[3].lower() == 'volume':
                    if float(value_tmp) < 0.0 or 2.0 < float(value_tmp):
                        await message_tmp.channel.send(comment_Synthax + 'volumeは0.0から2.0の範囲で指定してください')
                    else:
                        self.style_setting_dict[(command_tmp[1], command_tmp[2])]['volume'] = float(value_tmp)
                        await message_tmp.channel.send(comment_Synthax + command_tmp[1] + " " + command_tmp[2] + "の音量を" + command_tmp[4] + 'に設定しました')
                        self.writeStyleSettingDict()
                else:
                    await message_tmp.channel.send(comment_Synthax + "変更するパラメータには speed, pitch, intonation, volume を指定してください")

            except ValueError:
                await  message_tmp.channel.send(comment_dict['message_err'])

            return

        # 文字数制限の設定
        elif message_tmp.content.startswith(command_word_count_limit):
            command_tmp = message_tmp.content.split()
            # 要素数エラー
            if len(command_tmp) != 2:
                await message_tmp.channel.send(comment_dict['message_err'])
                return            
            # 2つめの要素がintでなければエラー
            try:
                self.flag_valid_dict[command_word_count_limit] = int(command_tmp[1])
                await message_tmp.channel.send(comment_Synthax + "文字数制限を"+command_tmp[1]+'に設定したのだ')            #設定の更新
                output_data(self.flist_file, self.flag_valid_dict)
            except ValueError:
                await message_tmp.channel.send(comment_dict['message_err'])
            return
            
        # 各種設定の変更
        elif message_tmp.content in self.flag_valid_dict.keys():
            self.flag_valid_dict[message_tmp.content] = not self.flag_valid_dict[message_tmp.content]
            await message_tmp.channel.send(comment_Synthax + flag_name_dict[message_tmp.content] + "を" + bool_name_dict[self.flag_valid_dict[message_tmp.content]] + "にしたのだ")
            #設定の更新
            output_data(self.flist_file, self.flag_valid_dict)
            # inform_tmp_roomの設定を反映させる
            if self.flag_valid_dict[command_inform_tmp_room]:
                await self.bot.change_presence(status=None, activity=self.game)
            else:
                await self.bot.change_presence(status=None, activity=None)
            
        # 現在の設定の確認
        elif message_tmp.content == command_show_setting:
            sentence = '```'
            for flag in self.flag_valid_dict.keys():
                if type(self.flag_valid_dict[flag]) == bool:
                    sentence = sentence + flag_name_dict[flag] + ';' + bool_name_dict[self.flag_valid_dict[flag]] + "\n"
                else:
                    sentence = sentence + flag_name_dict[flag] + ';' + str(self.flag_valid_dict[flag]) + "\n"
            sentence = sentence + '```'
            await message_tmp.channel.send(sentence)

        # 話者リストの表示
        elif message_tmp.content == command_show_speakers:
            sentence = '```'
            for generator in self.generators.values():
                sentence += generator.getSpeakersStr()
            sentence += '```'
            await message_tmp.channel.send(sentence)

        # 情報の再読み込み
        elif message_tmp.content == command_reload:
            await self.reload()
            
        # 例外処理
        else:
            await message_tmp.channel.send(comment_dict['message_err'])
    
    def writeVoiceDict(self):
        with open(self.vlist_file, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            for k, v in self.voice_dict.items():
                tmpList = v.copy()
                tmpList.insert(0, k)
                writer.writerow(tmpList)
    
    def writeStyleSettingDict(self):
        with open(self.style_setting_file, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['name', 'style', 'speed', 'pitch', 'intonation', 'volume'])
            for k, v in self.style_setting_dict.items():
                tmp_list = list(k)
                tmp_list += [str(v['speed']), str(v['pitch']), str(v['intonation']), str(v['volume'])]
                writer.writerow(tmp_list)