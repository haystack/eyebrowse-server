import sys
import time
import logging
import traceback
import base64

from django.core.mail import mail_admins
from django.contrib.sites.models import Site
from django.utils.six.moves import cPickle as pickle  # pylint: disable-msg=F

from .lockfile import FileLock, AlreadyLocked, LockTimeout
from .models import NoticeQueueBatch
from .signals import emitted_notices
from . import models as notification

from .compat import get_user_model
from .conf import settings


def acquire_lock(*args):
    if len(args) == 1:
        lock = FileLock(args[0])
    else:
        lock = FileLock("send_notices")

    logging.debug("acquiring lock...")
    try:
        lock.acquire(settings.PINAX_NOTIFICATIONS_LOCK_WAIT_TIMEOUT)
    except AlreadyLocked:
        logging.debug("lock already in place. quitting.")
        return
    except LockTimeout:
        logging.debug("waiting for the lock timed out. quitting.")
        return
    logging.debug("acquired.")
    return lock


def send_all(*args):
    lock = acquire_lock(*args)
    batches, sent, sent_actual = 0, 0, 0
    start_time = time.time()

    try:
        # nesting the try statement to be Python 2.4
        try:
            for queued_batch in NoticeQueueBatch.objects.all():
                notices = pickle.loads(base64.b64decode(queued_batch.pickled_data))
                for user, label, extra_context, sender in notices:
                    try:
                        user = get_user_model().objects.get(pk=user)
                        logging.info("emitting notice {0} to {1}".format(label, user))
                        # call this once per user to be atomic and allow for logging to
                        # accurately show how long each takes.
                        if notification.send_now([user], label, extra_context, sender):
                            sent_actual += 1
                    except get_user_model().DoesNotExist:
                        # Ignore deleted users, just warn about them
                        logging.warning(
                            "not emitting notice {0} to user {1} since it does not exist".format(
                                label,
                                user)
                        )
                    sent += 1
                queued_batch.delete()
                batches += 1
            emitted_notices.send(
                sender=NoticeQueueBatch,
                batches=batches,
                sent=sent,
                sent_actual=sent_actual,
                run_time="%.2f seconds" % (time.time() - start_time)
            )
        except Exception:  # pylint: disable-msg=W0703
            # get the exception
            _, e, _ = sys.exc_info()
            # email people
            current_site = Site.objects.get_current()
            subject = "[{0} emit_notices] {1}".format(current_site.name, e)
            message = "\n".join(
                traceback.format_exception(*sys.exc_info())  # pylint: disable-msg=W0142
            )
            mail_admins(subject, message, fail_silently=True)
            # log it as critical
            logging.critical("an exception occurred: {0}".format(e))
    finally:
        logging.debug("releasing lock...")
        lock.release()
        logging.debug("released.")

    logging.info("")
    logging.info("{0} batches, {1} sent".format(batches, sent,))
    logging.info("done in {0:.2f} seconds".format(time.time() - start_time))
