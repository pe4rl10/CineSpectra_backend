from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('movies/', include('movies.urls')),
    path('history/', include('history.urls'))
]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'), name='')]