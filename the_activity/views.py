from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction

# Create your views here.
from django.contrib.auth.decorators import login_required
from the_user.decorators import otp_required , change_password_required
from the_system.utils.paginator import get_paginator
import logging
logger = logging.getLogger('ilogger')
page_size = 25


# Create your views here.
@login_required
@otp_required
@change_password_required
def list_activities(request):
    # Profile.objects.all().delete()

    if hasattr(request,'search_value') and request.search_value:
        user_activities = request.user.activities.filter(change_message__icontains=request.search_value.lower()).order_by('-pk')
    else:
        user_activities = request.user.activities.order_by('-pk').all()

    page_number, activities = get_paginator(request, user_activities)  # 3 post per page
    page_number = request.GET.get('page')

    # TODO: make this async

    unread_activities = request.user.activities.filter(read=False).all()

    with transaction.atomic():
        for user_activity in unread_activities:
            user_activity.read = True
            user_activity.save()

    context = {"page": page_number, "activities": activities}
    return render(request, 'the_activity/activity_list.html', context)
