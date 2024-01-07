"""nessues URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404

import nessues_app.views as views
import nessues_app_users.views as users_views
import django.contrib.auth.views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', users_views.login_view, name='login'),
    path('logout/', users_views.logout_view, name='logout'),
    path('register/', users_views.register_view, name='register'),
    path('account/', users_views.account_view, name='account'),
    path('invitations/', login_required(views.InvitationsView.as_view()), name='intivations'),
    path('groups/', login_required(views.GroupsView.as_view()), name='groups'),
    path('rooms/', login_required(views.RoomsView.as_view()), name='rooms'),
    path('tables/<str:redirected_from>/<int:key_id>/', login_required(views.TablesView.as_view()), name='tables'),
    path('tasks/<int:key_id>/', login_required(views.TasksView.as_view()), name='tasks'),
    path('about/', login_required(views.about_view), name='about'),
    path('admin/', admin.site.urls),

]

# handler404 = 'nessues_app_users.views.error_404_view'
