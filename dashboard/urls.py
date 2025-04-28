"""
URL configuration for dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from . import views
from django.shortcuts import render
from .views import home
from .views import update_cluster
from .views import deploy_re
from .views import restart_ds
from .views import restart_sts
from .views import details
from .views import delete_pod
from .views import view_ecs_cluster
from .views import ecs
from .views import describe_task
from .views import list_task_definition

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('update', update_cluster, name='update_cluster'),
    path('deploy_re', deploy_re, name='deploy_re'),
    path('restart_ds', restart_ds, name='restart_ds'),
    path('restart_sts', restart_sts, name='restart_sts'),
    path('kubernetes/<str:namespace>/<str:id>', details, name='details'),
    path('delete_pod', delete_pod, name='delete_pod'),
    path('ecs/<str:cluster_name>/<str:cluster_region>/', view_ecs_cluster, name='view_ecs_cluster'),
    path('ecs/<str:clutser>/<str:svc>/<str:cluster_region>/', ecs, name='ecs'),
    re_path(r'^ecs/(?P<cluster>arn:aws:ecs:[^/]+/[^/]+)/(?P<task>arn:aws:ecs:[^/]+/[^/]+/.+)/$', describe_task, name='describe_task'),
    path('ecs/taskdefinition/<str:cluster_region>', list_task_definition, name='list_task_definition'),

]
