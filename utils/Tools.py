'''
Created on Feb 15, 2014

@author: joro
'''

import os
import shutil

# find files of given type in subdirectories
#   

targetDir = '/Volumes/izotope/sertan_sarki/'
# checkedDir = '/Users/joro/Documents/Phd/UPF/sertan_sarki'
checkedDir='/Volumes/SAMSUNG/sertan_sarki'

# top level function
def browseDirs(pathToDir):
    for rootPathTofileName, dirs, files in os.walk(pathToDir):
       
        for name in files: 
            if name.endswith(("sectionLinks.txt")):
                
                # third param is not functional - e.g. for print out only
                checkIfNameInListFromTargetDir(name, targetDir, rootPathTofileName)
    return

# checks if the given name is in list of dirs, which is derived from target dir 
def checkIfNameInListFromTargetDir(name, targetDir, rootPathTofileName):
   
    nameAndExt = os.path.splitext(name)
    nameNoExt = os.path.splitext(nameAndExt[0])
    
    # list of target fullpath and dirs names
    dirNames, fullDirNames = browseDirNames(targetDir)
    
    for i in range(len(dirNames)):
        if nameNoExt[0] == dirNames[i]:
            print "copying: ", 
            
            targetPath=os.path.join(fullDirNames[i],dirNames[i])
            checkedDirFile=os.path.join(rootPathTofileName, name)
            shutil.copy(checkedDirFile, targetPath)
            
    
    return

# browse dirs with recordings of the given symbTr composition. browse two times 1st level
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



if __name__ == "__main__":
    import sys
 
    browseDirs(checkedDir)
#     browseDirNames(sys.argv[1])