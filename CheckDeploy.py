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
            if compareFile(commit[2], deploy[1]) :
                commitCheck = 'O'

        log.debug('['+commitCheck+'] '+ commit[2])


    log.debug('----- DEPLOY LIST CHECK -----')

    # 배포 문서 확인
    for deploy in deployList:
        deployCheck = 'X'
        for commit in commitList:
            if compareFile(deploy[1], commit[2]):
                deployCheck = 'O'
        
        log.debug('['+deployCheck+'] '+ deploy[1])

def compareFile(str1, str2):
    return str1.rstrip('.class').rstrip('.java') == str2.rstrip('.class').rstrip('.java')

checkDeploy()