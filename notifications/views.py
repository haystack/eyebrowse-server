from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .compat import login_required
from .models import NoticeType, NOTICE_MEDIA
from .utils import notice_setting_for_user
from eyebrowse.log import logger


class NoticeSettingsView(TemplateView):
    template_name = "notifications/notice_settings.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NoticeSettingsView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user'] = request.user
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
