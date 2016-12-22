#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8
class PatternError(Exception):
    """
    Lua Table 格式错误,格式错误是抛出
    """
    def __str__(self):
        return repr("Lua table error!")
class FileError(Exception):
    """
    文件操作错误
    """
    def __str__(self):
        return repr("File error!")

class PyLuaTblParser(object):
    """
    PyLuaTblParser
    1.load(self,s) 字符串读取Lua table数据
    2.dump(self) 返回Lua table字符串
    3.loadLuaTable(self,f) 文件读取Lua table数据
    4.dumpLuaTable(self,f) 将类中内容存储到文件中,格式为Lua Table 字符串
    5.loadDict(self,d) 从字典参数读取数据
    6.dumpDict(self) 返回包含数据的字典
    """

    def __init__(self,len = 0):
        self.data = {}
        #self.length = None
        self.length = len

    def load(self,s):
        self.length = len(s)
        self.data,begin = self.parserTable(s,0)
        begin = self.skip(s,begin)
        if begin < self.length:
            raise PatternError()

    def dump(self):
        return self.encodeValue(self.data)

    def loadLuaTable(self,f):
        rList = []
        fr = None
        try:
            fr = open(f,"r")
            rList = fr.readlines()
            fr.close()
        except:
            raise Exception()
        s = "".join(rList)
        self.load(s)

    def dumpLuaTable(self,f):
        fo = None
        try:
            fo = open(f,"w")
            rStr = self.dump()
            fo.write(rStr)
            fo.close()
        except:
            raise FileError()

    def loadDict(self,d):
        rDic = {}
        if isinstance(d,list):
            for key,value in enumerate(d):
                rDic[key] = self.loadValue(value)
        elif isinstance(d,dict):
            for key,value in d.iteritems():
                if self.isString(key) or self.isNumber(key):
                    rDic[key] = self.loadValue(value)
        self.data = rDic

    def dumpDict(self):
        rDic = {}
        if isinstance(self.data,list):
            for key,value in enumerate(self.data):
                rDic[key] = self.loadValue(value)
        elif isinstance(self.data,dict):
            for key,value in self.data.iteritems():
                rDic[key] = self.loadValue(value)
        return rDic

    def safeEqual(self,s,begin,end,des):
        """
        索引安全的是否相等判别函数
        :param s: 源字符串
        :param beg: 开始索引
        :param end: 接收索引
        :param des: 目标字符串
        :return: 布尔值
        """
        if end > self.length : return False
        return s[begin:end] == des

    def skipTheUnvalid(self,s,begin = 0):
        """
        跳过多余的类空格字符
        :param s: 源字符串
        :param begin: 开始索引
        :return: 返回非空格字符串的索引
        """
        unvalid_character = ['\n','\t','\r',' ']
        while (begin < self.length) and (s[begin] in unvalid_character):
            begin += 1
        return begin

    def skipTheComment(self,s,begin = 0):
        """
        跳过注释:
        注释分三种:
        1.单行注释 --
        2.多行注释:--[[ *** ]]
        3.兼容性最强的注释:--[===[ *** ]===],两边等号数量要相同,数量无所谓
        :param s: 源字符串
        :param begin: 其实索引
        :return: 返回索引
        """
        if self.safeEqual(s,begin,begin + 2,'--'):
            if self.safeEqual(s,begin,begin + 3,'--['):
                if self.safeEqual(s,begin,begin + 4,'--[['):
                    #注释2
                    index = begin + 4
                    while index + 2 <= self.length and s[index:index+2] != ']]':
                        index += 1
                    if index + 2 > self.length:
                        raise PatternError()
                    else:
                        return index + 2
                else:
                    #注释3
                    index = begin + 3
                    while self.safeEqual(s,index,index + 1,'='):
                        index += 1
                    if self.safeEqual(s,index,index + 1,'['):
                        leftLen = index - begin - 3
                        index +=1
                        while index < self.length and s[index] != ']':
                            index += 1
                        if index >= self.length:
                            raise PatternError()
                        index += 1
                        rightLen = 0
                        while index < self.length and s[index] == '=':
                            index += 1
                            rightLen += 1
                        if rightLen != leftLen or s[index] != ']':
                            raise PatternError()
                        return index + 1
                    else:
                        #格式不对
                        raise PatternError()
            else:
                index = begin + 2
                while index < self.length and s[index] != '\n':
                    index += 1
                return index + 1
        else:
            return begin

    def skip(self,s,begin = 0):
        """
        跳过所有的类空格字符和注释字符
        :param s: 源字符串
        :param begin: 起始索引
        :return: 下一个有效的下标
        """
        lastStep = begin
        while begin < self.length:
            begin = self.skipTheUnvalid(s,begin)
            begin = self.skipTheComment(s,begin)
            if lastStep == begin:
                break
            else:
                lastStep = begin
        return begin

    def storeList(self,ls):
        """
        存储从字符串读取的数据到list
        :param ls: 字典,key为1,2,3,4
        :return: list
        """
        rList = []
        local_length = len(ls)
        for i in range(1,local_length + 1):
            rList.append(ls[i])
        return rList

    def storeDic(self,d):
        """
        存储从字符串读取的数据到字典
        :param d: dic
        :return: dic
        """
        rDic = {}
        for key,value in d.iteritems():
            if value == None:
                continue
            rDic[key] = value
        return rDic

    def isValidChar(self,c):
        """
        判断是否为有效字符串
        :param c: 字符串
        :return: Bool
        """
        if c == '_' or c.isdigit() or c.isalpha():
            return True
        else:
            return False

    def isNumber(self,n):
        """
        判断是否为有效数字
        :param n: 字符串
        :return: Bool
        """
        if isinstance(n,int) or isinstance(n,long) or isinstance(n,float):
            return True
        else:
            return False

    def isString(self,s):
        """
        判断是否为字符串
        :param s:
        :return:
        """
        if isinstance(s,str):
            return True
        else:
            return False

    def decorateString(self,s,begin,endStr):
        """
        Lua中字符串共三种形式:
        1.'****'
        2."****"
        3.[[ *** ]]
        :param s: 源字符串
        :param begin: 开始索引
        :param endStr: 字符串结束符
        :return: 修饰后的字符串
        """
        #映射表
        luaToPythonDic = {
            '\\"': '\"',
            "\\'": "\'",
            "\\b": "\b",
            "\\f": "\f",
            "\\r": "\r",
            "\\n": "\n",
            "\\t": "\t",
            "\\u": "u",
            "\\\\": "\\",
            "\\/": "/",
            "\\a": "\a",
            "\\v": "\v"
        }
        ls = []
        #pattern 1,2
        if self.safeEqual(s,begin,begin + 1,"'") or self.safeEqual(s,begin,begin+1,'"'):
            begin += 1
            while begin < self.length:
                if(s[begin] == endStr):
                    return "".join(ls),begin + 1
                elif s[begin] == '\\':
                    if begin + 2 > self.length:
                        raise PatternError()
                    tempStr = s[begin:begin+2]
                    if luaToPythonDic.has_key(tempStr):
                        ls.append(luaToPythonDic[tempStr])
                        begin += 2
                    else:
                        raise PatternError()
                else:
                    ls.append(s[begin])
                    begin += 1
            if begin >= self.length:
                raise PatternError()
        # pattern 3
        elif self.safeEqual(s,begin,begin + 2,'[['):
            begin += 2
            while begin + 1 < self.length:
                if self.safeEqual(s,begin,begin + 2,']]'):
                    return "".join(ls),begin + 2
                elif s[begin] == '\\':
                    tempStr = s[begin:begin + 2]
                    if luaToPythonDic.has_key(tempStr):
                        ls.append(luaToPythonDic[tempStr])
                    else:
                        raise PatternError()
                else:
                    ls.append(s[begin])
                    begin += 1
            if begin + 1 >= self.length:
                raise PatternError()
        else:
            raise PatternError()

    def parserNumber(self,s,begin):
        """
        解析数字
        :param s:
        :param begin:
        :return: 数字,索引
        """
        numberChars = '+-0123456789.e'
        isPositive = True
        index = begin
        if s[index] == '-':
            isPositive = False
            index += 1
        while index < self.length and s[index].lower() in numberChars:
            index += 1
        try:
            num = eval(s[begin:index])
            return num,index
        except:
            raise PatternError()

    def parserCommon(self,s,begin):
        '''
        返回普通字符串
        :param s: 源字符串
        :param begin: 起始索引
        :return: (str,index)
        '''
        index = begin
        while index < self.length and self.isValidChar(s[index]):
            index+=1
        return s[begin:index],index

    def isSpecial(self,value):
        """
        判读是否为特殊字符串
        :param value: str
        :return: Bool
        """
        if value == 'nil' or value == 'true' or value == 'false':
            return True
        else:
            return False

    def getSpecial(self,key):
        """
        根据特殊字符串获得相应的值
        :param key: str
        :return: (None,True,False)
        """
        specialDic = {
            'nil':None,
            'true':True,
            'false':False
        }
        if specialDic.has_key(key):
            return specialDic[key]
        else:
            return None

    def parserSpecial(self,s,begin):
        """
        返回特殊字符串对应的值
        :param s: 源字符串
        :param begin: 起始索引
        :return: 值(None,True,False),index
        """
        index = begin
        while index < self.length and s[index].isalpha():
            index += 1
        subStr = s[begin:index]
        if self.isSpecial(subStr):
            return self.getSpecial(subStr),index
        else:
            raise PatternError()

    def parserString(self,s,begin):
        """
        解析字符串
        :param s: 源字符串
        :param begin: 起始索引
        :return: 解析的字符串或数字,下一个索引
        """
        isStr = False
        begin = self.skip(s,begin)
        numberChars = '+-0123456789.e'

        rList = []
        #防止Lua连字符,使用while循环处理
        while True:
            if s[begin] in numberChars:
                #现在不能确定是否为数字还是字符串,有..链接的都是字符串
                tempNumber,begin = self.parserNumber(s,begin)
                rList.append(str(tempNumber))
            else:
                isStr = True
                subStr = None
                #修饰字符串
                if s[begin] == "'":
                    subStr,begin = self.decorateString(s,begin,"'")
                elif s[begin] == '"':
                    subStr,begin = self.decorateString(s,begin,'"')
                elif self.safeEqual(s,begin,begin+2,'[['):
                    subStr,begin = self.decorateString(s,begin,']]')
                else:
                    raise PatternError()
                rList.append(subStr)
            begin = self.skip(s,begin)
            if self.safeEqual(s,begin,begin+2,".."):
                begin += 2
                if begin >= self.length or s[begin] == '.':
                    raise PatternError()
                isStr = True
                begin = self.skip(s,begin)
            else:
                break
        if isStr :
            return "".join(rList),begin
        else:
            return eval(rList[0]),begin

    def parserValue(self,s,begin):
        """
        根据有效字符串返回有效的值
        :param s: 源字符串
        :param begin: 索引
        :return: (value,index)
        """
        begin = self.skip(s,begin)
        if begin >= self.length:
            raise PatternError()
        if s[begin] == '{':
            return self.parserTable(s,begin)
        elif s[begin] == 'n' or s[begin] == 't' or s[begin] == 'f':
            return self.parserSpecial(s,begin)
        elif self.safeEqual(s,begin,begin + 2,'[[') \
        or self.safeEqual(s,begin,begin+1,"'") \
        or self.safeEqual(s,begin,begin + 1,'"'):
            return self.parserString(s,begin)
        else:
            raise PatternError()

    def isOverFlow(self,index):
        """
        检测是否越界
        :param index:
        :return: if overflow : send except
        """
        if index >= self.length:
            raise PatternError()

    def parserTable(self,s,begin):
        begin = self.skip(s,begin)
        self.isOverFlow(begin)
        if s[begin] != '{':
            raise PatternError()
        begin += 1
        rDic = {}
        rLen = 1
        isList = True           #是否是列表,一开始假定是列表
        isDelimited = True      #是否应经被(,;)界定,开始的时候假设已经界定
        isDoubleValue = False   #是否是{ [key] = value [key] = value }格式
        isEmpty = True          #是否为空

        while True:
            begin = self.skip(s,begin)
            self.isOverFlow(begin)
            #结束符
            if s[begin] == '}':
                if isEmpty:
                    return {},begin + 1
                else:
                    if isList:
                        return self.storeList(rDic),begin + 1
                    else:
                        return self.storeDic(rDic),begin + 1

            elif s[begin] == ',' or s[begin] == ';':
                if isDelimited:
                    raise PatternError
                else:
                    isDelimited = True
                    isDoubleValue = False
                    begin += 1
            else:
                if isDoubleValue:
                    raise PatternError()
                isDoubleValue = True
                isDelimited = False
                # table
                if s[begin] == '{':
                    value,begin = self.parserTable(s,begin)
                    rDic[rLen] = value
                    rLen += 1
                # lua string must
                elif self.safeEqual(s,begin,begin + 2,'[['):
                    value,begin = self.parserString(s,begin)
                    rDic[rLen] = value
                    rLen += 1
                # [key] = value
                elif s[begin] == '[':
                    isList = False
                    begin += 1
                    begin = self.skip(s,begin)
                    self.isOverFlow(begin)
                    #key
                    key,begin = self.parserValue(s,begin)
                    begin = self.skip(s,begin)
                    self.isOverFlow(begin)
                    if s[begin] != ']':
                        raise PatternError()
                    begin += 1
                    begin = self.skip(s,begin)
                    self.isOverFlow(begin)
                    #value
                    if s[begin] != '=':
                        raise PatternError()
                    else:
                        begin += 1
                        value,begin = self.parserValue(s,begin)
                        if self.isNumber(key) and rDic.has_key(key):
                            continue
                        else:
                            rDic[key] = value
                # lua value
                elif s[begin] == '_' or s[begin].isalpha():
                    key,begin = self.parserCommon(s,begin)
                    if self.isSpecial(key):
                        rDic[rLen] = self.getSpecial(key)
                        rLen += 1
                    else:
                        isList = False
                        begin = self.skip(s,begin)
                        self.isOverFlow(begin)
                        if s[begin] != '=':
                            raise PatternError()
                        else:
                            begin += 1
                            begin = self.skip(s,begin)
                            value,begin = self.parserValue(s,begin)
                            rDic[key] = value
                # lua string
                elif s[begin] == '"' or s[begin] ==  "'" :
                    value,begin = self.parserString(s,begin)
                    rDic[rLen] = value
                    rLen += 1
                elif s[begin] in '-0123456789.e':
                    value,begin = self.parserNumber(s,begin)
                    rDic[rLen] = value
                    rLen += 1
                else:
                    raise PatternError()
            isEmpty = False

    def encodeSpecial(self,key):
        """
        返回特殊字符解码
        :param key: None,True,False
        :return: str,None
        """
        specialDic = {
            None : 'nil',
            True : 'true',
            False: 'false'
        }
        if specialDic.has_key(key):
            return specialDic[key]
        else:
            return None

    def encodeNumber(self,num):
        return str(num)

    def encodeString(self,s):
        specialDic = {
            "\a": "\\a",
            "\b": "\\b",
            "\f": "\\f",
            "\n": "\\n",
            "\r": "\\r",
            "\t": "\\t",
            "\v": "\\v",
            "\"": '\\"',
            "\'": "\\'",
            "\\": "\\\\"
        }
        rList = []
        for char in s:
            if char in specialDic:
                rList.append(specialDic[char])
            else:
                rList.append(char)
        rStr = "".join(rList)
        if '"' in rStr:
            return "'" + rStr + "'"
        elif "'" in rStr:
            return '"' + rStr + '"'
        else:
            return "'" + rStr + "'"

    def encodeValue(self,value):
        if value == None or isinstance(value,bool):
            return self.encodeSpecial(value)
        elif isinstance(value,str):
            return self.encodeString(value)
        elif self.isNumber(value):
            return self.encodeNumber(value)
        elif isinstance(value,list):
            return self.encodeList(value)
        elif isinstance(value,dict):
            return self.encodeDic(value)
        else:
            raise PatternError()

    def encodeList(self,ls):
        rList = []
        for value in ls:
            rList.append(self.encodeValue(value))
        return '{' + ','.join(rList) + '}'

    def encodeDic(self,dc):
        rList = []
        for key,value in dc.iteritems():
            if isinstance(key,tuple) or isinstance(key,complex):
                raise PatternError()
            rList.append('[' + self.encodeValue(key) + '] = ' + self.encodeValue(value) )
        return '{' + ','.join(rList) + '}'

    def loadValue(self,v):
        if isinstance(v,list):
            rList = []
            for value in v:
                rList.append(self.loadValue(value))
            return rList
        elif isinstance(v,dict):
            rDic = {}
            for key,value in v.iteritems():
                rDic[key] = self.loadValue(value)
            return rDic
        else:
            return v

if __name__ == '__main__':
    """
    s1 = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
    s2 = '{array = {65,23,5}, 1,2,3}'                                                   #right
    s3 = '{dict = {mixed = {43,54.33,false,9,string = "value",}}}'
    s4 = '{string = "value"}'
    parser = PyLuaTblParser()
    parser.load(s1)
    d = parser.dumpDict()
    print d

    """
    a1 = PyLuaTblParser()
    a2 = PyLuaTblParser()
    a3 = PyLuaTblParser()
    #test_str = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
    test_str = '{array = {65,23,5,}}'
    a1.load(test_str)
    d1 = a1.dumpDict()

    a2.loadDict(d1)
    a2.dumpLuaTable('test.txt')
    a3.loadLuaTable('test.txt')

    d3 = a3.dumpDict()