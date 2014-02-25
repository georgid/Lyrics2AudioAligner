'''
Created on Feb 19, 2014

@author: joro
'''

## loads timestamps from file .sectionLinks 
def loadsectionTimeStamps(pathToLinkedSectionsFile):
    sectionsFileHandle = open(pathToLinkedSectionsFile, 'r')
    
    next(sectionsFileHandle)
    for line in sectionsFileHandle:
        tokens =  line.split()
        # TODO: extract sections as well
        print tokens[0], tokens[1], tokens[2]
        
    # divide into columns
    
    beginTs=[]
    endTs = []  
    sectionNames = []
    
    
    sectionsFileHandle.close()
    
    return beginTs, endTs, sectionNames


# for given audio and ts divide audio into audio segments
def divideAudio(pathToAudio, beginTs, endTs):
    # call SOX here with subprocess
    
    return

# NOTE: Each section shoud be in a new line. Ideally copy paste from score.pdf to a textFile.
# assigns strophes(lyrical lines) to sections:  
# assumes strophes are 4 in pathTo.txtdivided file. Checks repeating labels in pathToLinkedSectionsFile   
# TODO: load from  symbTr instead 
def loadLyricsForSections(pathToTxtDividedFile, sectionNames):
    
    return


if __name__ == '__main__':    
    loadsectionTimeStamps('/Volumes/IZOTOPE/sertan_sarki/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde.sectionLinks.txt')
    