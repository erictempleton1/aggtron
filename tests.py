import unittest
from flask import Flask, current_app
from app import app, db, flask_bcrypt
from models import Users
from flask.ext.login import login_user, current_user
from flask.ext.testing import TestCase



class AggtronTestCase(unittest.TestCase):


    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron_test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_basic_load(self):
        """ test basic page loads """
        rv = self.app.get('/')
        assert 'Aggtron' in rv.data

        rv = self.app.get('/login')
        assert 'Login' in rv.data

        rv = self.app.get('/register')
        assert 'Register' in rv.data

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password
            ), follow_redirects=True)


if __name__ == '__main__':
    unittest.main()         