#!/Users/flip/.virtualenvs/nas/bin/python
#/usr/bin/env python
import argparse
import os
import subprocess
import sys
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

sys.path.append(".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "control.settings")
from server_manager.models import ServerCommand


def parse_options():
    parser = argparse.ArgumentParser(description="""
        Django Server Manager Remote Executor - Flip Hess 2014 - <flip@fliphess.com>
    """)
    parser.add_argument("-n", "--name", help="Where to find the settings file", required=False, type=str)
    parser.add_argument("-l", "--list", help="List all available options", required=False, action="store_true")
    parser.add_argument("-q", "--quiet", help="Be more silent", action="count", default=3   )
    args = parser.parse_args()

    if args.name and args.list:
        parser.error("Please choose one, can't have both")

    if not args.name and not args.list:
        parser.error("Please choose either one, can't have none")
    return args


def main():
    arguments = parse_options()

    if arguments.list:
        print("Getting all available items")
        for item in ServerCommand.objects.all():
            print "- %s" % item.name
        sys.exit(0)

    print("Getting database object for %s" % arguments.name)
    try:
        command = ServerCommand.objects.get(name=arguments.name)
    except ObjectDoesNotExist as e:
        print("Command %s not found in database: %s" % (arguments.name, e))
        sys.exit(1)

    if settings.DEVELOPMENT:
        print "\n\nBOGUS DATA", "-", "This instance is running in development mode\n\n"
        sys.exit(0)

    command_line = "%s 2>&1" % command.command
    if command.sudo:
        command_line = "sudo %s" % command_line

    print("Running command: %s" % command_line)
    process = subprocess.Popen(command_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        next_line = process.stdout.readline()
        if next_line == "" and process.poll() is not None:
            break
        elif next_line == "\n" or next_line == "":
            continue
        print next_line.strip("\n")
    exitcode = process.returncode

    if exitcode != 0:
        print("FAIL - Command %s Failed! Exitcode was %s" % (command.name, exitcode))
    else:
        print("OK - Command %s exited with exitcode %s" % (command.name, exitcode))

    print("\nAll done!\n")
    sys.exit(exitcode)


if __name__ == "__main__":
    main()