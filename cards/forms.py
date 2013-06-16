# -*- coding: utf-8 -*-

from django import forms
from cards.models import Developer,Project
from django.forms.extras.widgets import SelectDateWidget
import datetime,re

year = datetime.date.today().year

class AddCardForm(forms.Form):
    #TODO:проверить валидацию
    #Флаг обезательного поля
    req=True
    har=forms.CharField(label='Обозначение',max_length=6,required=req)
    name=forms.CharField(max_length=30, label='Наименование',required=req)
    ProjectForm=forms.ModelChoiceField(queryset=Project.objects.all(),empty_label='--------',label='Тема',required=req)
    DeveloperForm=forms.ModelChoiceField(queryset=Developer.objects.all(),empty_label='--------',label='Разработал',required=req)
    note=forms.CharField(max_length=255,widget=forms.Textarea,required=False,label='Заметка')

    #проверка поля Характеристика.
    def clean_har(self):
        har=unicode(self.cleaned_data['har'])
        if not har.isdigit():
            raise forms.ValidationError('Допустимы только цифры')
        return har

    def clean_name(self):
        name=unicode(self.cleaned_data['name'])

        return name.capitalize()

class SearchForm(AddCardForm):
    #делаем все поля необезательными
    req=False
    har=forms.CharField(label='Обозначение',max_length=10,required=req)#костыль!!!!!!
    Since=forms.DateField(label='Начало периода',required=False,widget=SelectDateWidget(years=range(year,1985,-1)))
    Before=forms.DateField(label='Окончание периода',
        required=False,
        widget=SelectDateWidget(years=range(year,1985,-1)),
        initial=datetime.date.today()
    )

    def clean_har(self):

        har=unicode(self.cleaned_data['har']).strip()
        if har:
            pat=re.compile(r"^(\d{,6})(\.(\d{,3}))?$")

            result=pat.match(har)

            if result:
                har=result.group(1,3)
            else:
                raise forms.ValidationError('Введенные данные не соответсвуют формату XXXXXX.XXX')


## Старый код проверки поля характеристики. Более сложен, но и более информативен. Отклчен из-за сложности.
#        if har:
#            if har.count('.')<=1:
#                #разбиваем характеристику на 2 части
#                parts=har.split('.')
#                #цикл для левой и правой части характеристики
#                for p in parts:
#                    if not p.isdigit():
#                        #если не цифры то ошибка
#                        raise forms.ValidationError('Допустимы только цифры')
#
#                if len(parts[0])!=6 and har.count('.')!=0:
#                    raise forms.ValidationError('Количество знаков до точки должно быть 6 знаков')
#                if isinstance(har,list) and len(parts[1])!=3:
#                    raise forms.ValidationError('Количество знаков после точки должно быть 3 знака')
#                har=parts
#            else:
#                raise forms.ValidationError('Точка может быть только одна')
#            if len(har)==1:
#                har=int(har[0])
        return har




