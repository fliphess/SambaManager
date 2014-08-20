from samba_manager.models import ManageableUser, ManageableGroup, ManageableShare


class Status(object):
    def __init__(self):
        self.message = None
        self.success = None
        self.status = dict()
        self.update()

    def __str__(self):
        return "Last handled action status object: %s" % self.status

    def set(self, message, success):
        self.success = success
        self.message = message
        self.update()

    def get(self):
        return self.status

    def update(self):
        self.status.update({'message': self.message, 'success': self.success})

    def add(self, item):
        self.status.update(dict(item))


class SambaTotals(object):
    def __init__(self):
        self.users = ManageableUser
        self.groups = ManageableGroup
        self.shares = ManageableShare

        self.total_users = self.users.objects.count()
        self.total_groups = self.groups.objects.count()
        self.total_shares = self.shares.objects.count()