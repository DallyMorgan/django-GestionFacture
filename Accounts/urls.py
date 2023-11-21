
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Accounts.views import login_user, logout_user

urlpatterns = [
    
    path('', login_user, name='login'),
    path('logout',logout_user, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)