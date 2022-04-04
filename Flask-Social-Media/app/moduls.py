from app import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(),
                   primary_key=True)
    username = db.Column(db.String(30),
                         nullable=False,
                         unique=True)
    email_address=db.Column(db.String(50),
                            nullable=False,
                            unique=True)
    password_hash = db.Column(db.String(60),
                              nullable=False)
    born_date = db.Column(db.Date(),
                          nullable=False)
    posts = db.relationship('Post',
                           backref='post_sender',
                           lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'User {self.username}'


class Post(db.Model):
    post_id = db.Column(db.Integer(),
                        primary_key=True)
    content = db.Column(db.String(),
                     nullable=False)
    date = db.Column(db.Date(),
                     nullable=False)
    sender = db.Column(db.Integer(),
                       db.ForeignKey('user.id'))