#coding: utf-8

import requests as rq
from enum import Enum

class API_URLs(Enum):
    EVENTS="https://api.thecrew-hub.com/v1/data/game?fields=missions,skills"
    BRANDS="https://api.thecrew-hub.com/v1/data/game?fields=brands"
    VEHICLES="https://api.thecrew-hub.com/v1/data/game?fields=models"
    TEXTS="https://api.thecrew-hub.com/v1/data/locas/en.json"
    SUMMIT_INF="https://api.thecrew-hub.com/v1/data/summit"


class Brand:
    def __init__(self,jsonDict : dict) -> None:
        self.id = jsonDict["id"]
        self.name = jsonDict["text_id"] #we consider that the id has been mapped to the text beforehand
    
    def __repr__(self) -> str:
        return f"<Brand({self.id},{self.name})>"

class Vehicle:
    def __init__(self,jsonDict : dict) -> None:
        self.id = jsonDict["id"]
        self.name = jsonDict["text_id"]
        self.vcat = jsonDict["vcat"]
        self.brand = jsonDict["brand"]
    
    def mapBrand(self,brandList : dict[str,Brand]):
        if self.brand in brandList.keys():
            self.brand = brandList[self.brand]
    
    def __repr__(self) -> str:
        return f"<Vehicle({self.id},{self.name},{self.vcat},{self.brand})>"


#Pull data from network only if needed (not initialized)
class TCData_t:
    def __init__(self) -> None:
        self.__events = None
        self.__brands = None
        self.__vehicles = None
        self.__texts = None
        self.__summitInf = None
    
    def events(self):
        if self.__events != None:
            return self.__events
    
    def brands(self)->dict[str,Brand]:
        if self.__brands != None:
            return self.__brands
        self.__brands = getBrands(self.texts())
        return self.__brands
    
    def vehicles(self)->dict[str,Vehicle]:
        if self.__vehicles != None:
            return self.__vehicles
        vDict = getVehicles(self.texts())
        for v in vDict.values():
            v.mapBrand(self.brands())
        self.__vehicles = vDict
        return self.__vehicles
    
    def texts(self):
        if self.__texts != None:
            return self.__texts
        return getTexts()
    
    def summitInf(self):
        if self.__summitInf != None:
            return self.__summitInf


tcData = TCData_t()


#C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\games\The Crew 2\data_win32
# Get all game missions
# https://api.thecrew-hub.com/v1/data/game?fields=missions,skills
# Get all vehicles brands and models
# https://api.thecrew-hub.com/v1/data/game?fields=brands,models
# Get all texts ...
# https://api.thecrew-hub.com/v1/data/locas/en.json
# Get summit info
# https://api.thecrew-hub.com/v1/data/summit

def __checkResponse(json : dict) -> bool:
    if "statusCode" in json.keys() and json["statusCode"] != 200:
        print(f"Error when fetching resource : {json['error']} : {json['message']}")
        return False
    return True

def __getJsonFromUrl(url : str):
    req = rq.get(url)
    json = req.json()
    if not __checkResponse(json):
        return None
    return json


def __mapTexts(jsonElement,texts : dict):
    if type(jsonElement) is list:
        for e in jsonElement:
            e = __mapTexts(e,texts)
    elif type(jsonElement) is dict:
        for k in jsonElement.keys():
            jsonElement[k] = __mapTexts(jsonElement[k],texts)
    else:
        isAText = jsonElement in texts.keys()
        if isAText:
            return texts[jsonElement]
    return jsonElement



def getTexts():
    return __getJsonFromUrl(API_URLs.TEXTS.value)

#return dict["id",Brand]
def getBrands(texts : dict)->dict[str,Brand]:
    tmp = __getJsonFromUrl(API_URLs.BRANDS.value)["brands"]
    __mapTexts(tmp,texts)
    out = {}
    for e in tmp:
        b = Brand(e)
        out[b.id] = b
    return out
    
def getVehicles(texts : dict)->dict[str,Vehicle]:
    tmp = __getJsonFromUrl(API_URLs.VEHICLES.value)["models"]
    __mapTexts(tmp,texts)
    out = {}
    for e in tmp:
        b = Vehicle(e)
        out[b.id] = b
    return out
    
def getEvents(texts : dict):
    tmp = __getJsonFromUrl(API_URLs.EVENTS.value)
    
def getSummitInf(texts : dict):
    tmp = __getJsonFromUrl(API_URLs.SUMMIT_INF.value)


if __name__ == "__main__":
    brands = tcData.brands()
    # for b in brands.values():
    #     print(b.name)
    vehicles = tcData.vehicles()
    for v in vehicles.values():
        print(v)