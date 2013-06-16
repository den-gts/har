#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Den'

import xlrd
import datetime,re
from django.core.exceptions import ValidationError
from cards.models import Card,Project,Developer,Devision
LOG_FILE='f:\\db.log'


def convertExcelTime(ExcelTime,file):#функция конвертирования формата екселевского времени в формат базы данных
    startTime=datetime.date(1899, 12, 30)#кривой эксель отсчитывает от 0 января 1900г

    try:
        delta=datetime.timedelta(days=ExcelTime)
    except TypeError,err:
        print 'error in $s: $s' % file,ExcelTime
        ErrorInLog('[%s] Time:%s Error:%s\n'.decode('utf-8')%(file,ExcelTime,err))
        delta=datetime.timedelta(days=0)
    return startTime+delta

def xls2sql(source_path,source_file):

    har=source_file[0:-4]#значение характеристики позиции, источник-имя файла
    rb=xlrd.open_workbook("%s\%s"%(source_path,source_file),formatting_info=True)
    sheet=rb.sheet_by_index(0)

    #предотвращаем дублирование записей
#    sql="SELECT `har`,`decimal` FROM `cards` WHERE `har`=%d" % har
#    cursor.execute(sql)
#    data =  cursor.fetchall()
    data=Card.objects.filter(Har=har)
    sDecimal=[x['Decimal'] for x in data.distinct().values('Decimal')]#составляем список децимальный номеров, которые есть в БД
    fields=sheet.row_values(0)
    for rownum in range(1,sheet.nrows):
        row=sheet.row_values(rownum)

        if row[1] and row[5]:#поля Имя и дата не должны быть пустыми
            DecMore=""
            #проверка входнных данных
            try:
                row[0]='%03d'% int(row[0])
                for i in range(2,4):
                    if not row[i]:
                        ErrorInLog('[%s.%s]:поле %s пусто\n'.decode('utf-8')%(har,row[0],fields[i]))
            except ValueError,err:
                #если децималный номер нестандартный
                pat=re.compile(r"^(\d{1,3})((-|\.).*)")#патерн для рег. выражения. 2ая группа - допустимые символы
                #после которых идет дополнительная часть
                reResult=pat.match(row[0])
                if reResult:#Если децимальный номер не валидный то
                    row[0]=reResult.group(1)#разделяем децимальный номер на валидную часть
                    DecMore=reResult.group(2)#и не валидную
                else:
                    ErrorInLog('[%s.%s]:%s\n'.decode('utf-8')%(har,row[0],err))

            if not row[0] in sDecimal or DecMore.strip():#проверяем есть ли совпаедния с БД

                try:
                    row[5]=convertExcelTime(row[5],source_file)
                except TypeError:
                    ErrorInLog(u'[%s.%s]:Ошибка заполнения времени %s' % (har,row[0],row[5]))

                if row[2].strip:
                    xlsProject=Project.objects.get_or_create(Name=row[2])
                else:
                    xlsProject='Не указан'
                xlsDeveloper=Developer.objects.get_or_create(Name=row[3],
                    defaults={'Devision':Devision.objects.get_or_create(Name='КО')[0]})
                try:
                    save=Card(Har=har,Decimal=row[0],
                        DecimalMore=DecMore,
                        Name=row[1],
                        Project=xlsProject[0],
                        Developer=xlsDeveloper[0],
                        CreatingDate=row[5])
                    save.save()
                except ValueError, ValidationError:
                    logFile=open("f:\\db.log",'a')
                    logFile.write('[%s.%s]:Ошибка ввода в БД'%(har,row[0]))
                    print '[%s.%s]:Ошибка ввода в БД'%(har,row[0])
                    logFile.close()
                except :
                    print 'ошибка'
                    raise

def ErrorInLog(message):
    logFile=open(LOG_FILE,'a')
    logFile.write(message.encode('utf-8'))
    logFile.close()

