'''
Created on Oct 27, 2010

@author: Patrick
'''

from STOLog import *

def createMeters(log):
    dm = DamageMeters(log)
            
    return dm

class DamageEntry:
    def __init__(self, displayName, internalId):
        self.displayName = displayName
        self.internalName = internalId
        self.damage = 0
        self.baseDamage = 0
        self.count = 0
        '''TODO: other flags(critical, overkill, etc)'''
        self.highest = 0
        self.lowest = 0
        
    def addDamage(self, damage, baseDamage):
        self.damage += float(damage)
        self.baseDamage += float(baseDamage)
        self.count += 1
    

class ObjectEntry:
    def __init__(self, displayName, internalId, ownerId):
        self.displayName = displayName
        self.internalName = internalId
        self.ownerId = ownerId
        self.damage = {}
        
    def addDamage(self, displayEventName, internalEventName, damage, baseDamage):
        if internalEventName not in self.damage:
            self.damage[internalEventName] = DamageEntry(displayEventName, internalEventName)
            
        self.damage[internalEventName].addDamage(damage, baseDamage)
        
class CombatSession:
    def __init__(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime
        self.objects = {}
        
    def parseEntry(self, logEntry):
        objectInternalName = logEntry.getInternalSourceOrOwner()
        if objectInternalName not in self.objects:
            self.objects[objectInternalName] = ObjectEntry(logEntry.getDisplaySourceOrOwner(), objectInternalName, logEntry.ownerInternalName)
            
        currentObject = self.objects[objectInternalName]
        currentObject.addDamage(logEntry.eventDisplayName, logEntry.eventInternalName, logEntry.magnitude, logEntry.baseMagnitude)
        
        if logEntry.eventDisplayName == "":
            print("Empty displayNameEvent at " + str(logEntry.timestamp) + " internalNameEvent: " + logEntry.eventInternalName)

class DamageMeters:
    def __init__(self, log):
        self.sessions = []
        self.parseLog(log)
        
    def parseLog(self, log):
        for session in log.sessions:
            combatSession = CombatSession(session.startTime, session.endTime)
            
            for entry in log.logEntries[session.startIndex:session.endIndex+1]:
                combatSession.parseEntry(entry)
                
            
            self.sessions.append(combatSession)
        

        
    '''def parseEntry(self, logEntry):
        objectInternalName = logEntry.getInternalSourceOrOwner()
        if objectInternalName not in self.objects:
            self.objects[objectInternalName] = ObjectEntry(logEntry.getDisplaySourceOrOwner(), objectInternalName)
        
        currentObject = self.objects[objectInternalName]
        currentObject.addDamage(logEntry.displayNameEvent, logEntry.internalNameEvent, logEntry.magnitude, logEntry.baseMagnitude)
        
        if logEntry.displayNameEvent == "":
            print("Empty displayNameEvent at " + logEntry.timestamp + " internalNameEvent: " + logEntry.internalNameEvent)'''
            
        
            


    