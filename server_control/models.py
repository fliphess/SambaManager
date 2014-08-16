from django.db import models


class ServerCommand(models.Model):
    name = models.CharField('title', max_length=100, unique=True)
    command = models.CharField('command', max_length=100, unique=False)
    title = models.CharField('title', max_length=100, unique=False)
    enabled = models.BooleanField('enabled', default=False)

    def __unicode__(self):
        return self.name


