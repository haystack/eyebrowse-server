
def humanize_time(time_delta):
    second_diff = time_delta.seconds
    day_diff = time_delta.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 60:
            return "a few seconds"
        if second_diff < 120:
            return  "a minute"
        if second_diff < 3600:
            return str( second_diff / 60 ) + " minutes"
        if second_diff < 7200:
            return "an hour"
        if second_diff < 86400:
            return str( second_diff / 3600 ) + " hours"
    if day_diff == 1:
        return "a day"
    if day_diff < 7:
        return str(day_diff) + " days"
    if day_diff < 31:
        return str(day_diff/7) + " weeks"
    if day_diff < 365:
        return str(day_diff/30) + " months"
    return str(day_diff/365) + " years"

            