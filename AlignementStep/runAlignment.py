'''
Created on Feb 19, 2014

@author: joro
'''

## loads timestamps from file .sectionLinks 
def loadsectionTimeStamps(pathToLinkedSectionsFile):
    
    beginTs=[]
    endTs = []  
    sectionNames = []
    
    
    return beginTs, endTs, sectionNames

# for given audio and ts divide audio into audio segments
def divideAudio(pathToAudio, beginTs, endTs):
    
    return

# NOTE: Each section shoud be in a new line. Ideally copy paste from score.pdf to a textFile.
# assigns strophes(lyrical lines) to sections:  
# assumes strophes are 4 in pathTo.txtdivided file. Checks repeating labels in pathToLinkedSectionsFile   
# TODO: load from  symbTr instead 
def loadLyricsForSections(pathToTxtDividedFile, sectionNames):
    
    return


if __name__ == '__main__':    