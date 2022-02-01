from users.models import Manager, Lackey, User


def get_manager_lackeys(manager):
    """
    Filter to get manager lackeys from email manager
    """
    manager = Manager.objects.filter(manager__email=manager)
    lackeys = Lackey.objects.filter(manager__in=manager)
    lackeys = lackeys.values_list('lackey__email', flat=True)
    return lackeys
