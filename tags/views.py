import json
import os
import urllib
import requests

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from annoying.decorators import ajax_request
from urlparse import urlparse
from common.templatetags.gravatar import gravatar_for_user

from api.models import Domain, Page
from tags.models import Highlight, CommonTag, TagCollection
from tags.models import Tag, Vote, UserTagInfo
from accounts.models import UserProfile

'''
Add a value tag
'''
@login_required
@ajax_request
def value_tag(request):
  user = request.user
  success = False
  errors = {}

  # Add a new tag
  if request.POST:
    tag_name = request.POST.get('name')
    url = process_url(request.POST.get('url'))
    errors['add_tag'] = []

    try:
      page = Page.objects.get(url=url)

      if len(Tag.objects.filter(common_tag__name=tag_name, page__url=url)) > 0:
        errors['add_tag'].append("Tag " + tag_name + " already exists")
      else:
        try:
          common_tag = CommonTag.objects.get(name=tag_name)
          new_tag = Tag(
            user=user, 
            page=page,
            common_tag=common_tag
          )
          new_tag.save()
          success = True
        except CommonTag.DoesNotExist:
          errors['add_tag'].append("Could not find base tag " + tag_name)

    except Page.DoesNotExist:
      errors['add_tag'].append("Page " + url + " does not exist")

  return {
    'success': success,
    'errors': errors,
  }

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

  if request.GET:
    highlight = request.GET.get('highlight')
    url = process_url(request.GET.get('url'))
    errors['get_tags'] = []

    if not len(errors['get_tags']):
      vts = Tag.objects.filter(highlight__id=highlight, page__url=url)

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
            'name': user_profile.get_full_name(),
            'pic': pic,
          })
        vt_info['votes'] = votes
        sorted_tags.append(vt_info)

  sorted_tags = sorted(sorted_tags, key=lambda x: x["vote_count"], reverse=True)

  return {
    'success': success,
    'errors': errors,
    'tags': sorted_tags,
  }


'''
A: 
  Adds domain
  Adds page; 
    if page already exists;
      get value tags for page
      if value tags don't exist;
        do B

B:
  Count value tags in page content
  Add value tags to page
  Add value tags to user
  Returns value tags for page
'''
@login_required
@ajax_request
def initialize_page(request):
  tags = {}
  errors = {}
  user = request.user
  count_tags = False

  if request.POST:
    url = process_url(request.POST.get('url'))
    domain_name = request.POST.get('domain_name')
    title = request.POST.get('title')
    add_usertags = request.POST.get('add_usertags')

    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))
    errors['add_page'] = []

    domain_name = domain if domain_name == "" else domain_name
    title = url if title == "" else title

    # Add domain
    d, d_created = Domain.objects.get_or_create(url=domain, name=domain_name)
    d.save()

    # Add page
    p, p_created = Page.objects.get_or_create(url=url, domain=d, title=title)
    p.save()

    vts = Tag.objects.filter(page__url=url, highlight=None)

    if p_created or len(vts) == 0:
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
      tc = TagCollection.objects.get(subscribers=user)
      trie = json.loads(tc.trie_blob)

      # Count value tags for page
      r = requests.get(url)
      emotes = countEmote(r.text, trie)
      ts = [(e, emotes[e]) for e in emotes if e]
      sorted(ts, key=lambda x: x[1], reverse=True)

      errors['add_valuetags'] = []
      for tag in ts:
        if tag[1] > 2:
          name = tag[0]

          # Add tag to page
          try:
            vt = Tag.objects.get(page__url=url, common_tag__name=name, highlight=None)
          except Tag.DoesNotExist:
            try:
              common_tag = CommonTag.objects.get(name=name)
              vt = Tag(
                user=user,
                page=p,
                common_tag=common_tag
              )
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
    }

'''
Add a vote to a value tag
'''
@login_required
@ajax_request
def add_vote(request):
  user = request.user
  success = False
  errors = {}
  vote_count = 0

  if request.POST:
    tag_name = request.POST.get('valuetag')
    url = process_url(request.POST.get('url'))
    highlight = request.POST.get('highlight')
    errors['add_vote'] = []
    vt = None

    try:
      vt = Tag.objects.get(
        common_tag__name=tag_name, 
        highlight__id=highlight, 
        page__url=url,
      )
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
@login_required
@ajax_request
def remove_vote(request):
  user = request.user
  success = False
  errors = {}
  vote_count = 0

  if request.POST:
    tag_name = request.POST.get('valuetag')
    url = process_url(request.POST.get('url'))
    highlight = request.POST.get('highlight')
    errors['remove_vote'] = []

    try:
      vt = Tag.objects.get(
        common_tag__name=tag_name, 
        highlight__id=highlight, 
        page__url=url,
      )
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
Add a highlight with value tags to a page
'''
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
    hl_id = request.POST.get('highlight_id')
    tags = json.loads(request.POST.get('tags'))
    errors['add_highlight'] = []

    if not len(errors['add_highlight']) and highlight != "":
      p = Page.objects.get(url=url)

      if hl_id:
        try:
          h = Highlight.objects.get(page=p, id=hl_id)
        except:
          errors['add_highlight'].append('Could not get highlight')
      else:
        h, created = Highlight.objects.get_or_create(page=p, highlight=highlight)
        h.save()

      if not len(errors['add_highlight']):
        for tag in tags:
          if len(Tag.objects.filter(highlight=h, common_tag__name=tag)) == 0:
            try:
              common_tag = CommonTag.objects.get(name=tag)
              vt = Tag(
                page=p, 
                highlight=h, 
                common_tag=common_tag,
                user=user, 
              )
              vt.save()
            except CommonTag.DoesNotExist:
              errors['add_highlight'].append("Base tag " + tag + " does not exist")

        success = True
        data['highlight_id'] = h.id

  return {
    'success': success,
    'errors': errors,
    'data': data,
  }

'''
Get all highlights for a page
'''
@login_required
@ajax_request
def highlights(request):
  success = False
  errors = {}
  data = {}
  highlights = {}
  max_tag = ()
  max_tag_count = 0

  if request.GET:
    url = process_url(request.GET.get('url'))
    errors['get_highlights'] = []

    if not len(errors['get_highlights']):
      hs = Highlight.objects.filter(page__url=url)
      for h in hs:
        max_tag = ()
        max_tag_count = 0

        vts = Tag.objects.filter(highlight=h, page__url=url)
        for vt in vts:
          vote_count = len(Vote.objects.filter(tag=vt))
          if vote_count >= max_tag_count:
            max_tag_count = vote_count
            max_tag = (vt.common_tag.name, vt.common_tag.color)
        highlights[h.highlight] = {
          'max_tag': max_tag,
          'id': h.id
        }
      success = True

  return {
    'success': success,
    'errors': errors,
    'highlights': highlights,
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
      "X-AYLIEN-NewsAPI-Application-ID": "649b72e1",
      "X-AYLIEN-NewsAPI-Application-Key": "ae45014e8f1e35a8f1435f0bba538840",
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
          "summary": item["body"]
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
  emote_dict = {}
  for word in text.split(" "):
    if word.isalpha():
      state = in_trie(trie, word)
      if state in emote_dict:
        emote_dict[state] += 1
      else:
        emote_dict[state] = 1
    
  return emote_dict


