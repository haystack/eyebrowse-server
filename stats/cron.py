import kronos

from common.cron_tasks.add_favicons import add_favicons
from scripts.cron_tasks.populate_popular_history import update_popular_history
from stats.cron_tasks.calculate_stats import user_stat_gen
from notifications.cron_tasks.calculate_stats import emit_notices


@kronos.register("0 * * * *")
def hourly_cron():
    user_stat_gen()
    add_favicons()
    update_popular_history()
    emit_notices()
