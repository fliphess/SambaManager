from django.db import models


class ServerCommand(models.Model):
    system_cmd = models.BooleanField('system_cmd', default=False)
    visible = models.BooleanField('visible', default=True)
    sudo = models.BooleanField('sudo', default=False)
    name = models.CharField('name', max_length=100, unique=True)
    command = models.CharField('command', max_length=100, unique=False)
    title = models.CharField('title', max_length=100, unique=False)

    db_table = "command"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s" % {
            "system_cmd": self.system_cmd,
            "visible": self.visible,
            "sudo": self.sudo,
            "name": self.name,
            "command": self.command,
            "title": self.title
        }
