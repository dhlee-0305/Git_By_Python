import os
from git import Repo

def connectGit(path):
    repo = Repo(path)
    return repo

def scanChangeFile(path, prev, curr):
    repo = connectGit(path)

    prev = repo.commit(prev)
    curr = repo.commit(curr)
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
        path = os.path.dirname(str(diff.b_path))
        changeFile = [diff.change_type, path, fileName]
        changeFileList.append(changeFile)
    return changeFileList

