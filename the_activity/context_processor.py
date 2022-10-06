from django.contrib import admin

import logging
logger = logging.getLogger('ilogger')


def user_activity_context_processor(request):
    user = request.user
    user_activities = []
    if request.user.is_authenticated:
        user_activities = user.activities.all()[:5]

    return {"user_activities": user_activities}
