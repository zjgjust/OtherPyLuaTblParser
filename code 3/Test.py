#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding=utf-8
from PyLuaTblParser import *

if __name__ == '__main__':
    a1 = PyLuaTblParser()
    a2 = PyLuaTblParser()
    a3 = PyLuaTblParser()

    test_str = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
    a1.load(test_str)
    d1 = a1.dumpDict()

    a2.loadDict(d1)
    a2.dumpLuaTable('test.txt')
    a3.loadLuaTable('test.txt')

    d3 = a3.dumpDict()
    print d3
#附：test_str对应的Python
"""
    dict：
    {
        "array": [65, 23, 5],
        "dict": {
            "mixed": {
                1: 43,
                2: 54.33,
                3: False,
                4: 9
                "string": "value"
            },
            "array": [3, 6, 4],
            "string": "value"
        }
    }
"""