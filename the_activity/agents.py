from __future__ import absolute_import, unicode_literals
import random
from the_system.services import registered_services
 
from django.utils import timezone
from django.db.models import Q
from django.db.models import F
 

from the_system.text_choices import TransactionTypes
from .models import UserActivity

from asgiref.sync import async_to_sync,sync_to_async
 
 
from the_system.text_choices import EmailStatus
from the_system.locks import lock_object
from the_system.settings import _get_setting

import logging
logger = logging.getLogger('ilogger')
import faust


def commit_user_activity(user_activity_data):
    user_activity =UserActivity.objects.create(user_id=user_activity_data.user_id,
                                target_id=user_activity_data.target_id,
                                target_ct_id = user_activity_data.target_ct_id,
                                change_message=user_activity_data.message,
                                ip_address=user_activity_data.ip_address,
                                user_agent=user_activity_data.user_agent,
                                path=user_activity_data.path
                                )

class UserActivityData(faust.Record, serializer='json'):
    user_id: int
    message:str
    target_id:int = None
    target_ct_id:int = None
    ip_address: str =None
    user_agent: str = None
    path:str =  None

 

app_name = _get_setting("APP_NAME","the_activity")

faust_app = registered_services.get("faust_app",None)

user_activity_topic = f"{app_name.lower().replace(' ', '_')}_user_activity"

if faust_app:
    capture_user_activity = faust_app.topic(str(user_activity_topic), value_type=UserActivityData)

    @faust_app.agent(capture_user_activity)
    async def capture_user_activity_agent(stream):
        async for event in stream:
            print("test_message_confirmation >>>>>>>>>>>>>>>>>>>>" ,event)
            user_activity = await async_to_sync(commit_user_activity)(event)