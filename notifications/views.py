from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .models import NoticeType, NOTICE_MEDIA
from .utils import notice_setting_for_user

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string

from annoying.decorators import render_to

from accounts.models import UserProfile

from api.models import EyeHistory, PopularHistoryInfo

from common.constants import EMPTY_SEARCH_MSG
from common.view_helpers import _template_values

from live_stream.query_managers import profile_stat_gen
from live_stream.query_managers import online_user

from stats.models import FavData
from notifications.models import Notification
from api.utils import humanize_time
from eyebrowse.log import logger
import datetime
from django.utils import timezone


@login_required
@render_to('notifications/notifications.html')
def notifications(request):

    user = get_object_or_404(User, username=request.user.username)
    userprof = UserProfile.objects.get(user=user)
    confirmed = userprof.confirmed
    if not confirmed:
        return redirect('/consent')

    empty_search_msg = EMPTY_SEARCH_MSG['notifications']

    # stats
    tot_time, item_count = profile_stat_gen(user)

    fav_data = FavData.objects.get(user=user)

    num_history = EyeHistory.objects.filter(user=user).count()

    is_online = online_user(user=user)

    following_users = user.profile.follows.all()
    following_count = following_users.count()
    follower_count = UserProfile.objects.filter(follows=user.profile).count()

    notifications = notification_renderer(user, empty_search_msg)

    nots = Notification.objects.filter(recipient=user, seen=False)
    for n in nots:
        n.seen = True
        n.save()

    
    template_dict = {
        "username": user.username,
        "following_count": following_count,
        "follower_count": follower_count,
        "is_online": is_online,
        "num_history": num_history,
        "notifications": notifications,
        "tot_time": tot_time,
        "item_count": item_count,
        "fav_data": fav_data,
    }

    return _template_values(request,
                            page_title="notifications",
                            navbar='notify',
                            sub_navbar="subnav_data",
                            not_count=0,
                            **template_dict)


def notification_renderer(user, empty_search_msg):
    notifications = Notification.objects.filter(recipient=user).select_related().order_by('-date_created')
    for notif in notifications:
        if notif.notice_type.label != "new_follower":
            pop = PopularHistoryInfo.objects.filter(url=notif.url)
            if pop.exists():
                notif.description = pop[0].description
                notif.img_url = pop[0].img_url
                notif.favIconUrl = pop[0].favIconUrl
                notif.title = pop[0].title
                notif.hum_date = humanize_time(timezone.now() - notif.date_created)
            else:
                notif.description = None
             
    template_dict = {'notifications': notifications,
                     'empty_search_msg': empty_search_msg, }

    return render_to_string('notifications/notification_list.html', template_dict)



class NoticeSettingsView(TemplateView):
    template_name = "notifications/notice_settings.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NoticeSettingsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['nav_account'] = 'active'
        context['email_notifications'] = 'active'
        context['user'] = request.user
        context['page_title'] = "Set Email Notifications"
        
        return self.render_to_response(context)

    @property
    def scoping(self):
        return None

    def setting_for_user(self, notice_type, medium_id):
        return notice_setting_for_user(
            self.request.user,
            notice_type,
            medium_id,
            scoping=self.scoping
        )

    def form_label(self, notice_type, medium_id):
        return "setting-{0}-{1}".format(
            notice_type.pk,
            medium_id
        )

    def process_cell(self, label):
        val = self.request.POST.get(label)
        _, pk, medium_id = label.split("-")
        notice_type = NoticeType.objects.get(pk=pk)
        setting = self.setting_for_user(notice_type, medium_id)
        if val == "on":
            setting.send = True
        else:
            setting.send = False
        setting.save()

    def settings_table(self):
        notice_types = NoticeType.objects.all()
        table = []
        for notice_type in notice_types:
            row = []
            for medium_id, medium_display in NOTICE_MEDIA:
                setting = self.setting_for_user(notice_type, medium_id)
                row.append((
                    self.form_label(notice_type, medium_id),
                    setting.send)
                )
            table.append({"notice_type": notice_type, "cells": row})
        return table

    def post(self, request, *args, **kwargs):
        table = self.settings_table()
        for row in table:
            for cell in row["cells"]:
                self.process_cell(cell[0])
        return HttpResponseRedirect(request.POST.get("next_page", "."))

    def get_context_data(self, **kwargs):
        settings = {
            "column_headers": [
                medium_display
                for _, medium_display in NOTICE_MEDIA
            ],
            "rows": self.settings_table(),
        }
        context = super(NoticeSettingsView, self).get_context_data(**kwargs)
        context.update({
            "notice_types": NoticeType.objects.all(),
            "notice_settings": settings
        })
        return context
