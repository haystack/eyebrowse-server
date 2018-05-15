import json
import os
import urllib
import requests

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from annoying.decorators import ajax_request
from annoying.decorators import render_to

from urlparse import urlparse
from common.templatetags.gravatar import gravatar_for_user
from dateutil import tz
from datetime import datetime

from common.view_helpers import _template_values

from api.models import Domain, Page, Summary, SummaryHistory, EyeHistoryMessage
from tags.models import Highlight, CommonTag, TagCollection
from tags.models import Tag, Vote, UserTagInfo
from accounts.models import UserProfile
from stats.models import FBShareData


'''
Get page info
'''
@login_required
@ajax_request
def page(request):
  success = False
  user = request.user
  errors = {}
  page_info = {}

  if request.GET:
    url = process_url(request.GET.get('url'))
    errors['page'] = []

    try: 
      p = Page.objects.get(url=url)
      page_info = {
        "url": url,
        "title": p.title,
        "favicon_url": p.favicon_url,
        "domain": {
          "name": p.domain.name,
          "url": p.domain.url,
        } 
      }
      success = True

    except Page.DoesNotExist:  
      errors['page'].append("Page does not exist")

  return {
    'success': success,
    'errors': errors,
    'page': page_info,
  }

'''
Get all tags associated with a page (but not highlight)
'''
@login_required
@ajax_request
def tags_by_page(request):
  '''
  Getting all tags for a page
  '''
  success = False
  errors = {}
  tags = {}
  user = request.user
  if request.GET:
    url = process_url(request.GET.get('url'))
    errors['get_tags'] = []

    if not len(errors['get_tags']):
      vts = Tag.objects.filter(page__url=url, highlight=None)

      try:
        page = Page.objects.get(url=url)

        # get relevant info for each value tag
        for vt in vts:
          vt_info = {
            'user_voted': False,
            'name': vt.common_tag.name,
            'color': vt.common_tag.color,
            'description': vt.common_tag.description,
            'is_private': vt.is_private,
            'vote_count': len(Vote.objects.filter(tag=vt)),
          }

          tags[vt.common_tag.name] = vt_info
          success = True

        if success == False:
          errors['get_tags'].append("No tags for page " + url)
      except Page.DoesNotExist:
        errors['get_tags'].append("Page " + url + " does not exist")

  return {
    'success': success,
    'errors': errors,
    'tags': tags,
  }

'''
Get all tags associated with a highlight
'''
@login_required
@ajax_request
def tags_by_highlight(request):
  success = False
  errors = {}
  tags = {}
  sorted_tags = []
  user = request.user
  highlight = ''
  highlight_owner = ''

  if request.GET:
    highlight_id = request.GET.get('highlight_id')
    url = process_url(request.GET.get('url'))
    errors['get_tags'] = []

    if not len(errors['get_tags']):
      vts = Tag.objects.filter(highlight__id=highlight_id, page__url=url)
      highlight = Highlight.objects.get(id=highlight_id).highlight
      highlight_owner =  Highlight.objects.get(id=highlight_id).user.username
      # get relevant info for each value tag
      for vt in vts:
        vt_info = {
          'user_voted': False,
          'name': vt.common_tag.name,
          'color': vt.common_tag.color,
          'description': vt.common_tag.description,
          'is_private': vt.is_private,
          'vote_count': len(Vote.objects.filter(tag=vt)),
          'is_owner': (vt.user == user),
          'id': vt.id,
          'owner':vt.user.username, #to get the owner of the tag
        }

        votes = []
        vs = Vote.objects.filter(tag=vt)

        # get vote info
        for v in vs:
          if user == v.voter:
            vt_info['user_voted'] = True
          user_profile = UserProfile.objects.get(user=v.voter)
          pic = user_profile.pic_url
          if not pic:
            pic = gravatar_for_user(v.voter)
          votes.append({
            'name': user_profile.user.username,
            'pic': 'https://%s' % pic[7:],
          })
        vt_info['votes'] = votes
        sorted_tags.append(vt_info)
        success = True

  sorted_tags = sorted(sorted_tags, key=lambda x: x["vote_count"], reverse=True)

  return {
    'success': success,
    'errors': errors,
    'tags': sorted_tags,
    'highlight': highlight,
    'highlight_owner':highlight_owner,
  }

