from typing import Any
from django.db.models import Model
from the_system.services import registered_services
 
from .models import UserActivity


def async_capture_user_activity_logger(  user_id: Model = None, ip_address=None, user_agent=None, path=None, target_id = None, target_ct_id =None,  message: str = '',
                            **kwargs):
    print("async_capture_user_activity_loggerasync_capture_user_activity_logger ",message)
    # if capture_user_activity.target:
    #     content_type = ContentType.objects.get_for_model(log_entry_data.target)
    #     object_id = log_entry_data.target.id

    if message:
        user_activity = UserActivity.objects.create(user_id=user_id,
                                     target_id=target_id,
                                     target_ct_id = target_ct_id,
                                     change_message=message,
                                     ip_address=ip_address,
                                     user_agent=user_agent,
                                     path=path
                                     )
        return True

    return False

celery_app = registered_services.get("celery_app",None)
faust_app = registered_services.get("faust_app",None)


if celery_app:
    async_capture_user_activity_logger = celery_app.task(name="capture_user_activity" ,queue="useractivity",max_retries=3)(async_capture_user_activity_logger)
