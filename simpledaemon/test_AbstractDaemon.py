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
        self.daemon = LaunchAbstractDaemon(self.pid_file)

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_start(self):
        """Try to start a daemon.
        """
        self.daemon.start()
        time.sleep(1)
        self.assertTrue(Daemon(self.pid_file).status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_stop(self):
        """Try to stop a daemon.
        """
        self.daemon.start()
        time.sleep(1)
        Daemon(self.pid_file).stop()
        time.sleep(1)
        self.assertFalse(Daemon(self.pid_file).status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_restart(self):
        """Try to restart a daemon.
        """
        self.daemon.restart()
        time.sleep(1)
        self.assertTrue(Daemon(self.pid_file).status())

    def test_run(self):
        with self.assertRaises(NotImplementedError):
            Daemon(self.pid_file).run()

    def test_status(self):
        """Try to check status of a daemon.
        """
        self.assertFalse(Daemon(self.pid_file).status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_check_pid_stopped(self):
        """Try to check pid of a stopped daemon.
        """
        self.assertFalse(Daemon(self.pid_file).check_pid())
        self.daemon.start()
        time.sleep(1)
        Daemon(self.pid_file).stop()
        time.sleep(1)
        self.assertFalse(Daemon(self.pid_file).check_pid())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_check_pid_started(self):
        """Try to check pid of a started daemon.
        """
        self.daemon.start()
        time.sleep(1)
        self.assertTrue(Daemon(self.pid_file).check_pid())

    def test_del_pid(self):
        """Try to remove pid file of a daemon.
        """
        with self.assertRaises(FileNotFoundError):
            Daemon(self.pid_file).delpid()

    def tearDown(self):
        """Stop and delete the daemon object.
        """
        if self.daemon and Daemon(self.pid_file).status():
            Daemon(self.pid_file).stop()


if __name__ == '__main__':
    unittest.main()
