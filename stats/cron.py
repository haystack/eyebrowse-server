import kronos

from stats.cron_tasks.calculate_stats import user_stat_gen

@kronos.register("0 * * * *")   
def hourly_cron():
    user_stat_gen()