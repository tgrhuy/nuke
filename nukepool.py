import os, shutil,re,json
import threading
import math
import time
import sys
import multiprocessing



def getwitnode(nukefile):
    content = open(nukefile, "r").read()
    ss = re.findall(r"Write {(.+?)}", content,re.S)  #
    renderNode = []
    tasklist = []
    Frange = 5
    for i in ss:
        i = i.replace('\n','",')
        i = i.replace(' ', '":"')
        i = i.replace('",":"','","')
        i = i[2:-1]
        i = "{"+i+"}"
        renderNode .append(json.loads(i))
    for i in renderNode:
        start = 0
        while start < int(i['last']):
            if start == 0:
                tasklist.append([i['name'], [start, start + math.floor(int(i['last']) / Frange)]])
            else:
                tasklist.append([i['name'], [start + 1, start + math.floor(int(i['last']) / Frange)]])
            start += math.floor(int(i['last']) / Frange)


    pool = multiprocessing.Pool(processes=8)
    for i in tasklist:

        # print(nuke_render(nukefile, i[0], i[1]))
        pool.apply_async(nuke_render, (nukefile, i[0], i[1]))

    pool.close()
    pool.join()


def nuke_render(nukepath,notes,st_end):
    s_e = str(st_end[0])+"-"+str(st_end[1])
    # os.system("Nuke10.5 -F 0-68 -X "+notes+" -x " + nukepath)
    os.system('"C:/Program Files/Nuke10.5v4/Nuke10.5.exe" -F '+s_e+" -X   "+notes+"   -x " + nukepath)
    # print('"C:/Program Files/Nuke10.5v4/Nuke10.5.exe" -F '+s_e+" -X   "+notes+"   -x " + nukepath)
if __name__ == '__main__':
    nukefile = sys.argv[1]
    # nukefile = 'E:/model/comp/xiu.nk'
    getwitnode(nukefile)