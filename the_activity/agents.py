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

user_activity_topic = f"{app_name.lower().replace(' ', '_')}_user_activity_topic"

if faust_app:
    capture_user_activity = faust_app.topic(str(user_activity_topic), value_type=UserActivityData)

    @faust_app.agent(capture_user_activity)
    async def capture_user_activity_agent(stream):
        async for event in stream:
            print("test_message_confirmation >>>>>>>>>>>>>>>>>>>>" ,event)



            user_activity = await sync_to_async(UserActivity.objects.create)(user_id=event.user_id,
                                        target_id=event.target_id,
                                        target_ct_id = event.target_ct_id,
                                        change_message=event.message,
                                        ip_address=event.ip_address,
                                        user_agent=event.user_agent,
                                        path=event.path
                                        )