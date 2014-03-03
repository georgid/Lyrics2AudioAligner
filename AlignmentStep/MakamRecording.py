'''
Created on Mar 3, 2014

@author: joro
'''
from MakamScore import MakamScore

class MakamRecording:
    '''
    classdocs
    '''
    
    

    def __init__(self, makamScore, pathToLinkedSectionsFile):
       
       # the score of the piece
        self.makamScore = makamScore
        
        # section lyrics
        self.sectionLyricsMap=[]
        
        # section timestamps,
        self.beginTs=[]
        self.endTs = []  
        
        self.sectionNames = []
        
        
        self.loadsectionTimeStamps( pathToLinkedSectionsFile)
        self.sectionLyricsMap = list(self.sectionNames)
        
        '''
        Constructor
        '''
        return
    
    
    # Handles the Division into sections. 
    # @param section annotaions as TimeStamps - 
    # @param txtTur - lyrics: each new line is a section
    # @param .mp3 -audio 
    def assignSectionLyrics(self):
        
       # TODO: write cheker for score 
        
       # check section names and get lyrics from score. use index to map to Ts index
        for index in range(len(self.sectionNames)):
            
            if self.sectionNames[index] in MakamScore.sectionNames:
                self.sectionLyricsMap[index] =  self.makamScore.sectionLyrics[self.sectionNames[index]]
            else:
                print "unknown section name: %s " ,  (self.sectionNames[index])
                self.sectionLyricsMap[index] = ""
                
            
        return
            
        
        
             
    ## loads timestamps from file .sectionAnno
    def loadsectionTimeStamps(self, pathToLinkedSectionsFile):
    
        sectionsFileHandle = open(pathToLinkedSectionsFile, 'rU')
        
        # skip first line
#         next(sectionsFileHandle)
        
        for line in sectionsFileHandle:
            tokens =  line.split()
            
            self.beginTs.append(tokens[0])
            self.endTs.append(tokens[1])
            self.sectionNames.append(tokens[2])
        
            
        # divide into columns
        
        
        
        sectionsFileHandle.close()
        
        return
    
    
if __name__ == '__main__':
        pathTotxtTur = '/Volumes/IZOTOPE/sertan_sarki/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik.txtTur'
        makamScore = MakamScore(pathTotxtTur)
        
        pathToSectionAnnotations = '/Volumes/IZOTOPE/sertan_sarki/muhayyerkurdi--sarki--duyek--ruzgar_soyluyor--sekip_ayhan_ozisik/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde/1-05_Ruzgar_Soyluyor_Simdi_O_Yerlerde.sectionAnno.txt'
        makamRecording = MakamRecording(makamScore, pathToSectionAnnotations)
        makamRecording.assignSectionLyrics()
        
        print "ready"
   
 
        