'''
Get all tags associated with a comment
'''
@login_required
@ajax_request
def tags_by_comment(request):
  success = False
  errors = {}
  tags = {}
  sorted_tags = []
  user = request.user
  if request.GET:
    eyehistory = request.GET.get('eyehistory')
    errors['get_tags'] = []

    if not len(errors['get_tags']):
      vts = Tag.objects.filter(comment__eyehistory__id=eyehistory)

      # get relevant info for each value tag
      for vt in vts:
        vt_info = {
          'user_voted': False,
          'name': vt.common_tag.name,
          'color': vt.common_tag.color,
          'description': vt.common_tag.description,
          'is_private': vt.is_private,
          'vote_count': len(Vote.objects.filter(tag=vt)),
          'is_owner': (vt.user == user),
        }

        votes = []
        vs = Vote.objects.filter(tag=vt)

        # get vote info
        for v in vs:
          if user == v.voter:
            vt_info['user_voted'] = True
          user_profile = UserProfile.objects.get(user=v.voter)
          pic = user_profile.pic_url
          if not pic:
            pic = gravatar_for_user(v.voter)
          votes.append({
            'name': user_profile.user.username,
            'pic': 'https://%s' % pic[7:],
          })
        vt_info['votes'] = votes
        sorted_tags.append(vt_info)
        success = True

  sorted_tags = sorted(sorted_tags, key=lambda x: x["vote_count"], reverse=True)

  return {
    'success': success,
    'errors': errors,
    'tags': sorted_tags,
  }

'''
A: 
  Adds domain
  Adds page 
    if page already exists
      get value tags for page
      if value tags don't exist
        do B

B:
  Count value tags in page content
  Add value tags to page
  Add value tags to user
  Returns value tags for page
'''
@csrf_exempt
@login_required
@ajax_request
def initialize_page(request):
  tags = {}
  errors = {}
  user = request.user
  count_tags = False
  highlights = 0

  if request.POST:
    url = process_url(request.POST.get('url'))
    favIconUrl = request.POST.get('favIconUrl')
    domain_name = request.POST.get('domain_name')
    title = request.POST.get('title')
    add_usertags = request.POST.get('add_usertags')

    domain = '{uri.netloc}'.format(uri=urlparse(url))
    errors['add_page'] = []

    title = url if title == "" else title

    # Add domain
    d, d_created = Domain.objects.get_or_create(url=domain)
    if domain_name is not None:
      d.name = domain_name
    d.save()

    # Add page
    try: 
      p = Page.objects.get(url=url)
      p.title = title
      p.save()
    except:
      if len(Page.objects.filter(url=url)) == 0:
        p = Page(url=url, domain=d)
        p.title = title
        p.save()
        count_tags = True
      else:
        errors['add_page'].append("More than one page exists")

    if len(errors['add_page']) == 0:
      highlights = len(Highlight.objects.filter(page__url=url))
      vts = Tag.objects.filter(page__url=url, highlight=None)
      if len(vts) == 0:
        count_tags = True
      
      for vt in vts:
        vt_info = {
          'user_voted': False,
          'name': vt.common_tag.name,
          'color': vt.common_tag.color,
          'description': vt.common_tag.description,
          'is_private': vt.is_private,
          'vote_count': len(Vote.objects.filter(tag=vt)),
        }

        tags[vt.common_tag.name] = vt_info

        # Add tag to user
        if add_usertags == "true":
          uti, created = UserTagInfo.objects.get_or_create(user=user, page=p, tag=vt)
          uti.save()

      if count_tags:
        errors['get_tc'] = []
        try:
          tc = TagCollection.objects.get(subscribers=user)
          trie = json.loads(tc.trie_blob)
        except: 
          errors['get_tc'].append('User not subscribed')

        if len(errors['get_tc']) == 0:
          # Count value tags for page
          r = requests.get(url, verify=False)
          emotes = countEmote(r.text, trie)
          ts = [(e, emotes[e]) for e in emotes if e]
          sorted(ts, key=lambda x: x[1], reverse=True)

          errors['add_valuetags'] = []

          if len(ts) == 0:
            errors['add_valuetags'].append('No tags counted')

          count = 3
          for tag in ts:
            if tag[1] > 2 and count > 0:
              count -= 1
              name = tag[0]

              # Add tag to page
              try:
                vt = Tag.objects.get(page__url=url, common_tag__name=name, highlight=None)
              except Tag.DoesNotExist:
                try:
                  common_tag = CommonTag.objects.get(name=name)
                  vt = Tag(page=p, common_tag=common_tag, word_count=tag[1])
                  vt.save()

                  # Add tag to user
                  if add_usertags == "true":
                    uti, created = UserTagInfo.objects.get_or_create(user=user, page=p, tag=vt)
                    uti.save()
                except CommonTag.DoesNotExist:
                  errors['add_valuetags'].append("Could not get base tag")

              if len(errors['add_valuetags']) == 0:
                tags[name] = {
                  'name': name,
                  'color': vt.common_tag.color,
                  'description': vt.common_tag.description,
                }

      success = True
      for error_field in errors:
        if errors[error_field] != []:
          success = False

    return {
      'success': success,
      'errors': errors,
      'tags': tags,
      'highlights': highlights,
    }

