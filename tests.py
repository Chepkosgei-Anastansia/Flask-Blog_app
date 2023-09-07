from app import app,db
import unittest
from app.models import Post, User
import datetime
from _datetime import timedelta

class UserModelCase(unittest.TestCase):
    #setup() and tearDown() are special methods that the unit testing framework executes before and after each test respectively
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all() # creates all database tables
        # prevents the unit tests from using the regular database used for development
        # uses in-memory SQLite database tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='Anastansia')
        u.set_password('herod')
        self.assertFalse(u.check_password('jesus'))
        self.assertTrue(u.check_password('herod'))

    def test_avatar(self):
        u = User(username='Angela',email='angela@gmail.com')
        self.assertEqual(u.avatar(128),('https:// www.gravatar.com/avatar/'
         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))
    

    def test_follow(self):
        u1 = User(username='Anastansia',email='anastansia@gmail.com')
        u2 = User(username='Angela',email='angela@gmail.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(),[])
        self.assertEqual(u1.followers.all(),[])


        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(),1)
        self.assertEqual(u1.followed.first().username,'Angela')
        self.assertEqual(u2.followers.count(),1)
        self.assertEqual(u2.followers.first().username,'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(),0)
        self.assertEqual(u2.followers.count(),0)
           
        
        def test_follow_posts(self):
                # create four users
            u1 = User(username='ann', email='ann@example.com')
            u2 = User(username='jesse', email='jesse@example.com')
            u3 = User(username='eliud', email='eliud@example.com')
            u4 = User(username='agatha', email='agatha@example.com')
            db.session.add_all([u1, u2, u3, u4])

            # create four posts
            now = datetime.utcnow()
            p1 = Post(body="post from ann", author=u1,
                    timestamp=now + timedelta(seconds=1))
            p2 = Post(body="post from jesse", author=u2,
                    timestamp=now + timedelta(seconds=4))
            p3 = Post(body="post from eliud", author=u3,
                    timestamp=now + timedelta(seconds=3))
            p4 = Post(body="post from agatha", author=u4,
                    timestamp=now + timedelta(seconds=2))
            db.session.add_all([p1, p2, p3, p4])
            db.session.commit()

            # setup the followers
            u1.follow(u2)  # ann follows jesse
            u1.follow(u4)  # ann follows agatha
            u2.follow(u3)  # jesse follows eliud
            u3.follow(u4)  # eliud follows agatha
            db.session.commit()

            # check the followed posts of each user
            f1 = u1.followed_posts().all()
            f2 = u2.followed_posts().all()
            f3 = u3.followed_posts().all()
            f4 = u4.followed_posts().all()
            self.assertEqual(f1, [p2, p4, p1])
            self.assertEqual(f2, [p2, p3])
            self.assertEqual(f3, [p3, p4])
            self.assertEqual(f4, [p4])

        if __name__ == '__main__':
            unittest.main(verbosity=2)
