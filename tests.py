import models
import unittest
from app import app, db
from flask.ext.login import login_user



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

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
            ), follow_redirects=True)

    def test_login(self):
        new_user = models.Users(email='eric1@eric1.com', password='eric1')
        db.session.add(new_user)
        db.session.commit()

        rv = self.login('eric1@eric1.com', 'eric1')
        print rv.data
        assert 'Hello' in rv.data        



if __name__ == '__main__':
    unittest.main()         