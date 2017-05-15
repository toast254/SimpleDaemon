# -*- coding: utf-8 -*-

import sys
import time
import unittest
import MyDaemon


class TestMyDaemon(unittest.TestCase):
    """Test MyDaemon class.
    """

    def setUp(self):
        """Create a daemon object.
        """
        self.daemon = MyDaemon.MyDaemon('pidfile')

    def test_do_something(self):
        """Try to execute 'do_something' method from the daemon.
        """
        self.assertIsNone(MyDaemon.do_something())

    def test_usage_help(self):
        """Try to print usage help from the daemon.
        """
        self.assertIsNone(MyDaemon.usage_help())

    @unittest.skip('Too long and equivalent to "test_do_something" test, skipping it...')
    @unittest.skipIf(sys.platform.startswith("win"), "not available on Windows")
    def test_run(self):
        """Try to execute 'run' method from the daemon.
        """
        self.daemon.run()
        self.assertTrue(self.daemon.status())

    def tearDown(self):
        """Stop and remove the daemon object.
        """
        if self.daemon and self.daemon.status():
            time.sleep(1)
            self.daemon.stop()


if __name__ == '__main__':
    unittest.main()
