import unittest
from app import app, db
from flask.ext.login import login_user
from flask.ext.testing import TestCase



class AggtronTestCase(unittest.TestCase):


    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron_test.db'
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_basic(self):
        """ test basic page loads """
        rv = self.client.get('/')
        assert 'Aggtron' in rv.data

        rv = self.client.get('/login')
        assert 'Login' in rv.data

        rv = self.client.get('/register')
        assert 'Register' in rv.data

        rv = self.client.post('/login', data=dict(email='eric@eric.com', password='eric'))
        print rv.data
        assert 'eric@eric.com' in rv.data  


if __name__ == '__main__':
    unittest.main()         