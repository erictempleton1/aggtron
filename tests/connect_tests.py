import os, sys
top_dir = os.path.join(os.path.dirname(__file__), '../../')
sys.path.append(top_dir)

import aggtron
from aggtron import db, app
from flask import Flask
import unittest
import tempfile
from aggtron.models import Users, Project
from flask.ext.login import login_user, current_user


class ConnectTestCase(unittest.TestCase):


    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron_test.db'
        self.app = app.test_client()
        db.create_all()

    def test_create_user(self):
        user = Users(email='eric1@eric1.com', password='eric')
        db.session.add(user)
        db.session.commit()

        u = Users.query.filter_by(email='eric1@eric1.com').first()

        print u.email
        self.assertEqual('eric1@eric1.com', u.email)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()