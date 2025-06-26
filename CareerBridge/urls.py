from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # Default redirect to home (companies list) if logged in
    path('', lambda request: redirect('company_list'), name='home'),

    # Include app-specific URLs
    path('accounts/', include('account.urls')),
    path('placement/', include('placement.urls')),
]
