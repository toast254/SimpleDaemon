# -*- coding: utf-8 -*-

import sys
import time
import unittest
from AbstractDaemon import Daemon


class TestAbstractDaemon(unittest.TestCase):
    """Test AbstractDaemon class.
    """

    def setUp(self):
        """Create a new Daemon obect.
        """
        self.daemon = Daemon('/tmp/test.pid')

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_start(self):
        """Try to start a daemon.
        """
        with self.assertRaises(SystemExit) as cm:
            self.daemon.start()
            print(cm)
        self.assertTrue(self.daemon.status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_stop(self):
        """Try to stop a daemon.
        """
        with self.assertRaises(SystemExit) as cm:
            self.daemon.start()
            print(cm)
        time.sleep(1)
        self.daemon.stop()
        self.assertFalse(self.daemon.status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_restart(self):
        """Try to restart a daemon.
        """
        with self.assertRaises(SystemExit) as cm:
            self.daemon.restart()
            print(cm)
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
        with self.assertRaises(SystemExit) as cm:
            self.daemon.start()
            print(cm)
        time.sleep(1)
        self.daemon.stop()
        self.assertFalse(self.daemon.check_pid())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_check_pid_started(self):
        """Try to check pid of a started daemon.
        """
        with self.assertRaises(SystemExit) as cm:
            self.daemon.start()
            print(cm)
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
            time.sleep(1)
            self.daemon.stop()


if __name__ == '__main__':
    unittest.main()
