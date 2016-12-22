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

if __name__ == '__main__':
    rStr = parseTrackMessage('output.txt')
    print rStr
