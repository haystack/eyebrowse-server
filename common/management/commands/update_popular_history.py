import sys
import datetime
import urllib2

from lxml import etree
from urllib2 import urlopen

from django.utils import timezone
from django.core.management.base import NoArgsCommand

from api.models import EyeHistory
from api.models import PopularHistory
from api.models import PopularHistoryInfo
from api.utils import humanize_time

from accounts.models import UserProfile

from eyebrowse.log import logger


class Command(NoArgsCommand):
    help = 'Updates popular history whoo!'

    def handle(self, **options):
        self.log('Beginning update')
        self._reset_values()
        self._populate_popular_history()
        self._calculate_scores()
        self.log('Update complete.')

    def log(self, msg):
        msg = 'update_popular_history:::%s\n' % msg
        logger.info(msg)
        self.stdout.write(msg)

    def _reset_values(self):
        self.log('resetting values')
        
        #set total time ago (sum of time ago for all eyebrowse visits to this page in last 10 weeks) to 0
        #set total time spent (sum of time spend for all eyebrowse visits to this page in last 10 weeks) to 0
        PopularHistory.objects.update(total_time_ago=0, total_time_spent=0)

    def _create_pop(self, ehist, url):
        self.log("_create_pop, %s" % ehist.title)
        p, _ = PopularHistoryInfo.objects.get_or_create(url=url,
                                                        domain=ehist.domain,
                                                        favicon_url=ehist.favicon_url,
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
                p.img_url = m[0].get('content', '')
            else:
                n = tree.xpath("//meta[@property='twitter:image']")
                if n:
                    p.img_url = n[0].get('content', '')

            m = tree.xpath("//meta[@property='og:description']")
            if m:
                p.description = m[0].get('content', '')
            else:
                n = tree.xpath("//meta[@property='twitter:description']")
                if n:
                    p.description = n[0].get('content', '')
        except:
            pass

        p.save()

        return p

    def _populate_popular_history(self):

        month_ago = datetime.datetime.now() - datetime.timedelta(weeks=10)
        timezone.make_aware(month_ago, timezone.get_current_timezone())

        # get all eyehistory events from 10 weeks ago to today
        e = EyeHistory.objects.filter(start_time__gt=month_ago)

        for ehist in e.iterator():
            url = ehist.url
            url = url[:min(255, len(url))]

            # popularhistoryinfo stores general information about this page
            # such as description, title, domain, image, etc.
            p = PopularHistoryInfo.objects.filter(url=url)
            if not p.exists():
                # try to extract description, title, etc from the page and
                # create a popularhistoryinfo item from it
                p = self._create_pop(ehist, url)
            else:
                p = p[0]

            # each popularhistory is associated with a popularhistoryitem
            # popularhistory contains scoring info and is tied either to 
            # no user (so scoring for the firehose) or to a particular user
            # (so scoring for their following feed)
            pop_items = PopularHistory.objects.filter(
                popular_history=p, user=None)
            if pop_items.count() == 0:
                total_pop = PopularHistory.objects.create(
                    popular_history=p, user=None)
            elif pop_items.count() > 1:
                total_pop = pop_items[0]
                for i in pop_items[1:]:
                    i.delete()
            else:
                total_pop = pop_items[0]

            # we add every eyehistory to the firehose popularhistory counterpoint
            # and also keep track of the users and messages to that page
            if not total_pop.eye_hists.filter(pk=ehist.id).exists():
                total_pop.eye_hists.add(ehist)
                total_pop.visitors.add(ehist.user)

                messages = ehist.eyehistorymessage_set.all()
                for message in messages:
                    total_pop.messages.add(message)

            # we increment the total time spent and total time ago
            total_pop.total_time_spent += ehist.total_time

            time_diff = timezone.now() - ehist.end_time
            total_pop.total_time_ago += int(
                round(float(time_diff.total_seconds()) / 3600.0))

            total_pop.save()


            # for each of the users that are following the person
            # in this eyehistory, we add this eyehistory to the
            # the popularhistory item for that user
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

        # if there are any popularhistory items that still have
        # total_time_ago or total_time_spent as 0 then that means
        # that no eyehistories in the preceeding loop
        # had been to that page. This means the popularhistory is
        # stale (all visits are from over 10 weeks ago) so we delete
        self.log('deleting total pop')
        p = PopularHistory.objects.filter(total_time_ago=0)
        self.log('count %s' % p.count())
        p.delete()

        self.log('deleting total spent should be 0')
        p = PopularHistory.objects.filter(total_time_spent=0)
        self.log('count %s' % p.count())
        p.delete()

        # we're interested in including one's own visits to the score in
        # one's own feed, but don't want to include in list of users
        p = PopularHistory.objects.filter(user__isnull=False)

        for pop in p.iterator():
            if pop.visitors.count() == 1:
                if pop.visitors.all()[0] == pop.user:
                    pop.delete()

        # remove eyehistories that are from over 10 weeks ago
        # if everything gets removed then delete the popularhistory
        # though this shouldn't happen (see above)
        p = PopularHistory.objects.all()
        for i in p.iterator():
            for e in i.eye_hists.filter(start_time__lt=month_ago):
                i.eye_hists.remove(e)
            if i.eye_hists.count() == 0:
                self.log('shouldn\'t even get here...')
                i.delete()

        # if there are any popularhistoryinfo items now that have
        # no corresponding popularhistory objects (because they've been
        # deleted for being stale presumably) then delete
        p = PopularHistoryInfo.objects.all()
        for pop in p.iterator():
            if len(list(pop.popularhistory_set.all())) == 0:
                self.log('delete pop hist info')
                pop.delete()

    def _calculate_scores(self):

        # we should have lists of eyehistories, list of users,
        # list of messages, total time ago, and total time spent 
        # populated for each popularhistory. Now we calculate
        # scores based on these things.
        p = PopularHistory.objects.all()

        for pop in p.iterator():
            try:
                if pop.eye_hists.count() == 0:
                    pop.delete()
                    continue

                # avg time ago is total time ago / number of eyehistories
                time = pop.total_time_ago / float(pop.eye_hists.count())
                pop.avg_time_ago = datetime.datetime.now(
                ) - datetime.timedelta(hours=time)

                # avg time spent is total time spent / eyehistories
                time_spent = pop.total_time_spent / \
                    float(pop.eye_hists.count())
                pop.humanize_avg_time = humanize_time(
                    datetime.timedelta(milliseconds=time_spent))

                # num comment score gives score based on num
                # comments with a time decay factor
                num_comments = pop.messages.count()
                c = float(num_comments * 40.0) / \
                    float(
                        ((
                            float(pop.total_time_ago) + 1.0) /
                            float(pop.eye_hists.count())) ** 1.2)
                pop.num_comment_score = c

                # num visitors score gives score based on num
                # visitors with a time decay factor
                num_vistors = pop.visitors.count()
                v = float((num_vistors - 1.0) * 50.0) / \
                    float(
                        ((
                            float(pop.total_time_ago) + 1.0) /
                            float(pop.eye_hists.count())) ** 1.2)
                pop.unique_visitor_score = v

                # num time score gives score based on avg time
                # spent with a time decay factor
                num_time = float(pop.total_time_spent) / \
                    float(pop.eye_hists.count())

                t = float((num_time ** .8) / 1000.0) / \
                    float(
                        ((
                            float(pop.total_time_ago) + 1.0) /
                            float(pop.eye_hists.count())) ** 1.5)

                t2 = float((num_time - 5000) / 1000.0) / \
                    float(
                        ((
                            float(pop.total_time_ago) + 1.0) /
                            float(pop.eye_hists.count())) ** 1)
                pop.avg_time_spent_score = t2

                # top score combines all the scores together
                pop.top_score = float(c + v + t)
                pop.save()
            except Exception, e:
                self.log(e)
                continue
