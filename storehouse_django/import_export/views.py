from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
import django_excel as excel # without this does not work %)
import pyexcel as pe
from pyexcel_webio import make_response

from places import models as places_models
from items import models as items_models

from .forms import DocumentForm

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
        '',
        'Объём',
        'Использованный объём',
        'Свободный объём',
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
            '',
            place.volume,
            place.used_volume,
            place.free_volume,
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

def make_items_sheet(model):
    first_row = [
        'Код',
        'Комментарий',
        '',
        'Имя',
        'tsubtype',
        'itcomment',
        '',
        'Количество',
        'Место',


    ]

    sheet = pe.Sheet()
    sheet.name = 'Предметы'
    sheet.row += first_row
    sheet.row += ['']

    for item in model.objects.all():
        if item.itemtype:
            name = item.itemtype.name
            tsubtype = item.itemtype.tsubtype
            itcomment = item.itemtype.comment
        else:
            name = 'n/a'
            tsubtype = 'n/a'
            itcomment = 'n/a'
            

        sheet.row += [
            item.humanid,
            item.comment,
            '',
            name,
            tsubtype,
            itcomment,
            '',
            item.count,
            item.place.full_humanid,

        ]

    return sheet

def export_data(request, atype):
    places = make_places_sheet(places_models.StoragePlace)
    opening_types = make_opening_types_sheet(places_models.OpeningType)
    formfactros = make_formfactros_sheet(places_models.Formfactor)
    items = make_items_sheet(items_models.Item)

    book = places + opening_types + formfactros + items

    return make_response(book, 'ods', status=200, file_name='sheet')

def import_openingtype(sheet):
    places_models.OpeningType.objects.all().delete()
    for row in sheet.row[1:]:
        if (row[0]) and (sheet.row[0]!=''):
            record = places_models.OpeningType(humanid=row[0], comment=row[1])
            record.save()
            print(record)

def import_formfactor(sheet):
    places_models.Formfactor.objects.all().delete()
    for row in sheet.row[1:]:
        if (row[0]) and (sheet.row[0]!=''):
            if row[4] != '':
                outside_width = row[4]
            else:
                outside_width = None

            if row[5] != '':
                outside_height = row[5]
            else:
                outside_height = None

            if row[6] != '':
                outside_depth = row[6]
            else:
                outside_depth = None

            if row[8] != '':
                inside_width = row[8]
            else:
                inside_width = None

            if row[9] != '':
                inside_height = row[9]
            else:
                inside_height = None

            if row[10] != '':
                inside_depth = row[10]
            else:
                inside_depth = None

            if row[11] != '':
                empty_weight = row[11]
            else:
                empty_weight = None

            if row[12] != '':
                contents_weight_max = row[12]
            else:
                contents_weight_max = None

            record = places_models.Formfactor(
                humanid = int(row[0]),
                comment = row[1],
                outside_width = outside_width,
                outside_height = outside_height,
                outside_depth = outside_depth,

                inside_width = inside_width,
                inside_height = inside_height,
                inside_depth = inside_depth,

                empty_weight = empty_weight,
                contents_weight_max = contents_weight_max,
            )
            record.save()
            print(record)

def import_storageplace(sheet):
    places_models.StoragePlace.objects.all().delete()
    for row in sheet.row[1:]:
        if (row[0]) and (sheet.row[0]!=''):
            '''
            0place.full_humanid,
            1'',
            2parent,
            3 place.comment,
            4'',
            5'',
            6place.opening_type.humanid,
            7place.formfactor.humanid,
            8place.humanid,
            '',
            place.volume,
            place.used_volume,
            place.free_volume,
            '''

            opening_type = places_models.OpeningType.objects.filter(humanid=row[6])[0]

            if row[7] != '':
                formfactor_humanid = row[7]
            else:
                formfactor_humanid = 0

            formfactor = places_models.Formfactor.objects.filter(humanid=int(formfactor_humanid))[0]

            record = places_models.StoragePlace(
                comment = row[3],
                humanid = row[8],
                opening_type = opening_type,
                formfactor = formfactor,
            )
            try:
                record.save()
            except:
                print(row)
            else:
                print(record)

    for row in sheet.row[1:]:
        if (row[0]) and (sheet.row[0]!='') and (row[2]) and (row[2] != ''):
            #record = places_models.StoragePlace.objects.filter(full_humanid = row[0])
            record = [obj for obj in places_models.StoragePlace.objects.all() if obj.full_humanid == row[0]][0]
            parent = [obj for obj in places_models.StoragePlace.objects.all() if obj.full_humanid == row[2]][0]
            #parent = places_models.StoragePlace.objects.filter(full_humanid = row[2])
            record.pace = parent

def import_items(sheet):
    for row in sheet.row[2:]:
        # check-add ItemType
        # items_models.Item
        itemtype = items_models.ItemType.objects.filter(name=row[3])
        if not itemtype:
            itemtype_record = items_models.ItemType(
                name = row[3],
                tsubtype = row[4],
                comment = row[5],
            )
            try:
                itemtype_record.save()
            except:
                print(row)
            else:
                print(itemtype_record)

        itemtype = items_models.ItemType.objects.filter(name=row[3])[0]
        # add Item
        place = [obj for obj in places_models.StoragePlace.objects.all() if obj.full_humanid == row[8]]
        kwargs = {}
        if place:
            kwargs['place'] = place[0]

        kwargs['itemtype'] = itemtype
        if (row[0]) and (row[0] != ''):
            kwargs['humanid'] = row[0]

        if (row[1]) and (row[1] != ''):
            kwargs['comment'] = row[1]

        if (row[7]) and (row[7] != ''):
            kwargs['count'] = int(row[7])

        item_record = items_models.Item(**kwargs)

        try:
            item_record.save()
        except:
            print(row)
        else:
            print(item_record)




def import_data(book):
    #['Места', 'Предметы', 'Типоразмеры', 'Типы открытия']
    if 'Типы открытия' in book.sheet_names():
        import_openingtype(book['Типы открытия'])

    if 'Типоразмеры' in book.sheet_names():
        import_formfactor(book['Типоразмеры'])

    if 'Места' in book.sheet_names():
        import_storageplace(book['Места'])

    if 'Предметы' in book.sheet_names():
        import_items(book['Предметы'])


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['docfile']
            print(filehandle)
            book = pe.get_book(file_content=filehandle, file_type='ods')
            #print(book)
            #print(dir(book))
            #print(book.sheet_names())
            import_data(book)
            #newdoc = Document(docfile = request.FILES['docfile'])
            #newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Render list page with the documents and the form
    return render(request, 'list.html', {'form': form})
