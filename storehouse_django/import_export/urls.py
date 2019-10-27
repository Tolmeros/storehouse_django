from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^export/(.*)', views.export_data, name="export"),
    url(r'^import/', views.list, name='list')

]
