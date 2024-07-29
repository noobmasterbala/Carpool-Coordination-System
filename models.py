from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Group(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), nullable=False)
    members = db.relationship('User', secondary='group_members')
    schedule = db.Column(db.String(100), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)

class Ride(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = db.Column(UUID(as_uuid=True), db.ForeignKey('group.id'))
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(10), nullable=False)
    participants = db.relationship('User', secondary='ride_participants')

group_members = db.Table('group_members',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
    db.Column('group_id', UUID(as_uuid=True), db.ForeignKey('group.id'))
)

ride_participants = db.Table('ride_participants',
    db.Column('user_id', UUID(as_uuid=True), db.ForeignKey('user.id')),
    db.Column('ride_id', UUID(as_uuid=True), db.ForeignKey('ride.id'))
)
