
def create_track(outfile):
    outfile.write("from common import *\n")
    ft = '''def __ascii_%d(s, d=100):\n if d ==0 or len(s) == 0: raise NonePattern("") \n else: track_map[ord(s[0])](s[1:], d - 1)\n'''
    for i in range(0, 255):
        outfile.write(ft % i)

def create_map(outfile):
    ft = '''track_map = %s'''
    s = str([ "__ascii_%d" % i for i in range(0, 255)])
    s = s.replace('\'', '')
    s += '\n'
    outfile.write(ft % s)
    ft = '''def ascii(s, d=100):\n if d ==0 or len(s) == 0: raise Exception("") \n else: track_map[ord(s[0])](s[1:], d - 1)\n'''
    outfile.write(ft)

# with open("track_map.py","w") as fd:
#     create_track(fd)
#     create_map(fd)

# import track_map
# track_map.ascii("abc")
# l = [345,336,336,351,99,186,99,372,42,33,30,335]

def map_to_str(l = []):
    s = ""
    if len(l) == 0:
        return ""
    else:
        l[len(l) - 1] += 1
    for c in l:
        if c >= 3:
            s += chr(c/3-1)
    print s

import re
def track_to_list(s = ''):
    return [int(i) for i in re.findall(r'\d+', s)]


with open("track_data.txt","r") as fd:
    s = fd.read()
    l = track_to_list(s)
    ma = max(l)
    mi = min(l)
    map_to_str(l)