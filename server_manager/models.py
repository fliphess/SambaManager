from django.db import models


class ServerCommand(models.Model):
    system_cmd = models.BooleanField('system_cmd', default=False)
    visible = models.BooleanField('visible', default=True)
    sudo = models.BooleanField('sudo', default=False)
    name = models.CharField('name', max_length=100, unique=True)
    command = models.CharField('command', max_length=100, unique=False)
    title = models.CharField('title', max_length=100, unique=False)

    def __unicode__(self):
        return self.name
