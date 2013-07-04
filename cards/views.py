# -*- coding: utf-8 -*-
# Create your views here.
import os
from django.shortcuts import render_to_response, HttpResponse
from django.core.paginator import  Paginator,PageNotAnInteger,EmptyPage
from cards.forms import AddCardForm,SearchForm
from cards.models import Card
from django.views.decorators.csrf import csrf_exempt
import datetime


def getSearchResult(form):
    #делаем поля необезательными.. криво, не явно, но лучшего способа не нашел
    for item in form.fields.values():
        item.required = False
    SearchResult = None
    if form.is_valid():
        cd = form.cleaned_data
        SearchResult = Card.objects
        EmptyForm = True
        # для обозначения отдельные манипуляции. Так как оно состоит из характеристики и децимального номера
        # разделенные точкой. В форме одно поле har,  а в модели 2 поля har и Decimal
        if cd['har']:
            EmptyForm = False
            SearchResult = SearchResult.filter(Har__contains=cd['har'][0])
            if cd['har'][1]:  # если есть децимальная часть то записываем ее
                SearchResult = SearchResult.filter(Decimal__contains=cd['har'][1])
            print cd['har']
        # Словарь соответсвия полей модели с полями формы
        ConfList = {'Name__contains':cd['name'],
                    'Project': cd['ProjectForm'],
                    'Developer': cd['DeveloperForm'],
                    'Note__contains': cd['note'],
                    'CreatingDate__gte': cd['Since'],
                    'CreatingDate__lte': cd['Before'],
        }
        #Цикл формирования запросов поиска.
        for listKey in ConfList:
            if ConfList[listKey]:
                EmtpyForm = False
                SearchResult = SearchResult.filter(**{listKey: ConfList[listKey]})
        #Если форма пустая тогда отображаем все записи
        if EmptyForm:
            SearchResult = SearchResult.all()
    return SearchResult


def show_all(request,template_name='show_card.html'):
    items=Card.objects.all()
    return render_to_response(template_name,{'items':items})

@csrf_exempt
def add_card(request,template_name='add_card.html',result_template='result_add.html'):
    if request.method=='POST':
        form=AddCardForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data

            # вычисление децимального номера

            #находим все записи с заданной характеристикой, сортируем в обратном порядке
            FndItm=Card.objects.filter(Har=cd['har']).order_by('Decimal')
            if FndItm:
                listDecimal=[]
                #если такая характеристика есть
                for item in FndItm:#составляем список децимальных номеров из БД
                    listDecimal.append(item.Decimal)
                listDecimal=list(set(listDecimal))#удаляем дубликаты.
                RsltDec=firstHole(listDecimal)#ищем окно,если нет то прибавляем к последнему децимальному 1
            else:
                # если такой характеристики раньше не было, устанавливаем децимальный =001
                RsltDec = 1

            #вносим данные в БД
            Result = Card(Har=cd['har'],
                          Decimal=RsltDec,
                          Name=cd['name'],
                          Project=cd['ProjectForm'],
                          Developer=cd['DeveloperForm'],
                          CreatingDate=datetime.date.today(),
                          Note=cd['note']
            )
            Result.save()
            return render_to_response(result_template,{'ItemList':FndItm,'AddedItem':Result})

    else:
        form=AddCardForm()
    return render_to_response(template_name, {'form':form})


def search(request, template_name='search.html'):
    if request.GET:  # проверяем первый ли запуск страницы поиска
        form = SearchForm(request.GET)
        SearchResult = getSearchResult(form)
        request.session['result'] = SearchResult
        # формирование постраничного вывода результатов поиска
        paginator = Paginator(SearchResult, 25)  # второй аргумент - количество элементов на странице
        page = request.GET.get('page')

        try:
            SearchResult = paginator.page(page)
        except PageNotAnInteger:
            SearchResult = paginator.page(1)
        except EmptyPage:
            SearchResult = paginator.page(paginator.num_pages)
        # составляем последнюю часть URL с данными формы для постраничной навигации
        DictRequest = dict(request.GET)
        if 'page' in DictRequest:
            DictRequest.pop('page')
        Referer = ''
        for key, value in DictRequest.items():
            if Referer:
                Referer += '&'
            Referer += "%s=%s" % (key, value[0])
        SearchResult.has_previous()
        return render_to_response(template_name, {'form': form,
                                                  'Result': SearchResult,
                                                  'requestGET': True,
                                                  'LimitNPages': getLimitPageRange(paginator,page),
                                                  'Referer': Referer,
                                                })
    else:  # если первый запуск
        form = SearchForm()
    return render_to_response(template_name, {'form': form})


def show_cur_path(request):
    return HttpResponse("path:"+os.curdir)


def getLimitPageRange(dataList, page):
    if not page: page = 1
    LIMIT = 4
    left = int(page)-LIMIT-1
    right = int(page)+LIMIT
    if left < 0:
        left = 0
    if right > dataList.num_pages:
        right = dataList.num_pages
    return dataList.page_range[left:right]


def firstHole(data):  # функция определения первой "дыры" в последовательности. например 1,2,3,5. Вернет 4
    if type(data) != tuple and type(data) != list:
        raise TypeError('given %s.list or tuple excepcted.' % str(type(data)))
    prv = 0

    for i in data:
        if prv != i-1:
                break
        prv = i
    return prv+1


def exportCSV(request):
    import csv
    SearchResult = request.session['result']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="har.csv"'
    CSVwriter = csv.writer(response,delimiter=';')
    # Cp1251 все для творния Microsoft с их кодиировкой
    CSVwriter.writerow([x.encode('cp1251') for x in u'Обозначение', u'Наименование', u'Разработал', u'Проект', u'Дата'])
    for row in SearchResult:
        CSVwriter.writerow(["%s.%03d%s" % (row.Har, int(row.Decimal), row.DecimalMore),
                            unicode(row.Name).encode('cp1251'),
                           unicode(row.Developer).encode('cp1251'),
                           unicode(row.Project).encode('cp1251'),
                           row.CreatingDate.strftime('%d.%m.%Y'),])
    return response