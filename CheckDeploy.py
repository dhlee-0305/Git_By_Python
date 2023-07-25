import re

from config import *
from gitScan import *
from excelScan import *
from logger import *
from elapsed import *

log = getLogger('CheckDeploy')

@elapsed
def main():
    config = loadConfig()
    repoPath = config['ENV']['REPO_PATH']

    commitList = scanChangeFile()
    deployList = loadExcel()

    # 커밋 리스트 확인
    log.debug('----- COMMIT LIST CHECK -----')
    for commit in commitList:
        commitCheck = 'X'
        if isExist(commit['file'], deployList):
            commitCheck = 'O'
        if isInnerClassExist(repoPath, commit['path'], commit['file']):
            commitCheck = commitCheck + '|I'
        log.debug('['+commitCheck+'] '+ commit['file'])

    # 배포 문서 확인
    log.debug('----- DEPLOY LIST CHECK -----')
    for deploy in deployList:
        deployCheck = 'X'
        if isExist(deploy['file'], commitList):
            deployCheck = 'O'
        log.debug('['+deployCheck+'] '+ deploy['file'])

def isExist(checkStr, strList):
    for str in strList:
        if compareFileName(checkStr, str['file']):
            return True
    return False

def compareFileName(str1, str2):
    return re.sub('\$|\d', '', str1).rstrip('.class').rstrip('.java') \
        == re.sub('\$|\d', '', str2).rstrip('.class').rstrip('.java')

@elapsed
def printCommit(commitList):
    log.debug('----- PRINT COMMIT LIST -----')
    for commit in commitList:
        if len(commit['path']) > 0:
            log.debug('['+commit['change_type']+'] /'+ commit['path'] + '/' + commit['file'])
        else:
            log.debug('['+commit['change_type']+'] /'+ commit['file'])

def isInnerClassExist(repoPath, filePath, sourceName):
    path = repoPath + filePath
    binPath = path.replace('\\', '/').replace('//', '/').replace('/src', '/bin')
    ret = os.path.isfile(binPath + '/'+sourceName.rstrip('.java')+'$.class') \
        or os.path.isfile(binPath + '/'+sourceName.rstrip('.java')+'$1.class')
    return ret

if __name__ == '__main__':
    main()