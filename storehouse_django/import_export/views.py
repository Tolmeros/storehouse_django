from django.shortcuts import render
import django_excel as excel # without this does not work %)
import pyexcel as pe
from pyexcel_webio import make_response

from places import models as places_models


def export_data(request, atype):
    model = places_models.StoragePlace
    '''
    StoragePlace.objects.all()[0].opening_type.humanid
    StoragePlace.objects.all()[0].formfactor.humanid
    StoragePlace.objects.all()[0].humanid - пробовать разложить на "серия" и "номер"
    StoragePlace.objects.all()[0].full_humanid
    StoragePlace.objects.all()[0].comment

    StoragePlace.objects.all()[0].place
    StoragePlace.objects.all()[0].inside_places.all()
    '''

    first_row = [
        'Код',
        'Цвет (заменить на фактура или подходящее',
        'Внутри в',
        'Комментарий',
        '',
        '',
        'Тип открытия',
        'Типоразмер',
        'Серия,Номер',
    ]
    
    sheet = pe.Sheet()
    sheet.row += first_row
    sheet.row += []

    for place in model.objects.all():
        parent = ''
        if place.place:
            parent = place.place.full_humanid

        sheet.row += [
            place.full_humanid,
            '',
            parent,
            place.comment,
            place.opening_type.humanid,
            place.formfactor.humanid,
            place.humanid,
        ]

    return make_response(sheet, 'ods', status=200, file_name='sheet')
