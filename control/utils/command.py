import logging
import subprocess
from django.conf import settings

def run_command(script, log, sudo=False):
    output = []

    if sudo:
        script = "sudo %s" % script
    script += ' 2>&1'

    log.info('Running command: %s' % script)
    process = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() != None:
            break
        elif nextline == '\n' or nextline == '':
            continue
        output.append(nextline)
        log.info('remote_executor - %s' % nextline.strip())
    exitcode = process.returncode
    return output, exitcode


def logger(name, verbosity=1):
    level = {
        3: logging.ERROR,
        2: logging.WARNING,
        1: logging.INFO,
        0: logging.DEBUG
    }.get(verbosity, logging.DEBUG)

    log = logging.getLogger(name=name)
    log.setLevel(level=level)

    fh = logging.FileHandler(settings.LOGFILE)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)-7s %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)
    return log
