import types
import datetime
from tempfile import NamedTemporaryFile
from ConfigParser import SafeConfigParser

from django.conf import settings
import pexpect

from control.utils import pam
from samba_manager.models import ManageableGroup, ManageableShare, ManageableUser


def run_as_root(command):
    """
    Login as root and execute a command returning a spawned process
    @param command: command to be executed.
    @return: pexpect.spawn
    """

    # Now login as root to run command
    command_line = 'sudo su root -c "{0}"'.format(command)
    process = pexpect.spawn(command_line)
    process.logfile = open(settings.LOGFILE, 'wa')

    process.expect('Password: ')
    process.sendline(settings.ROOT_PASSWORD)

    return process


def change_password(username, old_password, new_password, admin=False):
    if not admin:
        if not pam.authenticate(username, old_password):
            return 'Error authenthicating. Check the error log for more info'

    process = run_as_root('passwd {0}'.format(username))

    if type(process) is types.StringType:
        return process

    process.expect('Enter new UNIX password: ')
    process.sendline(new_password)
    process.expect('Retype new UNIX password: ')
    process.sendline(new_password)
    i = process.expect(['passwd: password updated successfully', 'new password is too simple'])
    if i == 0:
        return True
    if i == 1:
        return 'This password is too easy! Use at least 6 chars'


def add_user(username, password):
    user = ManageableUser.objects.filter(name=username)
    if len(user) == 0:
        process = run_as_root('useradd "{username}" --home "{home}"'.format(
            home=settings.USER_HOME_DIR.format(username), username=username))
        process.expect(pexpect.EOF)

        process = run_as_root('smbpasswd -a "{0}"'.format(username))
        
        process.expect('New SMB password:')
        process.sendline(password)
        
        process.expect('Retype new SMB password:')
        process.sendline(password)
        
        process.expect(pexpect.EOF)
        
        ManageableUser.objects.create(name=username)
        return True
    else:
        return False


def del_user(username):
    user = ManageableUser.objects.filter(name=username)
    if len(user):
        process = run_as_root('smbpasswd -x "{0}"'.format(username))
        process.expect(pexpect.EOF)
        process = run_as_root('deluser "{0}"'.format(username))
        process.expect(pexpect.EOF)
        user.delete()
        return True
    else:
        return False


def add_group(group_name):
    groups = ManageableGroup.objects.filter(name=group_name)
    if len(groups) == 0:
        process = run_as_root('addgroup "{0}"'.format(group_name))
        process.expect(pexpect.EOF)
        ManageableGroup.objects.create(name=group_name)
        return True
    else:
        return False


def del_group(group_name):
    groups = ManageableGroup.objects.filter(name=group_name)
    if len(groups):
        process = run_as_root('delgroup "{0}"'.format(group_name))
        process.expect(pexpect.EOF)
        groups.delete()
        return True
    else:
        return False


def get_user_groups(username):
    process = pexpect.spawn('groups {0}'.format(username))
    process.expect(pexpect.EOF)
    return process.before.split(':')[1].strip().split(' ')


def get_user_groups_tuple(username):
    users = get_user_groups(username)
    users_list = []
    for user in users:
        users_list.append((user, user))
    return tuple(users_list)


def add_user_group(username, group_name):
    if group_name in get_user_groups(username):
        process = run_as_root('addgroup "{0}" "{1}"'.format(username, group_name))
        process.expect(pexpect.EOF)
        return True
    else:
        return False


def del_user_group(username, group_name):
    user_groups = get_user_groups(username)
    if group_name in user_groups:
        user_groups.remove(group_name)
        user_groups = ','.join(user_groups)
        process = run_as_root('usermod -G "{0}" "{1}"'.format(user_groups, username))
        process.expect(pexpect.EOF)
        return True
    else:
        return False


def set_user_groups(username, groups):
    group_list = list()
    for item in groups:
        group_list.append(str(item))
    group_list.append(username)
    group_list = ','.join(group_list)
    process = run_as_root('usermod -G "{0}" "{1}"'.format(group_list, username))
    process.expect(pexpect.EOF)
    return True


def get_samba_conf():
    config = SafeConfigParser()
    config.read(settings.SAMBA_CONF)
    return config


def get_samba_shares(config):
    manageable_shares_db = ManageableShare.objects.all()
    manageable_shares = {}
    for share in manageable_shares_db:
        manageable_shares[share.name] = None
    samba_sections = config.sections()
    for section in samba_sections:
        if section in manageable_shares:
            manageable_shares[section] = config.items(section)
    return manageable_shares


def _save_samba_share(conf):
    temp = NamedTemporaryFile('w', delete=False)
    
    conf.write(temp)
    temp.close()
    bkp_date = datetime.datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss')
    process = run_as_root('cp "/etc/samba/smb.conf" "/etc/samba/smb.conf-{0}.bkp"'.format(bkp_date))
    process.expect(pexpect.EOF)

    process = run_as_root('cp "{0}" "/etc/samba/smb.conf"'.format(temp.name))
    process.expect(pexpect.EOF)
    
    process = run_as_root('chmod 644 /etc/samba/smb.conf')
    process.expect(pexpect.EOF)
    
    process = run_as_root('chown root:root /etc/samba/smb.conf')
    process.expect(pexpect.EOF)
    temp.unlink(temp.name)


def add_change_samba_share(confs):
    name = confs.get('name', None)
    comment = confs.get('comment', None)
    groups = confs.get('allowed_groups', None)
    conf = get_samba_conf()
    path = settings.SAMBA_SHARES_DIR.format(name)
    
    if not conf.has_section(name):
        ManageableShare.objects.create(name=name)
        process = run_as_root('mkdir -p "{0}"'.format(path))
        process.expect(pexpect.EOF)
        process = run_as_root('chmod 777 "{0}"'.format(path))
        process.expect(pexpect.EOF)
        conf.add_section(name)
        conf.set(name, 'guest ok', 'no')
        conf.set(name, 'browseable', 'yes')
        conf.set(name, 'writable', 'yes')
        conf.set(name, 'create mask', '0660')
        conf.set(name, 'directory mask', '0770')
        conf.set(name, 'vfs objects', 'recycle')
    conf.set(name, 'path', path)
    conf.set(name, 'comment', comment)
    conf.set(name, 'valid users', ' '.join(map(lambda x: '@' + x, [x.name for x in groups])))
    _save_samba_share(conf)
    return True


def del_samba_share(share_name):
    conf = get_samba_conf()
    if conf.has_section(share_name):
        conf.remove_section(share_name)
        _save_samba_share(conf)
        ManageableShare.objects.get(name=share_name).delete()
    return True


