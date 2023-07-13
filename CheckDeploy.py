import re

from config import *
from gitScan import *
from excelScan import *
from logger import *

config = loadConfig()
log = getLogger('CheckDeploy')

def checkDeploy():
    repoPath = config['ENV']['REPO_PATH']
    prevCommit = config['COMMIT']['PREV_COMMIT']
    currCommit = config['COMMIT']['CURR_COMMIT']
    commitList = scanChangeFile(repoPath, prevCommit, currCommit)

    deployList = loadExcel()

    # 커밋 리스트 확인
    log.debug('----- COMMIT LIST CHECK -----')
    for commit in commitList:
        commitCheck = 'X'
        for deploy in deployList:
            if compareFileName(commit[2], deploy[1]) :
                commitCheck = 'O'
        if isInnerClassExist(repoPath, commit[1], commit[2]):
            commitCheck = commitCheck + '|I'
        log.debug('['+commitCheck+'] '+ commit[2])


    log.debug('----- DEPLOY LIST CHECK -----')

    # 배포 문서 확인
    for deploy in deployList:
        deployCheck = 'X'
        for commit in commitList:
            if compareFileName(deploy[1], commit[2]):
                deployCheck = 'O'
        
        log.debug('['+deployCheck+'] '+ deploy[1])
    
    # printCommit(commitList)

def compareFileName(str1, str2):
    return re.sub('\$|\d', '', str1).rstrip('.class').rstrip('.java') == re.sub('\$|\d', '', str2).rstrip('.class').rstrip('.java')

def printCommit(commitList):
    log.debug('----- PRINT COMMIT LIST -----')
    for commit in commitList:
        if len(commit[1]) > 0:
            log.debug('['+commit[0]+'] /'+ commit[1] + '/' + commit[2])
        else:
            log.debug('['+commit[0]+'] /'+ commit[2])

def isInnerClassExist(repoPath, filePath, sourceName):
    path = repoPath + filePath
    binPath = path.replace('\\', '/').replace('//', '/').replace('/src', '/bin')
    ret = os.path.isfile(binPath + '/'+sourceName.rstrip('.java')+'$.class') \
        or os.path.isfile(binPath + '/'+sourceName.rstrip('.java')+'$1.class')
    return ret

checkDeploy()