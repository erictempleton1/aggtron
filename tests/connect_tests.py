import os, sys
top_dir = os.path.join(os.path.dirname(__file__), '../../')
sys.path.append(top_dir)

import aggtron
import unittest
import tempfile


class ConnectTestCase(unittest.TestCase):


    def setUp(self):
        self.db_fd, aggtron.app.config['MONGODB_SETTINGS'] = {'DB': 'testing'}
        aggtron.app.config['TESTING'] = True
        self.app = aggtron.app.test_client()
        aggtron.init_db()

    def tearDown(self):
        os.close(self.db_fb)
        os.unlink(aggtron.app.config['MONGODB_SETTINGS'])


if __name__ == '__main__':
    unittest.main()