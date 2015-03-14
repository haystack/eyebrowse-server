import setup_django
<<<<<<< HEAD

=======
from django.utils import timezone
from api.models import EyeHistory, PopularHistory, PopularHistoryInfo
>>>>>>> master
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


<<<<<<< HEAD
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
=======
def create_pop(eyehist, url):
    print eyehist.title
    p, _ = PopularHistoryInfo.objects.get_or_create(url=url,
                                                    domain=eyehist.domain,
                                                    favicon_url=eyehist.favicon_url,
                                                    title=eyehist.title)

    try:
        try:
            conn = urlopen(eyehist.url)
        except urllib2.HTTPError, x:
>>>>>>> master
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

<<<<<<< HEAD
    for ehist in e.iterator():
        url = ehist.url
=======
    for eyehist in e.iterator():
        url = eyehist.url
>>>>>>> master
        if len(url) > 255:
            url = url[:255]

        p = PopularHistoryInfo.objects.filter(url=url)
        if not p.exists():
            p = create_pop(ehist, url)
        else:
            p = p[0]

        total_pop, _ = PopularHistory.objects.get_or_create(
            popular_history=p, user=None)

<<<<<<< HEAD
        if not total_pop.eye_hists.filter(pk=ehist.id).exists():

            total_pop.eye_hists.add(ehist)
            total_pop.visitors.add(ehist.user)

            messages = ehist.eyehistorymessage_set.all()
=======
        if not total_pop.eye_hists.filter(pk=eyehist.id).exists():

            total_pop.eye_hists.add(eyehist)
            total_pop.visitors.add(eyehist.user)

            messages = eyehist.eyehistorymessage_set.all()
>>>>>>> master

            for message in messages:
                total_pop.messages.add(message)

<<<<<<< HEAD
            total_pop.total_time_spent += ehist.total_time

        time_diff = timezone.now() - ehist.end_time
=======
            total_pop.total_time_spent += eyehist.total_time

        time_diff = timezone.now() - eyehist.end_time
>>>>>>> master
        total_pop.total_time_ago += int(
            round(float(time_diff.total_seconds()) / 3600.0))

        total_pop.save()
<<<<<<< HEAD

        follow_users = list(
            UserProfile.objects.filter(
                follows=ehist.user.profile).select_related())

        follow_users.append(ehist.user.profile)
=======
<<<<<<< HEAD

        follow_users = UserProfile.objects.filter(
            follows=eyehist.user.profile).select_related()
=======
                
    
        follow_users = list(UserProfile.objects.filter(follows=eyehist.user.profile).select_related())
        
        follow_users.append(eyehist.user.profile)
>>>>>>> master
>>>>>>> master

        for user_prof in follow_users:
            u = user_prof.user

            user_pop, _ = PopularHistory.objects.get_or_create(
                popular_history=p, user=u)

<<<<<<< HEAD
            if not user_pop.eye_hists.filter(pk=ehist.id).exists():

                user_pop.eye_hists.add(ehist)
                user_pop.visitors.add(ehist.user)

                messages = ehist.eyehistorymessage_set.all()
=======
            if not user_pop.eye_hists.filter(pk=eyehist.id).exists():

                user_pop.eye_hists.add(eyehist)
                user_pop.visitors.add(eyehist.user)

                messages = eyehist.eyehistorymessage_set.all()
>>>>>>> master

                for message in messages:
                    user_pop.messages.add(message)

<<<<<<< HEAD
                user_pop.total_time_spent += ehist.total_time

            time_diff = timezone.now() - ehist.end_time
=======
                user_pop.total_time_spent += eyehist.total_time

            time_diff = timezone.now() - eyehist.end_time
>>>>>>> master
            user_pop.total_time_ago += int(
                round(float(time_diff.total_seconds()) / 3600.0))

            user_pop.save()

    p = PopularHistory.objects.filter(total_time_ago=0)
    p.delete()
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
    
>>>>>>> master
    p = PopularHistory.objects.filter(user__isnull=False)

    for pop in p.iterator():
        if pop.visitors.count() == 1:
            if pop.visitors.all()[0] == pop.user:
                pop.delete()
<<<<<<< HEAD

=======
    
>>>>>>> master
>>>>>>> master
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
<<<<<<< HEAD
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
=======
<<<<<<< HEAD
        c = float(num_comments * 85.0) / \
            float(
                ((float(pop.total_time_ago) + 1.0) / float(pop.eye_hists.count()))**1.4)
=======
        c = float(num_comments*40.0) / float(((float(pop.total_time_ago)+1.0)/float(pop.eye_hists.count()))**1.2)
>>>>>>> master
        pop.num_comment_score = c

        num_vistors = pop.visitors.count()
<<<<<<< HEAD
        v = float((num_vistors - 1.0) * 50.0) / \
            float(
                ((float(pop.total_time_ago) + 1.0) / float(pop.eye_hists.count()))**1.4)
        pop.unique_visitor_score = v

        num_time = float(pop.total_time_spent) / float(pop.eye_hists.count())

        t = float((num_time**.8) / 1000.0) / \
            float(
                ((float(pop.total_time_ago) + 1.0) / float(pop.eye_hists.count()))**1.4)

        t2 = float((num_time - 5000) / 1000.0) / \
            float(
                ((float(pop.total_time_ago) + 1.0) / float(pop.eye_hists.count()))**1)
=======
        v = float((num_vistors-1.0)*50.0) / float(((float(pop.total_time_ago)+1.0)/float(pop.eye_hists.count()))**1.2)
        pop.unique_visitor_score = v
        
        num_time = float(pop.total_time_spent)/float(pop.eye_hists.count())
        
        t = float((num_time**.8)/1000.0) / float(((float(pop.total_time_ago)+1.0)/float(pop.eye_hists.count()))**1.2)
        
        t2 = float((num_time - 5000)/1000.0) / float(((float(pop.total_time_ago)+1.0)/float(pop.eye_hists.count()))**1)
>>>>>>> master
>>>>>>> master
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
