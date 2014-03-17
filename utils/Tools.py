'''
Created on Feb 15, 2014

@author: joro
'''

import os
import shutil
import glob

# find files of given type in subdirectories
#   

targetDir = '/Volumes/IZOTOPE/sertan_sarki/'
# checkedDir = '/Users/joro/Documents/Phd/UPF/sertan_sarki'
# checkedDir = '/Volumes/SAMSUNG/sertan_sarki'

checkedDir = '/Volumes/IZOTOPE/researchCorpus_SymbTr/symbtr_cc_489'

# checkedDir = '/Volumes/IZOTOPE/researchCorpus_SymbTr/txt/'


''' go through all files in checkedDir with given extension 
    and compare with name of each folder in target dir

'''


def browseDirs(checkedDir, targetDir, fileExtension):
    for rootPathTofileName, dirs, files in os.walk(checkedDir):
       
        for name in files: 
            if name.endswith(fileExtension):
                
#                 fullFileName = os.path.join(rootPathTofileName, name)
                # HERE do something with file
                
#                 print os.lstat( fullFileName).st_size
                # third param is not functional - e.g. for print out only
                checkIfNameInListFromTargetDir(name, targetDir, rootPathTofileName)
    return

# checks if the given name is in list of dirs, which is derived from target dir . If it is it copies it to given target dir
def checkIfNameInListFromTargetDir(name, targetDir, rootPathTofileName):
   
    nameAndExt = os.path.splitext(name)
    nameNoExt = nameAndExt[0]
    
    # list of target fullpath and dirs names
    dirNames, fullDirNames = browseDirNames(targetDir)
    
    for i in range(len(dirNames)):
        if nameNoExt[0] == dirNames[i]:
            print "copying: ",
            
            targetPath = os.path.join(fullDirNames[i], dirNames[i])
            checkedDirFile = os.path.join(rootPathTofileName, name)
            print checkedDirFile
#             shutil.copy(checkedDirFile, targetPath)
            
    
    return

# browse dirs with recordings of the given symbTr composition. browse TWO times one level
# @return dirsWithRecordings - oonly the dir names. 
# @return fullDirNames - list of correponding full paths to dirs WithRecordings
def browseDirNames(pathToDir):
    dirsWithRecordings = []
    fullDirNames = []
    for roots, dirs, files in walklevel(pathToDir, level=0):
        for dirName in dirs:
            if not "NOT" in dirName and not dirName == ".git" : 
                fullDirName = os.path.join(pathToDir, dirName)
#                 print  "\n" , fullDirName
                for roots, subDirNames, files in walklevel(fullDirName, level=0):
                    for subDirName in subDirNames: 
#                         print subDirName
                        dirsWithRecordings.append(subDirName)
                        fullDirNames.append(fullDirName)
    return dirsWithRecordings, fullDirNames


# dir  files to specific level. not mine code 
def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

# loads a file with columns. returns them as two dim. array
def loadFileWithColumns(fullPathtoFile, numColumns):
    
    array = []
    inputFileHandle = open(fullPathtoFile, 'r')
    allLines = inputFileHandle.readlines()
     
    for line in allLines:
        tokens = line.split("\t")
        array.append(tokens)
#         for token in tokens:
            
         
    inputFileHandle.close()
    return array



def checkIfNameInListFromTargetDir2( pathTofileName, targetDir ):
   
    name = os.path.basename(pathTofileName)
    nameAndExt = os.path.splitext(name)
    nameNoExt = nameAndExt[0]
    
    # list of target fullpath and dirs names
    dirNames = os.walk(targetDir).next()[1] 
    
    for i in range(len(dirNames)):
        if nameNoExt == dirNames[i]:
            
            targetPath = os.path.join(targetDir, dirNames[i])
            print pathTofileName

#             print "copying: ",
#             shutil.copy(pathTofileName, targetPath)
            
    
    return




if __name__ == "__main__":
    import sys
    fileExtension = ".txt"
#     browseDirs(checkedDir, targetDir, fileExtension)
    
   
    print ' files which have symbTrV2.0 match'
#   
    for fileName in glob.glob(checkedDir + "/*.txt"):
        pathName = os.path.join(checkedDir,fileName)
        checkIfNameInListFromTargetDir2 (pathName, targetDir )
   
    print "all .txt files"
   # find .txt files in 2nd level of given dir
    dirsWithRecordings, fullDirNames = browseDirNames(targetDir)
    for dir in fullDirNames:
         for fileName in glob.glob(dir + "/*.txt"):
             print fileName 
        
#     array = loadFileWithColumns('/Users/joro/Documents/compositions/like_atiltudes.sonicVis.txt', 2)
#     print array
