'''
Created on Oct 27, 2010

@author: Patrick
'''
import datetime

class STOLogEntry:
    
    def setTime(self, timeStr):
        ''' 10:11:05:12:46:42.3 '''
        self.timestamp = datetime.datetime.strptime(timeStr, "%y:%m:%d:%H:%M:%S.%f")
        
    '''
    Returns the internal name of the source of the damage
    '''
    def getInternalSourceOrOwner(self):
        if (self.isSourceOwner()):
            return self.ownerInternalId
        else:
            return self.sourceInternalId
    
    '''
    Returns the display name of the source of the damage
    '''
    def getDisplaySourceOrOwner(self):
        if (self.isSourceOwner()):
            return self.ownerDisplayName
        else:
            return self.sourceDisplayName
    
    '''
    Checks to see if the Source of the damage is also the Owner
    '''
    def isSourceOwner(self):
        if (self.sourceInternalId == "*"):
            return True
        else:
            return False
        
    '''
    Checks to see if a specific flag is in the flags
    '''
    def flagExists(self, flag):
        if (str.find(self.flags, flag) > -1):
            return True
        else:
            return False


class Session:
    def __init__(self, startTimeStr, startIndex):
        self.startTime = datetime.datetime.strptime(startTimeStr, "%y:%m:%d:%H:%M:%S.%f")
        self.startIndex = startIndex
        
    
    
class STOLog:
    '''
    A STOLog class is a single complete log file.
    Does all the parsing, collating and storage
    '''

    def __init__(self, filename, lineNum = 0):
        self.file = filename
        self.logEntries = []
        self.sessions = []
        self.startTime = datetime.datetime.now()
        self.parseFile(filename, lineNum)
        self.endTime = datetime.datetime.now()
        
        td = self.endTime - self.startTime
        print("Log parsed in " + str(td))
        
        
        
    def splitInternalName(self, lineIn):
        ret = []
        
        if (lineIn == '*') or (lineIn == ''):
            ret.append('*')
            ret.append('*')
            ret.append('*')
            return ret
       
        ret.append(lineIn[0])
        split = lineIn.split(' ')
        ret.append(split[0].lstrip('PSC['))
        if (len(ret) == 2):
            ret.append(split[1].rstrip(']'))
        else:
            ret.append("")
        
        return ret
        
    def parseFile(self, filename, lineNum = 0):
        import csv
        #import str 
        try:
            fileHandle = open(filename, 'r')
        except IOError:
            print("Cannot open " + filename)
        else:
        
            if (lineNum > 0):
                for i in range(lineNum):
                    fileHandle.readline()
        
            reader = csv.reader(fileHandle)
            
            currentSession = None
            
            for row in reader:
                '''
                STO Log File format:
                    Display name of owner
                    Internal name of owner
                    Display name of source
                    Internal name of source
                    Display name of target
                    Internal name of target
                    Display name of event
                    Internal name of event
                    Type
                    Flags
                    Magnitude
                    Base magnitude
                '''
                timeName = row[0].split('::')
                #print(row[0])
                newEntry = STOLogEntry()
                newEntry.setTime(timeName[0])
                newEntry.ownerDisplayName = timeName[1]
                internal = self.splitInternalName(row[1])
                newEntry.ownerInternalType = internal[0]
                newEntry.ownerInternalId = internal[1]
                newEntry.ownerInternalName = internal[2]
                
                newEntry.sourceDisplayName = row[2]
                internal = self.splitInternalName(row[3])
                newEntry.sourceInternalType = internal[0]
                newEntry.sourceInternalId = internal[1]
                newEntry.sourceInternalName = internal[2]
                
                newEntry.targetDisplayName = row[4]
                internal = self.splitInternalName(row[5])
                newEntry.targetInternalType = internal[0]
                newEntry.targetInternalId = internal[1]
                newEntry.targetInternalName = internal[2]
                
                newEntry.eventDisplayName = row[6]
                newEntry.eventInternalName = row[7]
                newEntry.type = row[8]
                newEntry.flags = row[9]
                newEntry.magnitude = row[10]
                newEntry.baseMagnitude = row[11]
                
                '''Time for some tricksy fixes for Season 6 bugs:
                        IF the entry has Shield in it's flags, the entry will be buggy.
                        IF there is no source, the order is actually:
                            owner, target, source
                        IF there is a source, the order is actually:
                            source, target, blank
                            
                    This small function fixes this problem as best it can'''
                ''' if (str.find(newEntry.flags, "Shield") != -1):
                    #Fixing the event if there is no source
                    if (str.equals(newEntry.sourceInternalType,"")):'''
                        
                    
                    
                
                
                lastLogNum = len(self.logEntries) - 1
                if (currentSession is None):
                    currentSession = Session(timeName[0], lastLogNum + 1)
                    
                else:
                    if (lastLogNum >= 0): 
                        deltaTime = newEntry.timestamp - self.logEntries[lastLogNum].timestamp
                       # print(deltaTime)
                        if (deltaTime.total_seconds() > 30):
                          #  print("Session end found, starting new one")
                            currentSession.endTime = self.logEntries[lastLogNum].timestamp
                            currentSession.endIndex = lastLogNum
                            
                            self.sessions.append(currentSession)
                            currentSession = Session(timeName[0], lastLogNum + 1)
                            
                self.logEntries.append(newEntry)
            
            lastLogNum = len(self.logEntries) - 1
            if (currentSession is not None):
                currentSession.endTime = self.logEntries[lastLogNum].timestamp
                currentSession.endIndex = lastLogNum
                self.sessions.append(currentSession)
                         
                
            fileHandle.close()