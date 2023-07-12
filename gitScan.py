import os
from git import Repo
from config import *

config = loadConfig()

def connectGit(path):
    repo = Repo(path)
    return repo

def scanChangeFile(repo, prev, curr):
    prev = repo.commit(prev)
    curr = repo.commit(curr)
    diff_index = prev.diff(curr)
    changeFileList = []
    for diff in diff_index:
        fileName = os.path.basename(str(diff.b_path))
        path = os.path.dirname(str(diff.b_path))
        changeFile = [diff.change_type, path, fileName]
        #print('['+diff.change_type+'] '+path+'/'+fileName)
        print(changeFile)

        changeFileList.append(changeFile)
    return changeFileList

repo_path = config['ENV']['REPO_PATH']
repository = connectGit(repo_path)

prev_commit = config['COMMIT']['PREV_COMMIT']
curr_commit = config['COMMIT']['CURR_COMMIT']
fileList = scanChangeFile(repository, prev_commit, curr_commit)

