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

    commitList = commitFile()
    deployList = loadExcel()

    # 커밋 리스트 확인
    log.info('----- COMMIT LIST CHECK -----')
    for commit in commitList:
        commitCheck = 'X'
        if isInclude(commit['file'], deployList):
            commitCheck = 'O'
        if isInnerClassExist(repoPath, commit['path'], commit['file']):
            commitCheck = commitCheck + '|I'
        log.info('COMMIT ['+commitCheck+'] '+ commit['file'])

    # 배포 문서 확인
    log.info('----- DEPLOY LIST CHECK -----')
    for deploy in deployList:
        deployCheck = 'X'
        if isInclude(deploy['file'], commitList):
            deployCheck = 'O'
        log.info('EXCEL ['+deployCheck+'] '+ deploy['file'])

def isInclude(checkStr, strList):
    for str in strList:
        if compareFileName(checkStr, str['file']):
            return True
    return False

def compareFileName(str1, str2):
    return re.sub('\$|\d', '', str1).rstrip('.class').rstrip('.java') \
        == re.sub('\$|\d', '', str2).rstrip('.class').rstrip('.java')

def isInnerClassExist(repoPath, filePath, sourceName):
    path = repoPath + filePath
    binPath = path.replace('\\', '/').replace('//', '/').replace('/src', '/bin')
    ret = os.path.isfile(binPath + '/'+sourceName.rstrip('.java')+'$.class') \
        or os.path.isfile(binPath + '/'+sourceName.rstrip('.java')+'$1.class')
    return ret

if __name__ == '__main__':
    main()