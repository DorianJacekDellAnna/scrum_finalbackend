"""scrum_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from contacts.views import view_contacts
from tasks.views import login_user, create_user, view_tasks, view_topics, reset_user_pw
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("Welcome to the home page!")

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('tasks/', view_tasks.as_view(), name='tasks'),
    path('topics/', view_topics.as_view(), name='topics'),
    path('contacts/', view_contacts.as_view(), name='contacts'),
    path('login/', login_user.as_view(), name='login'),
    path('registry/', create_user.as_view(), name='registry'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/password_reset/confirm/<str:uidb64>/<str:token>/', reset_user_pw.as_view(), name='password_reset_confirm'),
]