import os

from git import Repo
from config import *

def commitFile():

    config = loadConfig()
    
    repoPath   = config['ENV']['REPO_PATH']
    ignoreList = config['ENV']['IGNOR_FILE']
    prevCommit = config['COMMIT']['PREV_COMMIT']
    currCommit = config['COMMIT']['CURR_COMMIT']

    repo = Repo(repoPath)
    prev = repo.commit(prevCommit)
    curr = repo.commit(currCommit)
    diff_index = prev.diff(curr)

    '''
    change_type
        ’A’ for added paths
        ’D’ for deleted paths
        ’R’ for renamed paths
        ’M’ for paths with modified data
        ’T’ for changed in the type paths
    '''
    changeFileList = []
    for diff in diff_index:
        fileName = os.path.basename(str(diff.b_path))
        if not isIgnore(ignoreList, fileName):
            path = os.path.dirname(str(diff.b_path))
            changeFile = {'change_type':diff.change_type, 'path':path, 'file':fileName}
            changeFileList.append(changeFile)
    
    return changeFileList

def isIgnore(ignoreList, fileName):
    if ignoreList.find(fileName) != -1:
        return True
    else:
        return False

if __name__ == '__main__':
    changed = commitFile()
    for s in changed:
        print(s)

