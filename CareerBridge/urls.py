from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Default redirect to home (companies list) if logged in
    path('', lambda request: redirect('company_list'), name='home'),

    # Include app-specific URLs
    path('accounts/', include('account.urls')),
    path('/', include('placement.urls')),
    path('tnp/', include('tnpadmin.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
