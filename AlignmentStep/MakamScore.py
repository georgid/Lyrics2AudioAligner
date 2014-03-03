'''
Created on Mar 3, 2014

@author: joro
'''

class MakamScore():
    '''
    classdocs
    '''

    #class const variable. order is important
    sectionNames = ["zemin","nakarat", "meyan","nakarat2"]

    def __init__(self, pathToTxtTurFile):
        '''
        Constructor
        
        '''

#         self.sectionLyrics=[]
        self.sectionLyrics = {MakamScore.sectionNames[0]:"",MakamScore.sectionNames[1]:"",MakamScore.sectionNames[2]:"", MakamScore.sectionNames[3]:""}
        
        # lyrics divided by sections
        self.loadLyricsForSections(pathToTxtTurFile)
        
        

        
        
             # NOTE: Each section shoud be in a new line. Ideally copy paste from score.pdf to a textFile.
    # assigns strophes(lyrical lines) to sections:  
    # assumes strophes are 4 in pathTo.txtdivided file. Checks repeating labels in pathToLinkedSectionsFile   
    # TODO: load from  symbTr instead 
    def loadLyricsForSections(self, pathToTxtTurFile):
            txtTurFileHandle =  open(pathToTxtTurFile)
            lyrics = txtTurFileHandle.readlines()
            if len(lyrics) != 4:
                print "num of lyrics lines in file % is not 4"
                return
            else:
                # put in dictionary the lyrics
                for i in range(4):
                    self.sectionLyrics[MakamScore.sectionNames[i]]=lyrics[i]
                
             
#                 self.sectionLyrics.append(lyrics[0])
#                 self.sectionLyrics.append(lyrics[1])
#                 self.sectionLyrics.append(lyrics[2])
#                 self.sectionLyrics.append(lyrics[3])
            
