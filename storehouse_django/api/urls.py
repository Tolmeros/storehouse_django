from django.conf import settings
from django.urls import include, path
#from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from . import views

urlpatterns = []
schema_view = get_schema_view(title='Pastebin API')

router = DefaultRouter()


router.register(
    r'formfactor',
    views.FormfactorViewSet,
    base_name='formfactor'
)

router.register(
    r'openingtype',
    views.OpeningTypeViewSet,
    base_name='openingtype'
)

router.register(
    r'storageslace',
    views.StoragePlaceViewSet,
    base_name='storageslace'
)

router.register(
    r'item',
    views.ItemViewSet,
    base_name='item'
)

router.register(
    r'itemtype',
    views.ItemTypeViewSet,
    base_name='itemtype'
)



#urlpatterns = router.urls

urlpatterns += [
    path('', include(router.urls)),
    path('schema/', schema_view),
]


urlpatterns += [
    path('rest-auth/', include('rest_auth.urls')),
    #path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/token-refresh/', refresh_jwt_token),
    path('rest-auth/token-verify/', verify_jwt_token),
]


'''
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
'''


