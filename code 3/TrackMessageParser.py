class MyError(Exception):
    def __str__(self):
        return repr('File read error')
def getSpecialChar(s):
    destStr = '__ascii_'
    if destStr in s:
        index = s.find(destStr)
        index += len(destStr)
        begin = index
        while index < len(s) and s[index].isdigit():
            index+=1
        return  s[begin:index]
    else:
        return None

def getLineNumberFromWeb(s):
    destStr = 'line '
    index = s.find(destStr)
    index += len(destStr)
    begin = index
    while index < len(s) and s[index].isdigit():
        index+=1
    return s[begin:index]
def parseWebMessage(f):
    charMap = createMap()
    fr = None
    try:
        fr = open(f, "r")
    except:
        raise MyError()
    lineList = []
    rList = []
    try:
        lineList = fr.readlines()
    except:
        raise MyError()
    for line in iter(lineList):
        rStr = getLineNumberFromWeb(line)
        rList.append(chr(charMap[int(rStr)]))
    return "".join(rList)

def parseTrackMessage(f):
    fr = None
    try:
        fr = open(f,"r")
    except:
        raise MyError()
    lineList = []
    rList = []
    try:
        lineList = fr.readlines()
    except:
        raise MyError()
    for line in iter(lineList):
        rStr = getSpecialChar(line)
        if rStr == None:
            continue
        rList.append(chr(int(rStr)))
    return "".join(rList)

def createMap():
    rDic = {}
    index = 9
    for value in range(0,255):
        rDic[index] = value
        index += 3
    return rDic

if __name__ == '__main__':
    #rStr = parseTrackMessage('output.txt')
    rStr = parseWebMessage('output.txt')
    print rStr