'''
initialize page using highlights 
'''
@csrf_exempt
@login_required
@ajax_request
def initialize_page_highlights(request):
  errors = {}
  user = request.user
  if user == None:
    print "user not found"
    return{
    'success': False,
    'errors': "user not found"
    }
  highlights = 0

  if request.POST:
    url = process_url(request.POST.get('url'))
    favIconUrl = request.POST.get('favIconUrl')
    domain_name = request.POST.get('domain_name')
    title = request.POST.get('title')

    domain = '{uri.netloc}'.format(uri=urlparse(url))
    errors['add_page'] = []

    title = url if title == "" else title

    # Add domain
    d, d_created = Domain.objects.get_or_create(url=domain)
    if domain_name is not None:
      d.name = domain_name
    d.save()

    # Add page
    try: 
      p = Page.objects.get(url=url)
      p.title = title
      p.save()
    except:
      if len(Page.objects.filter(url=url)) == 0:
        p = Page(url=url, domain=d)
        p.title = title
        p.save()
      else:
        errors['add_page'].append("More than one page exists")

    if len(errors['add_page']) == 0:
      highlights = len(Highlight.objects.filter(page__url=url))
      success = True
      for error_field in errors:
        if errors[error_field] != []:
          success = False

    return {
      'success': success,
      'errors': errors,
      'highlights': highlights,
    }  
  
'''
Add a vote to a value tag
'''
@csrf_exempt
@login_required
@ajax_request
def add_vote(request):
  user = request.user
  success = False
  errors = {}
  vote_count = 0

  if request.POST:
    tag_id = request.POST.get('tag_id')
    errors['add_vote'] = []
    vt = None

    try:
      vt = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
      errors['add_vote'].append("Tag " + tag_name + " does not exist")

    if vt is not None:
      v, created = Vote.objects.get_or_create(tag=vt, voter=user)
      v.save()

      vote_count = len(Vote.objects.filter(tag=vt))
      success = True

  return {
    'success': success,
    'errors': errors,
    'vote_count': vote_count
  }

'''
Remove a vote from a value tag
'''
@csrf_exempt
@login_required
@ajax_request
def remove_vote(request):
  user = request.user
  success = False
  errors = {}
  vote_count = 0

  if request.POST:
    tag_id = request.POST.get('tag_id')
    errors['remove_vote'] = []

    try:
      vt = Tag.objects.get(id=tag_id)
      old_votes = Vote.objects.filter(tag=vt, voter=user)

      if len(old_votes) > 0:
        old_votes.delete()
        success = True

      vote_count = len(Vote.objects.filter(tag=vt))

    except Tag.DoesNotExist:
      errors['remove_vote'].append("Tag " + tag_name + " does not exist")

  return {
    'success': success,
    'errors': errors,
    'vote_count': vote_count
  }

