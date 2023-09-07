from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

# called to load a user given the ID
@login.user_loader
def load_user(id): # id is a string, so the databases tha uses numeric ids need to convert the  string to integer
      return User.query.get(int(id))


#Model Class
#class inherits from db Model,base class for all models from FLAsk SQLalchemy

#UserMixin is a Mixin class that include the generic implementattions that are appropriate for most user model classes
  
followers = db.Table('followers',db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
            db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))
           )
class User (UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

  # Method tells Python how to print objects of this class
    def __repr__(self):
        #return super().__repr__()

        return '<User {}>'.format(self.username)

    def set_password(self, password):
          self.password_hash = generate_password_hash(password)


    def check_password(self, password):
          return check_password_hash(self.password_hash, password)

    #avatars on the users profile section
    #returns the url of the user's avatr image,scaled to the requested size in pixels
    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)

    # following methods

    def follow(self,user):
        if not self.is_following(user):
            self.follow.append(user)

    def unfollow(self,user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
      

    followed = db.relationship(
        'User',secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers',lazy='dynamic'),lazy='dynamic'

    )
# Fetches posts belonging to the followers of the user ,in descending order
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

 
                
            
        
##join()-- invoked on the post table(instructs the db to create a temporary table that combines data from posts and followers table )
# first arg is the followers table
# second is the join condition (followed_id of the followers table must be equal to the users_is  of the post table)
#filter_by()..returns for a particular user
#order_by().responsible for sorting in descending order
class Post (db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.String,index=True,default=datetime.utcnow)
     #Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):

        return '<Post {}>'.format(self.body)

