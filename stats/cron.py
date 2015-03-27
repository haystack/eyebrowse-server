import kronos

from common.cron_tasks.add_favicons import add_favicons
from common.cron_tasks.update_popular_history import update_popular_history
from stats.cron_tasks.calculate_stats import user_stat_gen
from notifications.cron_tasks.calculate_stats import emit_notices


@kronos.register('0 * * * *')
def hourly_cron():
    user_stat_gen()
    add_favicons()
    emit_notices()

@kronos.register('0 */6 * * *')
def six_hour_cron():
    update_popular_history()
