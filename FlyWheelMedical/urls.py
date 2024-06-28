from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from FlyWheelMedicalApp.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('auntification/', include('FlyWheelMedicalApp.auntification.urls')),
    path('dashboard/', include('FlyWheelMedicalApp.profiles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)