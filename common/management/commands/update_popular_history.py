import sys
import datetime
import urllib2

from lxml import etree
from urllib2 import urlopen

from django.utils import timezone
from django.core.management.base import NoArgsCommand

from bulk_update.helper import bulk_update

from api.models import EyeHistory
from api.models import PopularHistory
from api.models import PopularHistoryInfo
from api.utils import humanize_time

from accounts.models import UserProfile

from common.helpers import queryset_iterator
from common.helpers import queryset_iterator_chunkify

from eyebrowse.log import logger

CHUNK_SIZE = 10000


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

    def _log_updates(self, i, total_updates, function):
        self.log(
            "Completed %d/%d updates. [%s]" % (i, total_updates, function))

    def _reset_values(self):
        self.log('resetting values')

        # set total time ago (sum of time ago for all eyebrowse visits to this page in last 10 weeks) to 0
        # set total time spent (sum of time spend for all eyebrowse visits to
        # this page in last 10 weeks) to 0
        PopularHistory.objects.update(total_time_ago=0, total_time_spent=0)

    def _create_pop(self, e, url):
        self.log("_create_pop, %s" % e.title)
        p, _ = PopularHistoryInfo.objects.get_or_create(url=url,
                                                        domain=e.domain,
                                                        favicon_url=e.favicon_url,
                                                        title=e.title)

        try:
            try:
                conn = urlopen(e.url)
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
        self.log('_populate_popular_history')

        month_ago = datetime.datetime.now() - datetime.timedelta(weeks=10)
        timezone.make_aware(month_ago, timezone.get_current_timezone())

        # get all eyehistory events from 10 weeks ago to today
        eye_history = EyeHistory.objects.filter(
            start_time__gt=month_ago).select_related()

        i = 0  # in case we try to log but there is no eye_history
        total_updates = eye_history.count()
        for i, e in enumerate(queryset_iterator(eye_history)):
            url = e.url
            url = url[:min(255, len(url))]

            # popularhistoryinfo stores general information about this page
            # such as description, title, domain, image, etc.
            p = PopularHistoryInfo.objects.filter(url=url)
            if not p.exists():
                # try to extract description, title, etc from the page and
                # create a popularhistoryinfo item from it
                p = self._create_pop(e, url)
            else:
                p = p[0]

            # each popularhistory is associated with a popularhistoryitem
            # popularhistory contains scoring info and is tied either to
            # no user (so scoring for the firehose) or to a particular user
            # (so scoring for their following feed)
            pop_items = PopularHistory.objects.filter(
                popular_history=p, user=None).prefetch_related('eye_hists')
            if pop_items.count() == 0:
                total_pop = PopularHistory.objects.create(
                    popular_history=p, user=None)
            elif pop_items.count() > 1:
                total_pop = pop_items[0]
                for i in pop_items[1:]:
                    i.delete()
            else:
                total_pop = pop_items[0]
            self._add_users_and_messages(total_pop, e)

            # for each of the users that are following the person
            # in this eyehistory, we add this eyehistory to the
            # the popularhistory item for that user
            follow_users = UserProfile.objects.filter(
                follows=e.user.profile).select_related()

            # do this outside of the loop so we can use an iterator
            user_pop, _ = PopularHistory.objects.get_or_create(
                popular_history=p, user=e.user)
            self._add_users_and_messages(user_pop, e)

            for user_prof in queryset_iterator(follow_users):
                user_pop, _ = PopularHistory.objects.get_or_create(
                    popular_history=p, user=user_prof.user)
                self._add_users_and_messages(user_pop, e)

            if i != 0 and i % CHUNK_SIZE == 0:
                self._log_updates(i, total_updates, 'popular_history')

        self._log_updates(i, total_updates, 'popular_history')
        self._delete_old()

        # we're interested in including one's own visits to the score in
        # one's own feed, but don't want to include in list of users
        popular_history = PopularHistory.objects.filter(
            user__isnull=False).prefetch_related(
                'visitors').select_related()

        for p in queryset_iterator(popular_history):
            if p.visitors.count() == 1:
                if p.visitors.all()[0] == p.user:
                    p.delete()

        # remove eyehistories that are from over 10 weeks ago
        # if everything gets removed then delete the popularhistory
        # though this shouldn't happen (see above)
        popular_history = PopularHistory.objects.all().prefetch_related(
            'eye_hists')
        for i in queryset_iterator(popular_history):
            i.eye_hists.remove(*i.eye_hists.filter(start_time__lt=month_ago))

        # if there are any popularhistoryinfo items now that have
        # no corresponding popularhistory objects (because they've been
        # deleted for being stale presumably) then delete
        PopularHistoryInfo.objects.filter(popularhistory=None).delete()

    def _add_users_and_messages(self, popular_history_item, e):
        # we add every eyehistory to the firehose popularhistory counterpoint
        # and also keep track of the users and messages to that page
        if not popular_history_item.eye_hists.filter(pk=e.id).exists():
            popular_history_item.eye_hists.add(e)
            popular_history_item.visitors.add(e.user)

            popular_history_item.messages.add(*e.eyehistorymessage_set.all())

        # we increment the total time spent and total time ago
        popular_history_item.total_time_spent += e.total_time

        time_diff = timezone.now() - e.end_time
        popular_history_item.total_time_ago += int(
            round(time_diff.total_seconds() / 3600.0))

        popular_history_item.save()

    def _delete_old(self):
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

    def _calculate_scores(self):
        self.log('_calculate_scores')
        # we should have lists of eyehistories, list of users,
        # list of messages, total time ago, and total time spent
        # populated for each popularhistory. Now we calculate
        # scores based on these things.
        popular_history = PopularHistory.objects.all().prefetch_related(
            'eye_hists', 'messages', 'visitors')
        total_updates = popular_history.count()
        i = 0  # in case we try to log but there is no eye_history
        for i, p in enumerate(queryset_iterator(popular_history)):
            try:
                eye_hist_count = p.eye_hists.count()
                if eye_hist_count == 0:
                    p.delete()
                    continue

                # avg time ago is total time ago / number of eyehistories
                time = p.total_time_ago / float(eye_hist_count)
                p.avg_time_ago = datetime.datetime.now(
                ) - datetime.timedelta(hours=time)

                # avg time spent is total time spent / eyehistories
                time_spent = p.total_time_spent / \
                    float(eye_hist_count)
                p.humanize_avg_time = humanize_time(
                    datetime.timedelta(milliseconds=time_spent))

                # num comment score gives score based on num
                # comments with a time decay factor
                num_comments = p.messages.count()
                comment_score = float(num_comments * 40.0) / \
                    float(
                        ((
                            float(p.total_time_ago) + 1.0) /
                            float(eye_hist_count)) ** 1.2)
                p.num_comment_score = comment_score

                # num visitors score gives score based on num
                # visitors with a time decay factor
                num_vistors = p.visitors.count()
                visitor_score = float((num_vistors - 1.0) * 50.0) / \
                    float(
                        ((
                            float(p.total_time_ago) + 1.0) /
                            float(eye_hist_count)) ** 1.2)
                p.unique_visitor_score = visitor_score

                # num time score gives score based on avg time
                # spent with a time decay factor
                num_time = float(p.total_time_spent) / \
                    float(eye_hist_count)

                time_score = float((num_time ** .8) / 1000.0) / \
                    float(
                        ((
                            float(p.total_time_ago) + 1.0) /
                            float(eye_hist_count)) ** 1.5)

                time_score_2 = float((num_time - 5000) / 1000.0) / \
                    float(
                        ((
                            float(p.total_time_ago) + 1.0) /
                            float(eye_hist_count)) ** 1)
                p.avg_time_spent_score = time_score_2

                # top score combines all the scores together
                p.top_score = float(comment_score + visitor_score + time_score)

                if i != 0 and i % CHUNK_SIZE == 0:
                    self._log_updates(i, total_updates, 'calculate_scores')
            except Exception, e:
                self.log(e)
                continue

        bulk_update(popular_history, batch_size=CHUNK_SIZE)
        self._log_updates(i, total_updates, 'calculate_scores')
