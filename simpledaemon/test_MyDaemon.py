# -*- coding: utf-8 -*-

import sys
import time
import unittest
import logging
import MyDaemon


class TestMyDaemon(unittest.TestCase):

    def setUp(self):
        self.daemon = MyDaemon.MyDaemon('pidfile')

    def test_do_something(self):
        self.assertIsNone(MyDaemon.do_something())

    def test_usage_help(self):
        self.assertIsNone(MyDaemon.usage_help())

    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_run(self):
        self.daemon.run()
        self.assertTrue(self.daemon.status())

    def tearDown(self):
        if self.daemon and self.daemon.status():
            time.sleep(1)
            self.daemon.stop()


if __name__ == '__main__':
    unittest.main()
