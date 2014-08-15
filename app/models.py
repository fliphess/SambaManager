from django.db import models


class ManageableUser(models.Model):
    name = models.CharField('user_name', max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class ManageableGroup(models.Model):
    name = models.CharField('group_name', max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class ManageableShare(models.Model):
    name = models.CharField('share_name', max_length=100, unique=True)

    def __unicode__(self):
        return self.name