from django.db import models


class ServerCommand(models.Model):
    enabled = models.BooleanField('enabled', default=False)
    sudo = models.BooleanField('sudo', default=False)
    name = models.CharField('name', max_length=100, unique=True)
    command = models.CharField('command', max_length=100, unique=False)
    title = models.CharField('title', max_length=100, unique=False)

    def __unicode__(self):
        return self.name
