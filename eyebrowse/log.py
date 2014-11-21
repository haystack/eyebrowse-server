import logging
import logging.handlers
import cloghandler
from settings import DEBUG

if DEBUG:
  LOG_LEVEL = logging.DEBUG
else:
  LOG_LEVEL = logging.INFO

LOG_PATH = '/var/opt/eyebrowse/logs/'

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(message)s')
logger = logging.getLogger('eyebrowse')

try:
  filehandler = cloghandler.ConcurrentRotatingFileHandler(''.join(
      [LOG_PATH, 'eyebrowse.log']), mode='a', maxBytes=10 * 2 ** 20, backupCount=3)
  filehandler.setLevel(LOG_LEVEL)
  filehandler.setFormatter(formatter)
  logger.addHandler(filehandler)

  handler = logging.StreamHandler()
  handler.setLevel(LOG_LEVEL)
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.setLevel(LOG_LEVEL)
except IOError:
  pass  # no log file
