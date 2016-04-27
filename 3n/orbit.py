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
        line_el = line.replace('\n','').replace('      ',' ').replace('     ',' ').replace('    ',' ').replace('   ',' ').replace('  ',' ').lstrip().split(' ')
        kd={}
        for i in range(l):
            if kluchi[i]=='nRMax':
                kd[kluchi[i]]=int(line_el[i])
            else:
                kd[kluchi[i]]=float(line_el[i])
        bd.append(kd)
    print('загружено {0} моментов(данных по телам в эти моменты) из файла {1}'.format(len(bd),f))

def lenOrbit(bd,kluchi,f):
    kd={}
    l_pryam = {1:0.0,2:0.0,3:0.0}
    l_pryam_q2 = {1:0.0,2:0.0,3:0.0}
    l_trop = {1:0.0,2:0.0,3:0.0}
    for i in range(len(kluchi)):
        if kluchi[i]=='nRMax':
            kd[kluchi[i]]=int(0)
        else:
            kd[kluchi[i]]=float(11)
    for i in bd:
        if kd['x1'] != 11.0 :
            l_pryam[1] += np.power(np.power(i['x1'] - kd['x1'],2) + np.power(i['y1'] - kd['y1'],2) + np.power(i['z1'] - kd['z1'],2),1.0/2.0)
            l_pryam[2] += np.power(np.power(i['x2'] - kd['x2'],2) + np.power(i['y2'] - kd['y2'],2) + np.power(i['z2'] - kd['z2'],2),1.0/2.0)
            l_pryam[3] += np.power(np.power(i['x3'] - kd['x3'],2) + np.power(i['y3'] - kd['y3'],2) + np.power(i['z3'] - kd['z3'],2),1.0/2.0)
            l_pryam_q2[1] += np.fabs(i['x1'] - kd['x1']) + np.fabs(i['y1'] - kd['y1']) + np.fabs(i['z1'] - kd['z1'])
            l_pryam_q2[2] += np.fabs(i['x2'] - kd['x2']) + np.fabs(i['y2'] - kd['y2']) + np.fabs(i['z2'] - kd['z2'])
            l_pryam_q2[3] += np.fabs(i['x3'] - kd['x3']) + np.fabs(i['y3'] - kd['y3']) + np.fabs(i['z3'] - kd['z3'])
            t = i['t'] - kd['t']
            l_trop[1] += np.power( np.power((i['vx1'] + kd['vx1'])/2.0*t,2)+np.power((i['vy1'] + kd['vy1'])/2.0*t,2)+np.power((i['vz1'] + kd['vz1'])/2.0*t,2),1.0/2.0)
            l_trop[2] += np.power( np.power((i['vx2'] + kd['vx2'])/2.0*t,2)+np.power((i['vy2'] + kd['vy2'])/2.0*t,2)+np.power((i['vz2'] + kd['vz2'])/2.0*t,2),1.0/2.0)
            l_trop[3] += np.power( np.power((i['vx3'] + kd['vx3'])/2.0*t,2)+np.power((i['vy3'] + kd['vy3'])/2.0*t,2)+np.power((i['vz3'] + kd['vz3'])/2.0*t,2),1.0/2.0)
        for j in kluchi:
            kd[j] = i[j]
    for i in [1,2,3]:
        print('N{3} l1 = {0}, \tl_trop = {1} \t l1 / l_trop = {4}'.format(l_pryam[i],l_trop[i],l_pryam_q2[i],i,l_pryam[i]/l_trop[i],l_trop[i]/l_pryam_q2[i],l_pryam_q2[i]/l_pryam[i]))



def orbit(file, f):
    out = open("./len/"+f,'w')
    kluchi = ['t','x1','x2','x3','y1','y2','y3','z1','z2','z3','vx1','vx2','vx3','vy1','vy2','vy3','vz1','vz2','vz3','Eox2','Ex2','r1','r2','r3','rMax','nRMax','fiMax']
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
