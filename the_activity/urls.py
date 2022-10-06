import django.conf.urls
from django.contrib import admin
from django.urls import path, include

from .views import list_activities
import logging
logger = logging.getLogger('ilogger')

app_name = 'the_activity'

urlpatterns = [
    path('', list_activities, name='list_user_activities'),


]
