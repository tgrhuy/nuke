# -*- coding: utf-8 -*-
import socket
import os


HOST = '192.168.1.193'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(ADDR)
serv.listen(5)
print ('listening ...')

def makefile(imagefile, outmovfile, nk_path, new_nk_path):
    content = open(nk_path, "r").read()
    content = content.replace('C:/Users/zt007/Desktop/asdf.png', imagefile)
    content = content.replace('z:/test/tc.png', outmovfile)
    with open(new_nk_path, "w") as f:
     f.write(content)
    return new_nk_path

filepath = '/root/jiaobiao/NK_prj/ads_updata/'


while True:
  conn, addr = serv.accept()
  print ('client connected ... ', addr)
  while True:
    data = conn.recv(BUFSIZE)
    if not data:
        break
    print(data)
    fileinfo = bytes.decode(data)

    cmd,filename,filesize = fileinfo.split('|')
    filefullpath = filepath+filename.split('.')[0]+'_01.'+filename.split('.')[-1]

    f = open(filefullpath, 'wb')
    cont = 0

    while cont != int(filesize):
      data = conn.recv(BUFSIZE)
      f.write(data)
      # print('writing file ....')
      cont+=len(data)
      # print(cont,int(filesize),len(data))
    f.close()
    print (cont,int(filesize))
  print ('finished writing file')

  outmovfile = '/var/www/threeJS/three.js/ads/e.png'

  nk_path = '/root/jiaobiao/NK_prj/NK/'+cmd+'.nk'
  new_nk_path = nk_path.split('.')[0]+'_'+filename.split('.')[0]+'.'+nk_path.split('.')[1]

  makefile(filefullpath,outmovfile,nk_path,new_nk_path)





  conn.close()
  os.system('''/usr/local/Nuke10.5v4/Nuke10.5  -remap "Z:/角标植入/ZZZ/,/root/jiaobiao/NK_prj/source/" -F 1-1 -x ''' + new_nk_path)


  print ('client disconnected')
