# -*- coding: utf-8 -*-

import sys
import time
import unittest
import threading
from AbstractDaemon import Daemon


class LaunchAbstractDaemon:
    """Launch an instance of AbstractDaemon
    """

    def __init__(self, pid_file: str):
        self.pid_file = pid_file
        self.daemon = Daemon(self.pid_file)

    def start(self):
        thread = threading.Thread(target=self.daemon.start, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()  # Start the execution

    def restart(self):
        thread = threading.Thread(target=self.daemon.restart, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()  # Start the execution


class TestAbstractDaemon(unittest.TestCase):
    """Test AbstractDaemon class.
    """

    def setUp(self):
        """Create a new Daemon obect.
        """
        self.pid_file = '/tmp/test.pid'
        self.daemon_launcher = LaunchAbstractDaemon(self.pid_file)
        self.daemon = Daemon(self.pid_file)

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_start(self):
        """Try to start a daemon.
        """
        self.daemon_launcher.start()
        time.sleep(1)
        self.assertTrue(self.daemon.status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_stop(self):
        """Try to stop a daemon.
        """
        self.daemon_launcher.start()
        time.sleep(1)
        self.daemon.stop()
        time.sleep(1)
        self.assertFalse(self.daemon.status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_restart(self):
        """Try to restart a daemon.
        """
        self.daemon_launcher.restart()
        time.sleep(1)
        self.assertTrue(self.daemon.status())

    def test_run(self):
        with self.assertRaises(NotImplementedError):
            self.daemon.run()

    def test_status(self):
        """Try to check status of a daemon.
        """
        self.assertFalse(self.daemon.status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_check_pid_stopped(self):
        """Try to check pid of a stopped daemon.
        """
        self.assertFalse(self.daemon.check_pid())
        self.daemon_launcher.start()
        time.sleep(1)
        self.daemon.stop()
        time.sleep(1)
        self.assertFalse(self.daemon.check_pid())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_check_pid_started(self):
        """Try to check pid of a started daemon.
        """
        self.daemon_launcher.start()
        time.sleep(1)
        self.assertTrue(self.daemon.check_pid())

    def test_del_pid(self):
        """Try to remove pid file of a daemon.
        """
        with self.assertRaises(FileNotFoundError):
            self.daemon.delpid()

    def tearDown(self):
        """Stop and delete the daemon object.
        """
        if self.daemon and self.daemon.status():
            self.daemon.stop()


if __name__ == '__main__':
    unittest.main()
