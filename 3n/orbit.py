#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
import subprocess
import shlex
import shutil
import urllib.request
import numpy as np


def input_bd(bd,kluchi,file,f):
    l = len(kluchi)
    for line in file:
        line_el = line.replace('\n','').replace('      ',' ').replace('     ',' ').replace('    ',' ')\
            .replace('   ',' ').replace('  ',' ').lstrip().split(' ')
        kd={}
        for i in range(l):
            if kluchi[i]=='nRMax':
                kd[kluchi[i]]=int(line_el[i])
            else:
                kd[kluchi[i]]=np.float64(line_el[i])
        bd.append(kd)
    print('загружено {0} моментов(данных по телам в эти моменты) из файла {1}'.format(len(bd),f))

def lenOrbit(bd,kluchi,f):
    kd={}
    l_pryam = {1:0.0,2:0.0,3:0.0}
    l_pryam_q2 = {1:0.0,2:0.0,3:0.0}
    l_trop = {1:0.0,2:0.0,3:0.0}
    l_ = {1:0.0,2:0.0,3:0.0}
    for i in range(len(kluchi)):
        if kluchi[i]=='nRMax':
            kd[kluchi[i]]=int(0)
        else:
            kd[kluchi[i]]=np.float64(11)
    for i in bd:
        if kd['x1'] != 11.0 :
            for j in [1,2,3]:
                l_pryam[j] += np.sqrt(
                    np.power(i['x{0}'.format(j)] - kd['x{0}'.format(j)],2) +
                    np.power(i['y{0}'.format(j)] - kd['y{0}'.format(j)],2) +
                    np.power(i['z{0}'.format(j)] - kd['z{0}'.format(j)],2) )
                #l_pryam_q2[j] += np.fabs(i['x{0}'.format(j)] - kd['x{0}'.format(j)]) + np.fabs(i['y{0}'.format(j)] - kd['y{0}'.format(j)]) + np.fabs(i['z{0}'.format(j)] - kd['z{0}'.format(j)])
                t = np.float64(i['t'] - kd['t'])
                l_trop[j] += np.sqrt(
                    np.power((i['vx{0}'.format(j)] + kd['vx{0}'.format(j)])/2.0*t,2) +
                    np.power((i['vy{0}'.format(j)] + kd['vy{0}'.format(j)])/2.0*t,2) +
                    np.power((i['vz{0}'.format(j)] + kd['vz{0}'.format(j)])/2.0*t,2) )
                #l_trop[j] += l_[j]
            #print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(l_trop[1],l_trop[2],l_trop[3] ,i['t'], kd['t'],t))
        for j in kluchi:
            kd[j] = i[j]

    for i in [1,2,3]:
        print('N{2} l1 = {0}, \tl_trop = {1} '.format(l_pryam[i],l_trop[i],i))



def orbit(file, f):
    out = open("./len/"+f,'w')
    kluchi = ['t','x1','x2','x3','y1','y2','y3','z1','z2','z3','vx1','vx2','vx3','vy1','vy2','vy3','vz1','vz2','vz3',\
              'Eox2','Ex2','r1','r2','r3','rMax','nRMax','fiMax']
    bd=[]
    input_bd(bd,kluchi,file,f)
    lenOrbit(bd,kluchi,f)
    out.write ('')
    out.close()



cmd = "ls"
args = shlex.split(cmd)
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
cmd = "mkdir len"
args = shlex.split(cmd)
subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
files = p.communicate()[0].decode('utf-8').rstrip('\n').split('\n')
for f in files:
    if f != "orbit.py" and f != "out.txt" and f != "len" and f != "man":
        file = open(f,'r')
        orbit(file,f)
        file.close()
