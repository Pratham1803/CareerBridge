from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from account.views import redirect_user_by_role


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect_user_by_role(request.user)
    return redirect("login")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("students/", include("students.urls")),
    path("accounts/", include("account.urls")),
    path("companies/", include("companies.urls")),    
    path("", home_redirect, name="home"),  # <-- add this line for home route

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# from django.contrib import admin
# from django.urls import path, include
# from django.shortcuts import redirect
# from django.conf import settings
# from django.conf.urls.static import static
# from account.views import redirect_user_by_role
# from companies import views as company_views


# def home_redirect(request):
#     if request.user.is_authenticated:
#         return redirect_user_by_role(request.user)
#     return redirect("login")


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path("students/", include("students.urls")),
#     path("accounts/", include("account.urls")),
#     path("companies/", include("companies.urls")),
#     path("jobs/create/", company_views.create_job, name="create_job"),  # <-- add this line
#     path("", home_redirect, name="home"),  # <-- add this line for home route

# ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
