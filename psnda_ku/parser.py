#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import urllib.request
import shutil
import numpy as np

n = 10
#n меньше этого числа
bd = []

def load_planet(file):
    with file:
        head=file.readline()
        header = head.replace('# ','').replace(' ','_').replace('\n','').split('\t')
        l = len(header)
        j = 0
        for line in file:
            line_el = line.replace('\n','').split('\t')
            kd={}
            for i in range(l):
                kd[header[i]]=line_el[i]
            bd.append(kd)
            j+=1
        print('Всего',j,'экзопланет загружено.')
def d_url():
    url = 'http://exoplanet.eu/catalog/dat/'
    destination = 'exoplanet.eu_catalog.dat'
    urllib.request.urlretrieve(url, destination)
def mantisa(st, step):
    i=0
    p=0
    while p!=1:
        if st[i] != '0' and st[i] !='.':
            p=1
        i+=1
    i-=1
    if i > step:
        return i
    else:
        return step
def findzero(st):
    step = st.find('.')
    if step != -1:
        step = 1 + mantisa(st,step)
        step_ziro = st.find('0',step)
        if step_ziro != -1:
            return st[:step_ziro+1]
    return st
def findnine(st):
    step = st.find('.')
    if step != -1:
        step = 1 + mantisa(st,step)
        step_nine = st.find('9',step)
        while step_nine != -1 and (st[step_nine-1] == '9' or st[step_nine-1] == '.'):
            step_nine = st.find('9',step_nine+1)
        if step_nine != -1:
            return st[:step_nine-1]+str(int(st[step_nine-1])+1)
    return st
def okruglenie():
    for planet in bd:
        old = planet['orbital_period']
        if '0' in planet['orbital_period']:
            planet['orbital_period']=findzero(planet['orbital_period'])
        if '9' in planet['orbital_period']:
            planet['orbital_period']=findnine(planet['orbital_period'])
        #if planet['orbital_period'] != '':
        #    planet['orbital_period']=float(planet['orbital_period'])
        #else:
        #    planet['orbital_period']=None
def otnPeriod(k_set,nn):
    stek=set()
    for i in range(nn-1):
        for ii in range(nn-1):
            stek.add((i+1) / (ii+1))
    for i in stek:
        k_set+=[i]
    k_set.sort()
#    for i in k_set:
#        print (i)
def starSPanet(bdStar):
    for ex in bd:
        if ex['star_name'] not in bdStar.keys():
            bdStar[ex['star_name']]=[]
        bdStar[ex['star_name']].append(ex)

    jst=0
    for st in bdStar:
        jst+=1
    print ('Всего',jst,'звезд с планетами.')
def findRezonans(bdStarSist):
    jstsis=0

    for st in bdStar:
        if len(bdStar[st]) > 1 :
            jstsis+=1
            for pl0 in bdStar[st]:
                if pl0['orbital_period'] !='':
                    for pl1 in bdStar[st]:
                        if pl0['name'] != pl1['name'] and pl1['orbital_period']!='':
                            #print (pl0['orbital_period'],pl1['orbital_period'])
                            if period(pl0['orbital_period'],pl1['orbital_period']):
                                #есть резонанс!
                                if st not in bdStarSist:
                                    bdStarSist[st]=[]
                                    bdStarSist[st]=bdStar[st]
    print ('Звезд с двумя и более планетами:',jstsis)
    print('Звезд с планетами у которых резонансными периодами',len(bdStarSist))


def period(p0,p1):
#    print (float(p0) / float(p1),float(p1) / float(p0),sep='\t')
    if float(p0) / float(p1) in k_set or float(p1) / float(p0) in k_set:
        return True
    else:
        return False
#    for i in k:
#        print (i)


try:
    file = open('exoplanet.eu_catalog.dat' ,'r')
except IOError as e:
    print(u'Не удалось открыть файл с базой данных по экзопланетам\nПопробуем загрузить из сети...')
    d_url()
    print('Загрузка завершена.')
    file = open('exoplanet.eu_catalog.dat' ,'r')
else:
    flag = input(u'Желаете обновить базу данных по экзопланетам из сети?(y/n): ')
    if (flag.lower() not in {'n','not','ne','nee','no','not','noo'}):
        shutil.copy('exoplanet.eu_catalog.dat', 'exoplanet.eu_catalog.dat.old')
        d_url()
        print('Обновление выполнено.')

load_planet(file)
okruglenie()
k_set=[]
otnPeriod(k_set,n)


bdStar={}
starSPanet(bdStar)

bdStarSist={}
findRezonans(bdStarSist)

for st in bdStarSist:
    for pl in bdStarSist[st]:
#        print ('зв({0})-пл({1}):    \tst_r = {2} st_Teff = {3}'.format(st, pl['name'], pl['star_radius'],pl['star_teff']),end=' ')
        zz=-1
        if (pl['star_radius']) != '' and pl['star_teff'] != '':
            zz=float(pl['star_radius'])*float(pl['star_teff'])*float(pl['star_teff'])/36000000
        print ('З.ж. зв: {0}'.format(zz),end='\t')
        if pl['semi_major_axis'] != '' and pl['eccentricity'] != '':
            apa= (1+float(pl['eccentricity']))*float(pl['semi_major_axis'])
            peri = (1-float(pl['eccentricity']))*float(pl['semi_major_axis'])
            print('peri = {0}, apa = {1}'.format(peri,apa),end='')
        print('')