'''
Add a highlight to a page
'''
@csrf_exempt
@login_required
@ajax_request
def highlight(request):
  success = False
  user = request.user
  errors = {}
  data = {}

  if request.POST:
    url = process_url(request.POST.get('url'))
    highlight = request.POST.get('highlight')
    highlight_id = request.POST.get('highlight_id')
    errors['add_highlight'] = []

    if highlight != "" or highlight_id:
      p = Page.objects.get(url=url)

      if highlight_id: 
        try:
          h = Highlight.objects.get(id=highlight_id)
          data['highlight_id'] = h.id
        except: 
          errors['add_highlight'].append('Get highlight failed')
      else:
        try:
          h, created = Highlight.objects.get_or_create(page=p, highlight=highlight)
          h.user = user
          h.save()

          success = True
          data['highlight_id'] = h.id
        except:
          errors['add_highlight'].append('Add highlight failed')

  return {
    'success': success,
    'errors': errors,
    'data': data,
  }

'''
Get highlight by highlight id
'''
@login_required
@ajax_request
def highlight_by_id(request):
  success = False
  errors = {}
  tags = {}
  sorted_tags = []
  user = request.user
  if user == None:
    print "user not found"
    return{
    'success': False,
    'errors': "user not found"
    }
  highlight = ''
  highlight_owner = ''

  if request.GET:
    highlight_id = request.GET.get('highlight_id')
    url = process_url(request.GET.get('url'))
    errors['get_highlights'] = []

    if not len(errors['get_highlights']):
      highlight = Highlight.objects.get(id=highlight_id).highlight
      highlight_owner =  Highlight.objects.get(id=highlight_id).user.username
      success = True

  return {
    'success': success,
    'errors': errors,
    'highlight': highlight,
    'highlight_owner':highlight_owner,
  }

'''
Get all highlights for a page
'''
@login_required
@ajax_request
def highlights(request):
  success = False
  errors = {}
  user = request.user
  data = {}
  highlights = {}

  if request.GET:
    url = process_url(request.GET.get('url'))
    errors['get_highlights'] = []

    if not len(errors['get_highlights']):
      hs = Highlight.objects.filter(page__url=url)
      for h in hs:
        comments = []
        eyehist_message = EyeHistoryMessage.objects.filter(highlight__id=h.id)
        for m in eyehist_message:
          comments.append({
            'comment': m.message,
          })
         

        highlights[h.highlight] = {
          'id': h.id,
          'comment_count':len(comments),
          'is_owner': h.user == user,
        }
      success = True

  return {
    'success': success,
    'errors': errors,
    'highlights': highlights,
  }

'''
Delete a highlight
'''
@csrf_exempt
@login_required
@ajax_request
def delete_highlight(request):
  success = False
  errors = {}
  user = request.user
  errors['delete_highlight'] = []

  if request.POST:
    highlight = request.POST.get('highlight')
    h = None

    try:
      h = Highlight.objects.get(id=highlight)
    except:
      errors['delete_highlight'].append("Highlight does not exist")

    if len(errors['delete_highlight']) == 0:
      if h.user == user:
        h.delete()
        success = True

  return {
    'success': success,
    'errors': errors,
  }


'''
Get related stories
'''
@login_required
@ajax_request
def related_stories(request):
  success = False
  errors = {}
  page_info = {}
  data = {}
  errors['related_stories'] = []

  if request.GET:
    url = process_url(request.GET.get('url'))
    api_url = "https://api.newsapi.aylien.com/api/v1/related_stories"

    payload = {
      "story_url": url,
      "return[]": ["id", "summary", "title", "source", "links", "body"],
      "source.rankings.alexa.rank.max": 2000,
      "language": ["en"],
      "per_page": 5,
    }

    headers = {
      "Access-Control-Allow-Origin": "*",
      "X-AYLIEN-NewsAPI-Application-ID": "c3cc0e6d",
      "X-AYLIEN-NewsAPI-Application-Key": " c548d0a8164ee2b74854d946817d8909",
    }

    r = requests.get(api_url, params=payload, headers=headers)

    if r.status_code == 200:
      for item in r.json()["related_stories"]:
        if "logo_url" in item["source"]:
          logo = item["source"]["logo_url"]
        else:
          logo = ""

        data[item["id"]] = {
          "title": item["title"],
          "link": item["links"]["permalink"],
          "source": item["source"]["name"],
          "domain": item["source"]["domain"],
          "logo": logo,
          "summary": item["body"],
        }

      success = True
    else:
      errors['related_stories'].append("Could not fetch related stories")

  return {
    'success': success,
    'errors': errors,
    'data': data,
  }

