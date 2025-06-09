from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('anime/', include(('pagina_main.urls', 'anime'), namespace='anime')),
    path('', include('pagina_main.urls')),
]
