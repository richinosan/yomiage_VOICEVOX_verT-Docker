from abc import ABCMeta, abstractmethod

class AbstractVoiceSpeaker(metaclass=ABCMeta):
    @abstractmethod
    def hasStyle(self, style_name:str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def getStylesStr(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def getName(self) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def getStylesDict(self) -> dict:
        raise NotImplementedError

class VoiceVoxVoiceSpeaker(AbstractVoiceSpeaker):
    def __init__(self, name:str, styles:dict):
        self.name = name
        self.styles = styles

    def hasStyle(self, style_name:str) -> bool:
        if style_name in self.styles.keys() :
            return True
        else:
            return False
    
    def getStylesStr(self) -> str:
        ret = "[" + self.name + "]:"

        for oneKey in list(self.styles.keys()):
            ret += oneKey + ", "
        
        return ret[:-2]
    
    def getStyleId(self, style_name:str) -> int:
        return self.styles[style_name]
    
    def hasStyleId(self, style_id:int) -> bool:
        if style_id in self.styles.values() :
            return True
        else:
            return False
    
    def getName(self) -> str:
        return self.name
    
    def getStyleNameWithId(self, style_id:int) -> str:
        for k, v in self.styles.items():
            if style_id == v:
                return k
        
        return None
    
    def getStylesDict(self) -> dict:
        return self.styles