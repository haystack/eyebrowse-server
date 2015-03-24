from django.core.exceptions import ObjectDoesNotExist

from django.contrib.contenttypes.models import ContentType

from notifications.conf import settings


def load_media_defaults():
    media = []
    defaults = {}
    for key, backend in settings.PINAX_NOTIFICATIONS_BACKENDS.items():
        # key is a tuple (medium_id, backend_label)
        media.append(key)
        defaults[key[0]] = backend.spam_sensitivity
    return media, defaults


def notice_setting_for_user(user, notice_type, medium, scoping=None):
    """
    @@@ candidate for overriding via a hookset method so you can customize lookup at site level
    """
    kwargs = {
        "notice_type": notice_type,
        "medium": medium
    }
    if scoping:
        kwargs.update({
            "scoping_content_type": ContentType.objects.get_for_model(scoping),
            "scoping_object_id": scoping.pk
        })
    else:
        kwargs.update({
            "scoping_content_type__isnull": True,
            "scoping_object_id__isnull": True
        })
    try:
        return user.noticesetting_set.get(**kwargs)
    except ObjectDoesNotExist:
        _, NOTICE_MEDIA_DEFAULTS = load_media_defaults()
        if scoping is None:
            kwargs.pop("scoping_content_type__isnull")
            kwargs.pop("scoping_object_id__isnull")
            kwargs.update({
                "scoping_content_type": None,
                "scoping_object_id": None
            })
        default = (NOTICE_MEDIA_DEFAULTS[medium] <= notice_type.default)
        kwargs.update({"send": default})
        setting = user.noticesetting_set.create(**kwargs)
        return setting
