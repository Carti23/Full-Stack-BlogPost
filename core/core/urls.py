from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view


"""swagger setup"""
schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('account/', include('account.urls', namespace='account')),
    path('api/', include('api.urls')),
    path('swagger/', schema_view),
    path('', include('django.contrib.auth.urls'))
]