'''
Get value tags associated with a user
'''
@csrf_exempt
@login_required
@ajax_request
def user_value_tags(request):
  success = False
  errors = {}
  data = {}
  user = request.user
  errors['user_value_tags'] = []

  if request.GET:
    tag_counts = {}
    uts = UserTagInfo.objects.filter(user=user)

    if len(uts) != 0:
      for ut in uts:
        if ut.tag.common_tag.name in tag_counts:
          tag_counts[ut.tag.common_tag.name] += 1
        else:
          tag_counts[ut.tag.common_tag.name] = 1
      data['tag_counts'] = tag_counts
      success = True

    else:
      errors['user_value_tags'].append("No user tag info")

  return {
    'success': success,
    'errors': errors,
    'data': data,
  }

@login_required
@ajax_request
def common_tags(request):
  success = False
  user = request.user
  common_tags = {}
  errors = {}
  errors['common_tags'] = []

  bts = CommonTag.objects.all()
  for bt in bts:
    common_tags[bt.name] = {
      'description': bt.description,
      'color': bt.color,
    }

  success = True

  return {
    'success': success,
    'errors': errors,
    'common_tags': common_tags,
  }

@csrf_exempt
@login_required
@ajax_request
def page_summary(request):
  success = False
  user = request.user
  data = {}
  errors = {}
  errors['page_summary'] = []
  data['summary'] = {
    'summary': '',
  }

  if request.GET:
    url = process_url(request.GET.get('url'))

    try:
      p = Page.objects.get(url=url)
      s, s_created = Summary.objects.get_or_create(page=p)

      from_zone = tz.tzutc()
      to_zone = tz.tzlocal()

      date = s.date.replace(tzinfo=from_zone)
      local = date.astimezone(to_zone)

      data['summary'] = {
        'summary': s.summary,
        'user': s.last_editor.username,
        'date': local.strftime('%b %m, %Y,  %I:%M %p'),
      }
      success = True
    except:
      errors['page_summary'].append('Could not get page ' + url)

  if request.POST:
    url = process_url(request.POST.get('url'))
    domain = '{uri.netloc}'.format(uri=urlparse(url))
    summary = request.POST.get('summary')

    try:
      d, d_created = Domain.objects.get_or_create(url=domain)
      d.save()

      if len(Page.objects.filter(url=url)) == 0:
        p = Page(url=url, domain=d)
        p.save()
      else:
        p = Page.objects.get(url=url)

      s, s_created = Summary.objects.get_or_create(page=p)
      prev_summary = s.summary
      sh = SummaryHistory(user=user, new_summary=summary, previous_summary=prev_summary, summary=s)
      sh.save()

      s.summary = summary
      s.last_editor = user
      s.date = datetime.now()
      s.save()

      from_zone = tz.tzutc()
      to_zone = tz.tzlocal()

      local = s.date.replace(tzinfo=from_zone)

      data['summary'] = {
        'summary': summary,
        'user': user.username,
        'date': local.strftime('%b %m, %Y,  %I:%M %p'),
      }
      success = True
    except: 
      errors['page_summary'].append('Could not get page ' + url)

  return {
    'success': success,
    'errors': errors,
    'data': data,
  }

'''
load comments for each highlight
'''
@login_required
@ajax_request
def comments_by_highlight(request):
  success = False
  errors = {}
  comments = []
  errors['comments_by_highlight'] = []
  user = request.user
  user_contributed = False

  hl_id = request.GET.get('highlight_id')

  eyehist_message = EyeHistoryMessage.objects.filter(highlight__id=hl_id)

  if len(comments) != 0:
    success = True
    
  for m in eyehist_message:
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    date = m.post_time.replace(tzinfo=from_zone)
    local = date.astimezone(to_zone)

    user_profile = UserProfile.objects.get(user=m.eyehistory.user) 
    pic = user_profile.pic_url

    if not pic:
      pic = gravatar_for_user(m.eyehistory.user)
      
    pic = 'https://%s' % pic[7:]

    comments.append({
      'comment': m.message,
      'date': local.strftime('%b %m, %Y,  %I:%M %p'),
      'time': local.strftime("%s"),
      'user': m.eyehistory.user.username,
      'prof_pic': pic,
      'id': m.id,
    })

  return {
    'success': success,
    'errors': errors,
    'comments': sorted(comments, key=lambda x:x['time']),
    'user_contributed': user_contributed,
  }

