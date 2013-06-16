# -*-coding: utf-8 -*-
from django.contrib import admin
from cards.models import *

class CardAdmin(admin.ModelAdmin):
    #list_display = ('Har','Decimal','Name','Project','Developer','CreatingDate','Note')
    search_fields =('Har','Decimal','Name','Project','Developer','CreatingDate','Note')
    fieldsets = (
        (None,{
            'classes':['wide'],
            'fields':(('Har','Decimal'),'Name','Project','Developer','CreatingDate','Note'),
        }),
    )



admin.site.register(Card,CardAdmin)
admin.site.register(Developer)
admin.site.register(Project)
admin.site.register(Devision)
