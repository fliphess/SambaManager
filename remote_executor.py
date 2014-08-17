#!/usr/bin/env python
import argparse
import os
import sys
from django.core.exceptions import ObjectDoesNotExist
from control.utils.command import logger, run_command

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


def main():
    arguments = parse_options()
    l = logger("server_manager remote executor: %s" % arguments.name, arguments.quiet)

    l.info('Getting database object for %s' % arguments.name)
    try:
        command = ServerCommand.objects.get(name=arguments.name)
    except ObjectDoesNotExist as e:
        l.error('Command %s not found in database: %s' % (arguments.name, e))
        sys.exit(1)

    output, exitcode = run_command(script=command.command, log=l, sudo=command.sudo)

    if exitcode != 0:
        l.error('Command %s Failed! Exitcode was %s' % (command.name, exitcode))
        l.error('Output for %s was: %s' % (command.command, output))
        sys.exit(exitcode)
    else:
        l.info('OK - Command %s exited with exitcode %s' % (command.name, exitcode))
        l.info('Output for %s was: %s' % (command.command, output))

    l.info('All done!')


if __name__ == "__main__":
    main()