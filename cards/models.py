# -*-coding: utf-8 -*-
from django.db import models


# Create your models here.

#Проекты
class Project(models.Model):
    Name=models.CharField(max_length=15,verbose_name='Название')

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ["Name"]
        verbose_name='Проект'
        verbose_name_plural='Проекты'

#Отделы
class Devision(models.Model):
    Name=models.CharField(max_length=15,verbose_name='Название')

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ["Name"]
        verbose_name='Отдел'
        verbose_name_plural='Отделы'


#Разработчики
class Developer(models.Model):
    Name=models.CharField(max_length=20,verbose_name='Название')
    Devision=models.ForeignKey(Devision,default=0,verbose_name='Отдел')

    def __unicode__(self):
        return self.Name

    class Meta:
        ordering = ["Name"]
        verbose_name='Разработчик'
        verbose_name_plural='Разработчики'


#Сами элементы карточки
class Card(models.Model):
    Har=models.CharField(max_length=6,verbose_name='Характеристика')
    Decimal=models.DecimalField(verbose_name='Децимальный номер',max_digits=3,decimal_places=0)
    DecimalMore=models.CharField(max_length=10)
    Name=models.CharField(max_length=30,verbose_name='Наименование')
    Project=models.ForeignKey(Project,verbose_name='Проект')
    Developer=models.ForeignKey(Developer,verbose_name='Разработал')
    CreatingDate=models.DateField(verbose_name='Дата создания')
    Note=models.CharField(max_length=60,blank=True,verbose_name='Примечание')


    def __unicode__(self):
        return "%s.%s %s" % (self.Har,self.Decimal,self.Name)

    class Meta:
        ordering = ["Har","Decimal"]
        verbose_name='Карточка'
        verbose_name_plural='Карточки'







