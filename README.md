# Samba manager
This is a manager of samba's conf file to add shares, add users and groups to system.
It is totally written in python and django.
I did this about 2010 for personal usage and now I'm sharing it.

## What is missing?
Translation, make code prettier and upgrade django.

## Using it
Change settings.py to reflect your setup, here is the basic stuff.

```python
SAMBA_CONF = '/etc/samba/smb.conf'
USER_HOME_DIR = '/storage/arquivos/home/{0}'
SAMBA_SHARES_DIR = '/storage/arquivos/{0}'
```

## initial commit 2014
* Port to current django version
* Setup a basic twitter bootstrap skeleton
* Translated all templates to english
* Replaced auth with django auth
* Refactor old to new

## TODO:

* write unit tests
* catch pexpect exceptions and return a nice web based error line
* log all actions and errors to a log file
* create some decent html
* Write docs and a nice README
* Add some screenshots to docs
* Add clean docstrings to all functions
* Use django bootstrap for forms