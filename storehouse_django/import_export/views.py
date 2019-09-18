from django.shortcuts import render
import django_excel as excel # without this does not work %)
import pyexcel as pe
from pyexcel_webio import make_response

from places import models as places_models

def make_places_sheet(model):
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
    sheet.name = 'Места'
    sheet.row += first_row
    sheet.row += ['']

    for place in sorted(model.objects.all(), key=lambda t: t.full_humanid):
        parent = ''
        if place.place:
            parent = place.place.full_humanid

        sheet.row += [
            place.full_humanid,
            '',
            parent,
            place.comment,
            '',
            '',
            place.opening_type.humanid,
            place.formfactor.humanid,
            place.humanid,
        ]

    return sheet

def make_opening_types_sheet(model):
    first_row = [
        'Код',
        'Комментарий',
    ]
    
    sheet = pe.Sheet()
    sheet.name = 'Типы открытия'
    sheet.row += first_row
    sheet.row += ['']

    for place in model.objects.all().order_by('humanid'):


        sheet.row += [
            place.humanid,
            place.comment,
        ]

    return sheet

def make_formfactros_sheet(model):
    first_row = [
        'Код',
        'Комментарий',
        '',
        'наружние',
        'Ш, мм',
        'В, мм',
        'Г, мм',
        'внутренние',
        'Ш, мм',
        'В, мм',
        'Г, мм',
        'Пустой вес, г',
        'Максимальный вес содержимого, г',
        '',
        'Внешний объём',
        'Внутренний объём',
    ]
    
    sheet = pe.Sheet()
    sheet.name = 'Типоразмеры'
    sheet.row += first_row
    sheet.row += ['']

    for place in model.objects.all().order_by('humanid'):


        sheet.row += [
            str(place.humanid),
            place.comment,
            '',
            '',
            place.outside_width,
            place.outside_height,
            place.outside_depth,
            '',
            place.inside_width,
            place.inside_height,
            place.inside_depth,
            place.empty_weight,
            place.contents_weight_max,
            '',
            place.outside_volume,
            place.inside_volume,
        ]

    return sheet

def export_data(request, atype):
    places = make_places_sheet(places_models.StoragePlace)
    opening_types = make_opening_types_sheet(places_models.OpeningType)
    formfactros = make_formfactros_sheet(places_models.Formfactor)

    book = places + opening_types + formfactros

    return make_response(book, 'ods', status=200, file_name='sheet')
