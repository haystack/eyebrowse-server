import kronos

from stats.cron_tasks.calculate_stats import user_stat_gen
from common.cron_tasks.add_favicons import add_favicons


@kronos.register("0 * * * *")
def hourly_cron():
    user_stat_gen()
    add_favicons()
