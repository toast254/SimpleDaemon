#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import sys
import time
import logging
from AbstractDaemon import Daemon

# log verbosity : CRITICAL, ERROR, WARNING, INFO, DEBUG
logging.basicConfig(filename='MyDaemon.log', level='DEBUG')
logger = logging.getLogger(__name__)


def do_something():
    logger.debug('I\'m alive !')


class MyDaemon(Daemon):
    """An AbstractDaemon instance I named `MyDaemon`

    run method is now implemented and call `do_something()`,
    it's also called when the daemon is given `run-once` as parameter.
    """

    def run(self):
        while True:
            do_something()
            time.sleep(1 * 60 * 60)  # 1 hours = 1 * 60 minutes = 1 * 60 * 60 seconds


def usage_help():
    print('usage: ' + sys.argv[0] + ' start|stop|restart|status|help|run-once')


if __name__ == '__main__':
    daemon = MyDaemon('MyDaemon.pid')
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            print('Starting MyDaemon')
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print('Stopping MyDaemon')
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print('Restarting MyDaemon')
            daemon.restart()
        elif 'status' == sys.argv[1]:
            if daemon.status():
                print('running')
            else:
                print('not running')
        elif 'help' == sys.argv[1]:
            usage_help()
        elif 'run-once' == sys.argv[1]:
            do_something()
        else:
            print('Unknown argument')
            usage_help()
            sys.exit(2)
        sys.exit(0)
    else:
        print('No argument')
        usage_help()
        sys.exit(2)
