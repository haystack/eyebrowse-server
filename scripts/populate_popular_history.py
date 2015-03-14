import setup_django

from django.utils import timezone
from api.models import EyeHistory, PopularHistory, PopularHistoryInfo

import datetime
import urllib2

from lxml import etree
from urllib2 import urlopen

from django.utils import timezone

from api.models import EyeHistory
from api.models import PopularHistory
from api.models import PopularHistoryInfo
from api.utils import humanize_time

from accounts.models import UserProfile


def reset_values():
    p = PopularHistory.objects.all()

    for pop in p.iterator():
        pop.total_time_ago = 0
        pop.save()

def create_pop(ehist, url):
    print ehist.title
    p, _ = PopularHistoryInfo.objects.get_or_create(url=url,
                                                    domain=ehist.domain,
                                                    favIconUrl=ehist.favIconUrl,
                                                    title=ehist.title)

    try:
        try:
            conn = urlopen(ehist.url)
        except urllib2.HTTPError:
            p.save()
            return p

        f = conn.read()
    except:
        p.save()
        return p
    try:
        tree = etree.HTML(f)
        m = tree.xpath("//meta[@property='og:image']")
        if m:
            p.img_url = m[0].get("content", '')
        else:
            n = tree.xpath("//meta[@property='twitter:image']")
            if n:
                p.img_url = n[0].get("content", '')

        m = tree.xpath("//meta[@property='og:description']")
        if m:
            p.description = m[0].get("content", '')
        else:
            n = tree.xpath("//meta[@property='twitter:description']")
            if n:
                p.description = n[0].get("content", '')
    except:
        pass

    p.save()

    return p


def populate_popular_history():

    month_ago = datetime.datetime.now() - datetime.timedelta(weeks=10)
    e = EyeHistory.objects.filter(start_time__gt=month_ago)

    for ehist in e.iterator():
        url = ehist.url
        if len(url) > 255:
            url = url[:255]

        p = PopularHistoryInfo.objects.filter(url=url)
        if not p.exists():
            p = create_pop(ehist, url)
        else:
            p = p[0]

        total_pop, _ = PopularHistory.objects.get_or_create(
            popular_history=p, user=None)

        if not total_pop.eye_hists.filter(pk=ehist.id).exists():

            total_pop.eye_hists.add(ehist)
            total_pop.visitors.add(ehist.user)

            messages = ehist.eyehistorymessage_set.all()

            for message in messages:
                total_pop.messages.add(message)

            total_pop.total_time_spent += ehist.total_time

        time_diff = timezone.now() - ehist.end_time

        total_pop.total_time_ago += int(
            round(float(time_diff.total_seconds()) / 3600.0))

        total_pop.save()

        follow_users = list(
            UserProfile.objects.filter(
                follows=ehist.user.profile).select_related())

        follow_users.append(ehist.user.profile)

        for user_prof in follow_users:
            u = user_prof.user

            user_pop, _ = PopularHistory.objects.get_or_create(
                popular_history=p, user=u)

            if not user_pop.eye_hists.filter(pk=ehist.id).exists():

                user_pop.eye_hists.add(ehist)
                user_pop.visitors.add(ehist.user)

                messages = ehist.eyehistorymessage_set.all()

                for message in messages:
                    user_pop.messages.add(message)

                user_pop.total_time_spent += ehist.total_time

            time_diff = timezone.now() - ehist.end_time

            user_pop.total_time_ago += int(
                round(float(time_diff.total_seconds()) / 3600.0))

            user_pop.save()

    p = PopularHistory.objects.filter(total_time_ago=0)
    p.delete()

    p = PopularHistory.objects.filter(user__isnull=False)

    for pop in p.iterator():
        if pop.visitors.count() == 1:
            if pop.visitors.all()[0] == pop.user:
                pop.delete()

    p = PopularHistoryInfo.objects.all()
    for pop in p.iterator():
        if len(list(pop.popularhistory_set.all())) == 0:
            pop.delete()


def calculate_scores():

    p = PopularHistory.objects.all()

    for pop in p.iterator():

        if pop.eye_hists.count() == 0:
            pop.delete()
            continue

        time = pop.total_time_ago / float(pop.eye_hists.count())
        pop.avg_time_ago = datetime.datetime.now(
        ) - datetime.timedelta(hours=time)

        time_spent = pop.total_time_spent / float(pop.eye_hists.count())
        pop.humanize_avg_time = humanize_time(
            datetime.timedelta(milliseconds=time_spent))

        num_comments = pop.messages.count()
        c = float(num_comments * 40.0) / \
            float(
                ((
                    float(pop.total_time_ago) + 1.0) /
                    float(pop.eye_hists.count())) ** 1.2)
        pop.num_comment_score = c

        num_vistors = pop.visitors.count()
        v = float((num_vistors - 1.0) * 50.0) / \
            float(
                ((
                    float(pop.total_time_ago) + 1.0) /
                    float(pop.eye_hists.count())) ** 1.2)
        pop.unique_visitor_score = v

        num_time = float(pop.total_time_spent) / float(pop.eye_hists.count())

        t = float((num_time ** .8) / 1000.0) / \
            float(
                ((
                    float(pop.total_time_ago) + 1.0) /
                    float(pop.eye_hists.count())) ** 1.2)

        t2 = float((num_time - 5000) / 1000.0) / \
            float(
                ((
                    float(pop.total_time_ago) + 1.0) /
                    float(pop.eye_hists.count())) ** 1)

        c = float(num_comments * 40.0) / \
            float(
                ((float(pop.total_time_ago) + 1.0) / float(pop.eye_hists.count()))**1.2)

        pop.num_comment_score = c

        num_vistors = pop.visitors.count()

        v = float((num_vistors - 1.0) * 50.0) / \
            float(
                ((float(pop.total_time_ago) + 1.0) / float(pop.eye_hists.count()))**1.2)
        pop.unique_visitor_score = v

        num_time = float(pop.total_time_spent) / float(pop.eye_hists.count())

        t = float((num_time**.8) / 1000.0) / \
            float(
                ((float(pop.total_time_ago) + 1.0) / float(pop.eye_hists.count()))**1.2)

        t2 = float((num_time - 5000) / 1000.0) / \
            float(
                ((float(pop.total_time_ago) + 1.0) / float(pop.eye_hists.count()))**1)

        pop.avg_time_spent_score = t2

        pop.top_score = float(c + v + t)
        try:
            pop.save()
        except:
            continue


if __name__ == '__main__':
    reset_values()
    populate_popular_history()
    calculate_scores()
