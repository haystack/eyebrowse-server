from django.conf.urls import patterns, url

urlpatterns = patterns('extension.views',
                       url(r'^trackPrompt$', 'prompt'),
                       url(r'^loginPrompt$', 'login'),
                       url(r'^loggedIn', 'logged_in'),
                       url(r'^getInfo', 'get_info'),
                       url(r'^bubbleInfo', 'bubble_info'),
                       url(r'^getTickerInfo', 'get_ticker_info'),
                       url(r'^getActiveUsers$', 'active'),
                       url(r'^getMessages$', 'get_messages'),
                       url(r'^getStats$', 'stats'),
                       url(r'^profilepic', 'profilepic'),
                       url(r'^getFriends$', 'get_friends')
                       )
