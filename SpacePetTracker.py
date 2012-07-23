'''
Created on Nov 29, 2010

@author: Patrick
'''

import STOLog
import time
import datetime
import os

trackedPetInternalNames = ['Space_Klingon_Raider_Player_Pet', 'Space_Klingon_Raider_Player_Pet_2', 'Space_Klingon_Fighter_Player_Pet', 'Space_Klingon_Raider_Player_Pet_2', 'Orion_Playership_Fighter_Pet_Slaver', 'Orion_Playership_Fighter_Pet_Slaver_2']
#trackedPetNames = {'Space_Klingon_Fighter_Player_Pet' : 'To\'Duj Fighter', 'Space_Klingon_Raider_Player_Pet' : 'Bird-of-Prey'}


def isTrackedPetName(internalName):
    for i in trackedPetInternalNames:
        isIn = internalName.find(i)
        if (isIn >= 0):
            return True
    
    return False

def isWarpCoreBreach(eventName):
    isIn = eventName.find("Warp Core Breach")
    if (isIn >= 0):
        return True
    
    return False

def getNumLinesInLog(filename):
    lineNum = 0
    fileHandle = open(filename, 'r')
    for line in fileHandle:
        lineNum += 1
    fileHandle.close()
    
    return lineNum

def purgeLog(filename):
    os.remove(filename)

if __name__ == '__main__':
    print("Pet tracker initializing")
    lineNum = 0
    filename = "D:\\Program Files (x86)\\Steam\\steamapps\\common\\star trek online\\Star Trek Online\\Live\\logs\\GameClient\\Combatlog.log"
    #filename = "D:\Program Files (x86)\Steam\steamapps\common\star trek online\Star Trek Online\Live\logs\GameClient"
    playerName = "Torokokill@torokokill"
    internalName = ""
    activePetList = {}

    '''Get current log's linecount'''
    lineNum = getNumLinesInLog(filename)
    print("Combatlog currently has " + str(lineNum) + " lines")
    
    while True:
        #print(" Opening log, starting at line " + str(lineNum))
        stoLog = STOLog.STOLog(filename, lineNum)
        
        newEndLine = len(stoLog.logEntries)
        #print(" Number of lines read: " + str(newEndLine))
        lineNum += newEndLine

        
        for entry in stoLog.logEntries:
            #Traditional entry as pet as source
            if (entry.ownerInternalName == playerName):
                if (isTrackedPetName(entry.sourceInternalName)):
                    idStr = entry.sourceInternalId + "|" + entry.sourceDisplayName
                    if idStr not in activePetList:
                        print(" New pet: " + entry.sourceDisplayName + " " + entry.sourceInternalId)
                        activePetList[idStr] = entry.timestamp 
            
            
            idStr = entry.targetInternalId + "|" + entry.targetDisplayName
            if idStr in activePetList:
                if (entry.flagExists("Kill")):
                    #Pet killed, removing it from the list
                    print("Killed pet: " + entry.targetDisplayName + " " + entry.targetInternalId)
                    del activePetList[idStr]
                else:
                    activePetList[idStr] = entry.timestamp
            
            #Fix for Season 6 bugs @todo: remove when fix goes live        
            idStr = entry.ownerInternalId + "|" + entry.ownerDisplayName
            if idStr in activePetList:
                activePetList[idStr] = entry.timestamp
            
            
            ''' if (entry.ownerInternalName == playerName):
                #TODO: Check if source is empty
                if (isTrackedPetName(entry.sourceInternalName)):
                    idStr = entry.sourceInternalId + "|" + entry.sourceDisplayName
                    if idStr not in activePetList:
                        print(" New pet: " + entry.sourceDisplayName + " " + entry.sourceInternalId)
                        activePetList[idStr] = entry.timestamp 
                        #Warp core breach and incoming damage
                    if (isWarpCoreBreach(entry.eventDisplayName)):
                        print(" " + entry.sourceInternalName + " " + entry.eventDisplayName + " " + entry.eventInternalName)
                        del activePetList[idStr]'''
        
        '''Clean up old entries'''                
        now = datetime.datetime.now()
        expiry = datetime.timedelta(seconds = 45)
        for petKey in list(activePetList.keys()):
            if now > activePetList[petKey] + expiry:
                print(" " + petKey + " has expired")
                del activePetList[petKey]
        
        '''Display new pet count'''
        collatedPets = {}
        for petKey in iter(activePetList):
            petSplit = str(petKey).split("|")
            if petSplit[1] not in collatedPets:
                collatedPets[petSplit[1]] = 1
            else:
                collatedPets[petSplit[1]] += 1
            
        '''Print collated pet counts'''
        for pet, count in collatedPets.items():
            print(pet + " x" + str(count))
        
        time.sleep(10)
        