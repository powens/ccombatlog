'''
Created on Oct 27, 2010

@author: Patrick
'''

import STOLog
import DamageMeters

if __name__ == '__main__':
    '''import sys -- sys.argv[1]'''
    stoLog = STOLog.STOLog('sessiontest.Log')
    dm = DamageMeters.createMeters(stoLog)
    
    ''' for objKey, objValue in dm.objects.items():
        print(objValue.displayName + " " + objValue.internalName)
        for damKey, damValue in objValue.damage.items():
            print("  " + damValue.displayName + "[" + damValue.internalName +"] " + str(damValue.damage) + " " + str(damValue.baseDamage) + " " + str(damValue.count))'''
    
    print(str(len(dm.sessions)) + " sessions")
    for session in dm.sessions:
        print("SESSION START: " + str(session.startTime) + " -- " + str(session.endTime))
        for objKey, objValue in session.objects.items():
            print(objValue.displayName + " " + objValue.internalName + " -- " + objValue.ownerId)
            for damKey, damValue in objValue.damage.items():
                print("  " + damValue.displayName + "[" + damValue.internalName +"] " + str(damValue.damage) + " " + str(damValue.baseDamage) + " " + str(damValue.count))