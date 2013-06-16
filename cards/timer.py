# -*- coding: cp1251 -*-
#функция подсчета разницы во времени между past и present
import time
def strTimer(past,present):
    timer1=time.gmtime(past)
    timer2=time.gmtime(present)
    difer=range(9)
    description=[u'г',u'мес',u'д',u'ч',u'мин',u'сек']
    maxVal=[99,12,31,23,59,59]
    for n in difer:
        difer[n]=int(timer2[n])-int(timer1[n])
    result=""
    for n in range(len(difer)):
        if difer[5-n]<0:
            difer[4-n]=difer[4-n]-1
            difer[5-n]=maxVal[5-n]+difer[5-n]
    for n in range(len(difer)):
        if difer[5-n]!=0:
            result=("%i%s. %s")%(difer[5-n],description[5-n],result)
            
    return result
    
