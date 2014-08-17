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

## IN PROGRESS
* class based views samba

* log all actions and errors to a log file through remote executor
* Replace pam module with sudo 
* Refactor utils to use sudo approved external executor that checks the database is the command is present in models
* use executor logic to add samba actions

## TODO:

* write unit tests
* write samba config file function
* sync users option: Sync users in database with users on the system
* fix no section exception (section not present in samba file) when editting on a no samba machine (mac):
  - alert and opt-in to write new config file 
  - alert and continue 

* catch pexpect exceptions and return a nice web based error line
* create some decent html
* Write docs and a nice README
* Add some screenshots to docs
* Add clean docstrings to all functions
* Use django bootstrap for forms

## LONGTERM TODO
* replace user configuration with LDAP
* Add LDAP admin panel