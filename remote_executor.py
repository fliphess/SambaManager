#!/Users/flip/.virtualenvs/nas/bin/python
#/usr/bin/env python
import argparse
import os
import subprocess
import sys
from django.core.exceptions import ObjectDoesNotExist

sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "control.settings")
from server_manager.models import ServerCommand


def parse_options():
    parser = argparse.ArgumentParser(description="""
        Django Server Manager Remote Executor - Flip Hess 2014 - <flip@fliphess.com>
    """)
    parser.add_argument('-n', '--name', help='Where to find the settings file', required=True, type=str)
    parser.add_argument('-q', '--quiet', help='Be more silent', action='count', default=0)
    return parser.parse_args()


def run_command(script, sudo=False):
    output = []

    if sudo:
        script = "sudo %s" % script
    script += ' 2>&1'

    print('Running command: %s' % script)
    process = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        elif nextline == '\n' or nextline == '':
            continue
        output.append(nextline.strip())
    exitcode = process.returncode
    return output, exitcode


def main():
    arguments = parse_options()

    print('Getting database object for %s' % arguments.name)
    try:
        command = ServerCommand.objects.get(name=arguments.name)
    except ObjectDoesNotExist as e:
        print('Command %s not found in database: %s' % (arguments.name, e))
        sys.exit(1)

    output, exitcode = run_command(script=command.command, sudo=command.sudo)

    print
    print('Output for %s was:' % command.command)
    print
    for line in output:
        print line.strip("\n")

    if exitcode != 0:
        print
        print('FAIL - Command %s Failed! Exitcode was %s' % (command.name, exitcode))
        sys.exit(exitcode)
    else:
        print
        print('OK - Command %s exited with exitcode %s' % (command.name, exitcode))
        print
        print('All done!')
        sys.exit(0)

if __name__ == "__main__":
    main()
