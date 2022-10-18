import os
import json
from abc import ABCMeta, abstractmethod
from for_developer.discordbot_setting import *
from for_developer.voice_speaker import AbstractVoiceSpeaker, VoiceVoxVoiceSpeaker

class AbstractVoiceGenerator(metaclass=ABCMeta):
    @abstractmethod
    def generate(self, character_name:str, style_name:str, query:str, speed:float):
        raise NotImplementedError()

    @abstractmethod
    def getSpeakersStr(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def hasSpeaker(self, name) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def getSpeaker(self, name) -> AbstractVoiceSpeaker:
        raise NotImplementedError
    
    @abstractmethod
    def hasStyle(self, speaker_name, style_name) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def getName(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def getSpeakersDict(self) -> dict:
        raise NotImplementedError
    
class VoiceVoxVoiceGenerator(AbstractVoiceGenerator):
    def __init__(self, name:str, port:str):
        # インスタンス変数の指定
        self.name = name
        self.port = port
        self.speakers = {}

        try:
            # VOICEVOX（あるいは互換ソフト）から、話者の一覧をJsonで取得する
            command = bat_speakers + ' ' + port
            os.system(command)

            #Jsonを解析して話者の情報を動的に取得する
            print("Jsonの解析開始")
            with open('tmp/speakers.json', 'r', encoding="utf-8_sig") as json_open:
                json_load = json.load(json_open)
                for speaker in json_load:
                    speaker_name = speaker['name']
                    speaker_styles = speaker['styles']
                    style_dict = {}

                    for style in speaker_styles:
                        style_dict[style['name']] = int(style['id'])
                    self.speakers[speaker_name] = VoiceVoxVoiceSpeaker(speaker_name, style_dict)

            print("Jsonの解析完了")
            print(self.getSpeakersStr())
        except Exception as e:
            raise e
            
    def generate(self, character_name:str, style_name:str, query:str, parameter:dict):
        # コマンドの設定
        style_id_str = str(self.speakers[character_name].getStyleId(style_name))
        command1 = bat_json + ' ' + self.port + ' ' + query + ' ' + style_id_str
        command2 = bat_voice + ' ' + self.port + ' ' + style_id_str

        # リクエスト用Jsonの生成
        os.system(command1)

        # jsonファイルのかきかえ
        with open(json_file, encoding="utf-8") as f:
            data_lines = f.read()
            data_lines = data_lines.replace('"speedScale":1.0'     , '"speedScale":'     +str(parameter["speed"]))
            data_lines = data_lines.replace('"pitchScale":0.0'     , '"pitchScale":'     +str(parameter["pitch"]))
            data_lines = data_lines.replace('"intonationScale":1.0', '"intonationScale":'+str(parameter["intonation"]))
            data_lines = data_lines.replace('"volumeScale":1.0'    , '"volumeScale":'    +str(parameter["volume"]))
        # 同じファイル名で保存
        with open(json_file, mode="w", encoding="utf-8") as f:
            f.write(data_lines)

        # wavファイルの生成
        os.system(command2)
    
    def getSpeakersStr(self) -> str:
        ret = "【" + self.name + "】\n"
        
        for speaker_name in self.speakers:
            ret += self.speakers[speaker_name].getStylesStr() + "\n"
        
        return ret
    
    def hasSpeaker(self, name) -> bool:
        if name in self.speakers.keys():
            return True
        else:
            return False
    
    def getSpeaker(self, name) -> VoiceVoxVoiceSpeaker:
        return self.speakers[name]
    
    def hasStyle(self, speaker_name, style_name) -> bool:
        if self.hasSpeaker(speaker_name):
            speaker = self.speakers[speaker_name]
            if speaker.hasStyle(style_name):
                return True
        
        return False
    
    def getName(self) -> str:
        return self.name
    
    def getSpeakerWithStyleId(self, id:int) -> VoiceVoxVoiceSpeaker:
        for speaker in self.speakers.values():
            if speaker.hasStyleId(id):
                return speaker
        return None
    
    def getSpeakersDict(self) -> dict:
        return self.speakers