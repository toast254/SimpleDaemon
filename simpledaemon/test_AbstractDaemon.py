# -*- coding: utf-8 -*-

import sys
import time
import unittest
from AbstractDaemon import Daemon


class TestAbstractDaemon(unittest.TestCase):

    def setUp(self):
        self.daemon = Daemon('pidfile')

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_start(self):
        self.daemon.start()
        self.assertTrue(self.daemon.status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_stop(self):
        self.daemon.start()
        time.sleep(1)
        self.daemon.stop()
        self.assertFalse(self.daemon.status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_restart(self):
        self.daemon.restart()
        self.assertTrue(self.daemon.status())

    def test_run(self):
        with self.assertRaises(NotImplementedError):
            self.daemon.run()

    def test_status(self):
        self.assertFalse(self.daemon.status())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_check_pid_stopped(self):
        self.assertFalse(self.daemon.check_pid())
        self.daemon.start()
        time.sleep(1)
        self.daemon.stop()
        self.assertFalse(self.daemon.check_pid())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_check_pid_started(self):
        self.daemon.start()
        self.assertTrue(self.daemon.check_pid())

    def test_del_pid(self):
        with self.assertRaises(FileNotFoundError):
            self.daemon.delpid()

    def tearDown(self):
        if self.daemon and self.daemon.status():
            time.sleep(1)
            self.daemon.stop()


if __name__ == '__main__':
    unittest.main()