#delete a comment
@csrf_exempt
@login_required
@ajax_request
def remove_comment(request):
  success = False
  user = request.user
  errors = {}

  if request.POST:
    comment = request.POST.get('comment_id')
    errors['remove_comment'] = []

    try:
      c = EyeHistoryMessage.objects.get(id=comment, eyehistory__user=user)
      c.delete()
      success = True
    except:
      errors['remove_comment'].append("Could not get comment " + comment)

  return {
    'success': success,
    'errors': errors,
  }

@csrf_exempt
@login_required
@ajax_request
def edit_comment(request):
  success = False
  user = request.user
  errors = {}

  if request.POST:
    comment_id = request.POST.get('comment_id')
    new_comment = request.POST.get('new_comment')
    errors['edit_comment'] = []

    try:
      c = EyeHistoryMessage.objects.get(id=comment_id)
      c.message = new_comment
      c.save()
      success = True
    except:
      errors['edit_comment'].append("Could not get comment " + comment)

  return {
    'success': success,
    'errors': errors,
  }


@login_required
@ajax_request
def comments_by_page(request):
  success = False
  errors = {}
  data = {}
  highlights = {}
  errors['comments_by_page'] = []

  if request.GET:
    url = process_url(request.GET.get('url'))

    try:
      cs = EyeHistoryMessage.objects.filter(highlight__page__url=url)
      for c in cs:
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        date = c.post_time.replace(tzinfo=from_zone)
        local = date.astimezone(to_zone)

        user_profile = UserProfile.objects.get(user=c.eyehistory.user) 
        pic = user_profile.pic_url

        if not pic:
          pic = gravatar_for_user(c.eyehistory.user) 

        pic = 'https://%s' % pic[7:]

        if c.highlight.id in data:
          data[c.highlight.id].append({
            'comment': c.message,
            'date': local.strftime('%b %m, %Y,  %I:%M %p'),
            'user': c.eyehistory.user.username,
            'prof_pic': pic,
            'id': c.id,
          })

        else:
          data[c.highlight.id] = [{
            'comment': c.message,
            'date': local.strftime('%b %m, %Y,  %I:%M %p'),
            'user': c.eyehistory.user.username,
            'prof_pic': pic,
            'id': c.id,
          }]

        highlights[c.highlight.id] = c.highlight.highlight

        success = True
    except:
      errors['comments_by_page'].append('Could not get comments')

  return {
    'success': success,
    'errors': errors,
    'comments': data,
    'highlights': highlights,
  }

@login_required
@render_to('tags/fb_share.html')
def fb_share(request):
  user = request.user 
  if request.GET:
    url = request.GET.get('url')
    text = request.GET.get('text')

    try:
      fb = FBShareData(user=user, url_shared=url, message=text)
      fb.save()
    except:
      pass

    return _template_values(request, page_title="FB share", 
                            url=url, text=text)

# Helper function to parse urls minus query strings
def process_url(url):
  for i in range(len(url)):
    if url[i] == "?":
      return url[:i]

  return url

# Helper trie functions
def in_trie(trie, word):
  _end = '_end_'
  current_dict = trie
  for letter in word: 
    if letter in current_dict:
      current_dict = current_dict[letter]
    elif "*" in current_dict:
      return current_dict["*"][_end][1]
    else:
      return False
  else:
    if _end in current_dict:
      return current_dict[_end][1]
    elif "*" in current_dict:
      return current_dict["*"][_end][1]
    else:
      return False

def countEmote(text, trie):
  count = 0
  emote_dict = {}
  for word in text.split(" "):
    if word.isalpha():
      count += 1
      state = in_trie(trie, word)
      if state in emote_dict:
        emote_dict[state] += 1
      else:
        emote_dict[state] = 1

  return emote_dict if count > 500 else {}


