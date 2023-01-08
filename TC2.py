#coding: utf-8

import requests as rq
from enum import Enum
import random

class EVENT_CAT(Enum):
    RACE = 0
    SKILL = 1

class VCAT(Enum):
    GROUND='4163869653'

class API_URLs(Enum):
    GAMEDATA_BASE="https://api.thecrew-hub.com/v1/data/game?fields"
    EVENTS=f"{GAMEDATA_BASE}=missions,skills"
    BRANDS=f"{GAMEDATA_BASE}=brands"
    VEHICLES=f"{GAMEDATA_BASE}=models"
    FAMILIES=f"{GAMEDATA_BASE}=families"
    DISCIPLINES=f"{GAMEDATA_BASE}=disciplines"
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

class Discipline:
    def __init__(self,jsonDict : dict) -> None:
        self.id = jsonDict["id"]
        self.name = jsonDict["text_id"]
        self.family = jsonDict["family"]
        self.img_path = jsonDict["img_path"]
    
    def __repr__(self) -> str:
        return f"<Discipline({self.id},{self.name},{self.family},{self.img_path})>"

class Event:
    def __init__(self,type : EVENT_CAT,jsonDict : dict) -> None:
        self.type = type
        self.id = jsonDict["id"]
        self.name = jsonDict["text_id"]
        self.discipline = None

        if "discipline" in jsonDict.keys():
            self.discipline = jsonDict["discipline"]
    
    def mapDiscipline(self,disciplineList : dict[str,Discipline]):
        if self.discipline in disciplineList.keys():
            self.discipline = disciplineList[self.discipline]

#Pull data from network only if needed (not initialized)
class TCData_t:
    def __init__(self) -> None:
        self.__disciplines = None
        self.__disciplinesNameMap = None
        self.__events = None
        self.__brands = None
        self.__families = None
        self.__vehicles = None
        self.__texts = None
        self.__summitInf = None
    
    def disciplines(self)->dict[str,Discipline]:
        if self.__disciplines != None:
            return self.__disciplines
        self.__disciplines = getDisciplines(self.texts())
        
        #mapping correct discipline name
        oldToNew = {
            "HYPERCAR" : "HC",
            "DRIFT" : "DF",
            "STREET RACE":"SR",
            "DRAG RACE":"DG",
            "ALPHA GRAND PRIX":"AGP",
            "AEROBATICS" : "AB",
            "JETSPRINT" : "JS",
            "MONSTER TRUCK" : "MT",
            "DEMOLITION DERBY" : "DD",
            "RALLY RAID" : "RR",
            "MOTOCROSS" : "MC",
            "RALLY CROSS" : "RC",
            "HOVERCRAFT" : "HT",
            "POWERBOAT" : "PB",
            "TOURING CAR" : "TC",
            "AIR RACE" : "AR"
        }
        for k in self.__disciplines.values():
            if k.name in oldToNew.keys():
                k.name = oldToNew[k.name]
        return self.__disciplines
        # raise Exception("disciplines are not yet implemented")
    
    def disciplinesNameMap(self)->dict[str,Discipline]:
        if self.__disciplinesNameMap != None:
            return self.__disciplinesNameMap
        dDict = self.disciplines()
        self.__disciplinesNameMap = {}
        for e in dDict.values():
            self.__disciplinesNameMap[e.name] = e
        return self.__disciplinesNameMap
    
    def events(self):
        if self.__events != None:
            return self.__events
        # raise Exception("Events are not yet implemented")
        eDict = getEvents(self.texts())
        self.__events = eDict
        dDict = self.disciplines()
        for e in eDict.values():
            e.mapDiscipline(dDict)
        return eDict

    
    def brands(self)->dict[str,Brand]:
        if self.__brands != None:
            return self.__brands
        self.__brands = getBrands(self.texts())
        return self.__brands

    def families(self)->dict[str,str]:#id : text_id
        if self.__families != None:
            return self.__families
        self.__families = getFamilies(self.texts())
        return self.__families
    
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
        raise Exception("Events are not yet implemented")

def __defaultRandomFilter(v : Vehicle):
    return True

def getRandomV(data : TCData_t,filterFunc : callable = __defaultRandomFilter) -> Vehicle:
    vList = data.vehicles()
    tmpList = []
    vcatList = {}
    for a in vList.values():
        vcatList[a.vcat] = a.name
        if filterFunc(a):
            tmpList.append(a)
    print(vcatList)
    return random.choice(tmpList)


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
            return texts[jsonElement].replace("#","").replace("&8209;","-")
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

def getFamilies(texts : dict)->dict[str,str]:
    tmp = __getJsonFromUrl(API_URLs.FAMILIES.value)["families"]
    __mapTexts(tmp,texts)
    out = {}
    for e in tmp:
        out[e["id"]] = e["text_id"]
    return out
    
def getVehicles(texts : dict)->dict[str,Vehicle]:
    tmp = __getJsonFromUrl(API_URLs.VEHICLES.value)
    tmp = tmp["models"]
    __mapTexts(tmp,texts)
    out = {}
    for e in tmp:
        b = Vehicle(e)
        out[b.id] = b
    return out

def getDisciplines(texts : dict) -> dict[str,Discipline]:
    tmp = __getJsonFromUrl(API_URLs.DISCIPLINES.value)["disciplines"]
    __mapTexts(tmp, texts)

    out = {}
    for e in tmp:
        d = Discipline(e)
        out[d.id] = d
    return out

def getEvents(texts : dict)->dict[str,Event]:
    tmp = __getJsonFromUrl(API_URLs.EVENTS.value)
    missions = tmp["missions"]
    skills = tmp["skills"]
    __mapTexts(missions,texts)
    __mapTexts(skills,texts)

    out = {}
    for e in missions:
        b = Event(EVENT_CAT.RACE,e)
        out[b.id] = b
    for e in skills:
        b = Event(EVENT_CAT.SKILL,e)
        out[b.id] = b

    return out

    
def getSummitInf(texts : dict):
    tmp = __getJsonFromUrl(API_URLs.SUMMIT_INF.value)


if __name__ == "__main__":
    tcData = TCData_t()
    brands = tcData.brands()
    # for b in brands.values():
    #     print(b.name)
    vehicles = tcData.vehicles()
    # for v in vehicles.values():
    #     print(v)

    print(tcData.families())