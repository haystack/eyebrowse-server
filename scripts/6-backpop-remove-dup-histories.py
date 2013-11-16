import setup_django
from django.contrib.auth.models import User
from api.models import EyeHistory
import datetime

def merge_histories(histories):
    histories = list(histories)
    i = 0
    
    while i < len(histories) - 1:
        hist1 = histories[i]
        j = i + 1
        while j < len(histories):
            hist2 = histories[j]
            if hist1.end_time + datetime.timedelta(minutes=5) >= hist2.start_time:
                print 'merging %s and %s' % (hist1, hist2)
                hist1.end_time = hist2.end_time
                hist1.end_event = hist2.end_event
                elapsed_time = hist1.end_time - hist1.start_time
                hist1.total_time = int(round((elapsed_time.microseconds / 1.0E3) + (elapsed_time.seconds * 1000) + (elapsed_time.days * 8.64E7)))
                hist1.humanize_time = humanize_time(elapsed_time)
                hist2.delete()
                hist1.save()
                print 'deleting %s' % (hist2)
                j+=1
            else:
                i = j
                break

def run():
    for u in User.objects.all():
        urls = EyeHistory.objects.filter(user=u).values_list('url', flat=True).distinct()
        for url in urls:
            dup_histories = EyeHistory.objects.filter(user=u, url=url).order_by('start_time')
            merge_histories(dup_histories)
            
    

if __name__ == '__main__':
    run()