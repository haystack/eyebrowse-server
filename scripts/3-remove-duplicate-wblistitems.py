import setup_django
from django.db import models
from api.models import WhiteListItem, BlackListItem

"""
Remove duplicates, keeping the one with greatest id
"""

def remove_duplicates(model, unique_fields):
    
    duplicates = (model.objects.values(*unique_fields)
                             .annotate(max_id=models.Max('id'),
                                       count_id=models.Count('id'))
                             .filter(count_id__gt=1)
                             .order_by())
    
    print duplicates
 
    for duplicate in duplicates:
        (model.objects.filter(**{x: duplicate[x] for x in unique_fields})
                        .exclude(id=duplicate['max_id'])
                        .delete())
    
if __name__ == '__main__':

    remove_duplicates(WhiteListItem, ['user', 'url', 'type'])
    remove_duplicates(BlackListItem, ['user', 'url', 'type'])