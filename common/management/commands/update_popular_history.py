
import sys
import datetime
import urllib2
import subprocess

from scipy import stats

from lxml import etree
from urllib2 import urlopen

from django.contrib.auth.models import User
from django.utils import timezone
from django.core.management.base import NoArgsCommand
from django.db.models import Avg

from bulk_update.helper import bulk_update

from api.models import Domain
from api.models import EyeHistory
from api.models import PopularHistory
from api.models import PopularHistoryInfo
from api.models import Page
from api.models import Ratings
from api.models import PersonalizedRatings

from api.utils import humanize_time

from accounts.models import UserProfile

from common.helpers import queryset_iterator
from common.helpers import queryset_iterator_chunkify

from eyebrowse.log import logger

CHUNK_SIZE = 10

news_list = ['www.nytimes.com',
             'www.buzzfeed.com',
             'www.cnn.com',
             'www.vox.com',
             'medium.com',
             'www.huffingtonpost.com']


class Command(NoArgsCommand):
    help = 'Updates popular history whoo!'

    def handle(self, **options):
        self.log('Beginning update')
        self._reset_values()
        self._populate_popular_history()
        self._update_page_scores()
        self._update_personalized_scores()
        self._calculate_scores()
        self.log('Update complete.')

    def log(self, msg):
        msg = 'update_popular_history:::%s\n' % msg
        logger.info(msg)
        #self.stdout.write(msg)

    def _log_updates(self, i, total_updates, function):
        self.log(
            "Completed %d/%d updates. [%s]" % (i, total_updates, function))
        print("Completed %d/%d updates. [%s]" % (i, total_updates, function))

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


    # When a user unfollows a user, need to update popular history
    def remove_user_populate_history(self, user, remove_user):

        user_pops = PopularHistory.objects.filter(user=user).select_related()

        for user_pop in queryset_iterator(user_pops):
            self._remove_users_and_messages(user, user_pop, remove_user)

       # self._calculate_scores(user)


    # create popular history feed for a particular user
    # only 1 week back to make it faster
    def user_populate_history(self, user, follow_user):

        week_ago = datetime.datetime.now() - datetime.timedelta(weeks=1)
        timezone.make_aware(week_ago, timezone.get_current_timezone())

        # get all the visits that the new followee has
        eyehists = follow_user.eyehistory_set.filter(
            start_time__gt=week_ago).select_related()
        for e in queryset_iterator(eyehists):
            url = e.url
            url = url[:min(255, len(url))]

            # popularhistoryinfo stores general information about this page
            # such as description, title, domain, image, etc.
            p = PopularHistoryInfo.objects.filter(url=url)
            if p.exists():
                p = p[0]

                # create a popular history item for the user and the visit that
                # that user's followee has been to
                user_pop, _ = PopularHistory.objects.get_or_create(
                    popular_history=p, user=user)
                self._add_users_and_messages(user_pop, e)


        # Next, go through all the popular history items created for this user
        # and score them
       # self._calculate_scores(user)


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
            #follow_users = UserProfile.objects.filter(
                #follows=e.user.profile).select_related()
            follow_users = UserProfile.objects.all();

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


    # when unfollowing a user, remove that user and their visits, messages
    def _remove_users_and_messages(self, user, popular_history_item, remove_user):

        visitors = popular_history_item.visitors.all()

        count = 0
        found = False
        for visitor in visitors:
            if visitor == remove_user:
                found = True
            elif visitor != user:
                count += 1
        if count == 0:
            popular_history_item.delete()
            return

        if found:
            popular_history_item.visitors.remove(remove_user)

            remove_e = []
            for eye_hist in popular_history_item.eye_hists.all():
                if eye_hist.user == remove_user:
                    remove_e.append(eye_hist)

            popular_history_item.eye_hists.remove(*remove_e)

            remove_m = []
            for message in popular_history_item.messages.all():
                if message.eyehistory.user == remove_user:
                    remove_m.append(message)

            popular_history_item.messages.remove(*remove_m)



    def _add_users_and_messages(self, popular_history_item, e):
        # we add every eyehistory to the firehose popularhistory counterpoint
        # and also keep track of the users and messages to that page
        if not popular_history_item.eye_hists.filter(pk=e.id).exists():
            popular_history_item.eye_hists.add(e)
            popular_history_item.visitors.add(e.user)

            popular_history_item.messages.add(*e.eyehistorymessage_set.all())

        # we increment the total time spent and total time ago
        if e.total_time > 0:
            popular_history_item.total_time_spent += e.total_time
        else:
            self.log('E %s' % e.id)

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

    def _update_ratings_time_spent(self):
        eye_hists = EyeHistory.objects.all().select_related("user", "page")
        total_updates = eye_hists.count()
        ratings = {}
        filled_ratings = set()
        for i, eye_hist in enumerate(queryset_iterator(eye_hists)):
            user = eye_hist.user
            domain,_ = Domain.objects.get_or_create(url=eye_hist.domain)
            page,_ = Page.objects.get_or_create(url=eye_hist.url,
                                                domain=domain)
            key = (user.id, page.id)

            if key in filled_ratings or \
            Ratings.objects.filter(user=user,page=page, from_time_distribution=False).exists():
              filled_ratings.add(key)
              continue

            if key not in ratings:
                ratings[key] = (0,0)
            ratings[key]= (ratings[key][0] + 1.0* eye_hist.total_time/1000,i)

            if i != 0 and i % CHUNK_SIZE == 0:
                self._log_updates(i, total_updates, 'avg_time_spent_for_pages')

        total_updates = len(ratings)
        i = 0
        users = {}
        for key,time_spent in ratings.items():
            user_id = key[0]
            avg_time_spent = 1.0*time_spent[0]/time_spent[1]
            if not user_id in users:
                users[user_id] = []
            users[user_id].append(avg_time_spent)
            ratings[key] = avg_time_spent

            if i != 0 and i % CHUNK_SIZE == 0:
                self._log_updates(i, total_updates, 'forming_time_spent_distributions_for_users')

            i+=1

        i = 0
        for key,avg_time_spent in ratings.items():
            try:
                rating = Ratings.objects.get(user=User.objects.get(id=key[0]),
                                                page=Page.objects.get(id=key[1]))
                rating.score = round(stats.percentileofscore(users[key[0]],
                                                    avg_time_spent))*4.0/100 + 1
                rating.save()
            except Ratings.DoesNotExist:
                Ratings.objects.create(user=User.objects.get(id=key[0]),
                                        page=Page.objects.get(id=key[1]),
                                        score=round(stats.percentileofscore(users[key[0]],
                                                    avg_time_spent))*4.0/100 + 1)
            if i != 0 and i % CHUNK_SIZE == 0:
                self._log_updates(i, total_updates, 'calculating_left_over_ratings')

            i+=1

    def _update_domain_scores(self, domain_agg_scores):
        total_updates = len(domain_agg_scores)
        i = 0
        for _,domain_agg_score in domain_agg_scores.items():
            domain = domain_agg_score[2]
            domain.agg_score = 1.0*domain_agg_score[0]/domain_agg_score[1]
            domain.save()
            if i != 0 and i % CHUNK_SIZE == 0:
                self._log_updates(i, total_updates, 'domain_scores')
            i+=1

    def _update_page_scores(self):

        self._update_ratings_time_spent()

        pages = Page.objects.all().select_related("domain")
        total_updates = pages.count()
        i = 0
        domain_agg_scores = {}
        for page in pages:
            Ratings.objects.filter(page=page)
            page.agg_score = Ratings.objects.filter(page=page).\
                                aggregate(Avg('score'))["score__avg"]
            if page.agg_score:
                if not page.domain.url in domain_agg_scores:
                    domain_agg_scores[page.domain.url] = (0,0,page.domain)
                domain_agg_scores[page.domain.url] = (page.agg_score + \
                                            domain_agg_scores[page.domain.url][0],
                                            1+domain_agg_scores[page.domain.url][1],
                                            domain_agg_scores[page.domain.url][2])
            page.save()
            if i != 0 and i % CHUNK_SIZE == 0:
                self._log_updates(i, total_updates, 'page_scores')

            i+=1

        self._update_domain_scores(domain_agg_scores)


    def _update_personalized_scores(self):
        #Figure out path
        user_item_scores = subprocess.check_output(['java', '-jar', 'recommender.jar'])\
                .splitlines()
        for user_item_score in user_item_scores:
            user, item, score = tuple(user_item_score.split())
            user = int(user)
            item = int(user)
            personalized_rating,_ = PersonalizedRatings.get_or_create(user=int(user),
                                                                      item=int(item))
            try:
                personalized_rating.score = int(score)
                personalized_rating.save()
            except ValueError:
                print("%d, %d score is not defined\n" % (user, item))

    def _calculate_scores(self, user=None):
        self.log('_calculate_scores')

        # we should have lists of eyehistories, list of users,
        # list of messages, total time ago, and total time spent
        # populated for each popularhistory. Now we calculate
        # scores based on these things.

        if user:
            popular_history = PopularHistory.objects.filter(user=user).prefetch_related(
                'eye_hists', 'messages', 'visitors', 'popular_history')
        else:
            popular_history = PopularHistory.objects.all().prefetch_related(
                'eye_hists', 'messages', 'visitors', 'popular_history')

        for p in popular_history:
            try:
                eye_hist_count = p.eye_hists.count()
                if eye_hist_count == 0:
                    p.delete()
                    continue

                # avg time ago is total time ago / number of eyehistories
                time = p.total_time_ago / float(eye_hist_count)
                p.avg_time_ago = timezone.now() - \
                    datetime.timedelta(hours=time)

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

                tot_time = 0
                if p.total_time_spent > 20000:
                    tot_time = 20000
                else:
                    tot_time = p.total_time_spent

                num_time1 = float(tot_time) / \
                    float(eye_hist_count)

                num_time2 = float(p.total_time_spent) / \
                    float(eye_hist_count)

                time_score = float((num_time1) / 1000.0) / \
                    (float(p.total_time_ago) + 1.0)

                time_score_2 = float((num_time2 - 5000) / 1000.0) / \
                    float(
                        ((
                            float(p.total_time_ago) + 1.0) /
                            float(eye_hist_count)) ** 1)
                p.avg_time_spent_score = time_score_2

                domain_score = 0.0

                if not user: # only do this for cron, not for user-specific since it adds time
                    # decrease factor if domain is popular
                    if p.popular_history.domain not in news_list:
                        num_domain_visits = EyeHistory.objects.filter(domain=p.popular_history.domain).count()
                        domain_score = float(num_domain_visits) / 5000.0

                    if p.popular_history.url.endswith('.com/') and p.visitors.count() > 4:
                        domain_score += 1.0

                personalized_score = 0.0
                if p.user:
                    personalized_score = PersonalizedRatings.get(page=p.popular_history.page,
                                                                user=p.user).score

                agg_score = p.popular_history.page.agg_score


                interaction_score = comment_score + visitor_score + time_score-\
                                    domain_score

                # top score combines all the scores together
                p.top_score = float((agg_score+personalized_score)*interaction_score)

                p.save()
            except Exception, e:
                self.log(e)
                continue
