from django.contrib.auth.models import User
from django.db.models.signals import post_save
from allauth.account.signals import user_logged_in, password_changed, password_reset, email_confirmed, \
    email_confirmation_sent, email_changed
from django.dispatch import receiver
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from dataclasses import dataclass
from typing import Any
from .tasks import async_capture_user_activity_logger
from django.db.models import Model

from .models import UserActivity

from .signals import capture_user_activity
import logging
logger = logging.getLogger('ilogger')
'''
https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META

CONTENT_LENGTH – The length of the request body (as a string).
CONTENT_TYPE – The MIME type of the request body.
HTTP_ACCEPT – Acceptable content types for the response.
HTTP_ACCEPT_ENCODING – Acceptable encodings for the response.
HTTP_ACCEPT_LANGUAGE – Acceptable languages for the response.
HTTP_HOST – The HTTP Host header sent by the client.
HTTP_REFERER – The referring page, if any.
HTTP_USER_AGENT – The client’s user-agent string.
QUERY_STRING – The query string, as a single (unparsed) string.
REMOTE_ADDR – The IP address of the client.  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
REMOTE_HOST – The hostname of the client.      <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
REMOTE_USER – The user authenticated by the Web server, if any.
REQUEST_METHOD – A string such as "GET" or "POST". <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
SERVER_NAME – The hostname of the server.
SERVER_PORT – The port of the server (as a string).

'''


@receiver(capture_user_activity)
def capture_user_activity_logger(request: Any = None, user_to_use: Model = None, target: Model = None, message: str = '',
                            **kwargs):
    if request:

        # request = log_entry_data.request
        # print("request.META['CONTENT_LENGTH']", request.META['CONTENT_LENGTH'])
        # print("request.META['CONTENT_TYPE']", request.META['CONTENT_TYPE'])
        # print("request.META['HTTP_ACCEPT']", request.META['HTTP_ACCEPT'])
        # print("request.META['HTTP_ACCEPT_ENCODING']", request.META['HTTP_ACCEPT_ENCODING'])
        # print("request.META['HTTP_ACCEPT_LANGUAGE']", request.META['HTTP_ACCEPT_LANGUAGE'])
        # print("request.META['HTTP_HOST']", request.META['HTTP_HOST'])
        # print("request.META['HTTP_REFERER']", request.META['HTTP_REFERER'])
        # print("request.META['HTTP_USER_AGENT']", request.META['HTTP_USER_AGENT'])
        # print("request.META['QUERY_STRING']", request.META['QUERY_STRING'])
        # print("request.META['REMOTE_ADDR']", request.META['REMOTE_ADDR'])
        # print("request.META['REMOTE_HOST']", request.META['REMOTE_HOST'])
        # print("request.META['REQUEST_METHOD']", request.META['REQUEST_METHOD'])
        # print("request.META['SERVER_NAME']", request.META['SERVER_NAME'])
        # print("request.META['SERVER_PORT']", request.META['SERVER_PORT'])

        user = request.user
        ip_address = request.META['REMOTE_ADDR']
        user_agent = request.META.get('HTTP_USER_AGENT','UNKNOWN')
        path = request.META.get('HTTP_REFERER','UNKNOWN')
    else:
        user = user_to_use
        ip_address =""
        user_agent =""
        path = ""

    kwargs_local = {
         "user_id" : user.id if user else None, 
         "ip_address":ip_address,
         "user_agent": user_agent,
         "path": path,
         "target_id":target.pk if target else None,
         "target_ct_id": ContentType.objects.get_for_model(target.__class__).pk  if target else None,
         "message": message
    }

    final_kwargs = {**kwargs_local, **kwargs}

    #print(" final_kwargs " , final_kwargs)
    try:
        async_capture_user_activity_logger.apply_async(kwargs= kwargs_local)
    except:
        async_capture_user_activity_logger(**kwargs_local)
    #print(" sent async_capture_user_activity_logger ----------- ")


'''
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE

def log_action(self, user_id, content_type_id, object_id, object_repr, action_flag, change_message=''):
    
LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(model_object).pk,
            object_id=object.id,
            object_repr=unicode(object.title),
            action_flag=ADDITION if create else CHANGE)

'''


# -------------------------------------------------
#  capture other signals
# -------------------------------------------------


@receiver(post_save, sender=User)
def on_save_user_profile(sender, instance, **kwargs):
    pass


@receiver(user_logged_in)
def login_logger(request, user, **kwargs):
    capture_user_activity_logger(request=request, message="Logged in")


@receiver(password_changed)
def log_password_changed(request, user, **kwargs):
    capture_user_activity_logger(request=request, message="Password Changed")


@receiver(password_reset)
def log_password_reset(request, user, **kwargs):
    capture_user_activity_logger(request=request, message="Password Reset")


@receiver(email_confirmed)
def log_email_confirmed(request, email_address, **kwargs):
    capture_user_activity_logger(request=request, message="Email Confirmed")


@receiver(email_confirmation_sent)
def log_email_confirmation_sent(request, confirmation,signup, **kwargs):
    capture_user_activity_logger(request=request, message="Email Confirmation Sent")


@receiver(email_changed)
def log_email_changed(request, user,from_email_address,to_email_address, **kwargs):
    capture_user_activity_logger(request=request, message="Email Changed")
