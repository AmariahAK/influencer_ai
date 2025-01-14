from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Influencer(db.Model):
    __tablename__ = 'influencers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(200))
    tags = db.Column(db.String(300))
    bio = db.Column(db.String(500))
    contact = db.Column(db.String(50))
    followers = db.Column(db.Integer)
    
    # Social media links
    instagram_link = db.Column(db.String(200))
    tiktok_link = db.Column(db.String(200))
    facebook_link = db.Column(db.String(200))
    youtube_link = db.Column(db.String(200))
    
    # Additional metrics
    engagement_rate = db.Column(db.Float)
    following_influencers = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Posts relationship
    posts = db.relationship('Post', backref='influencer', lazy=True)

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'))
    post_id = db.Column(db.String(100))
    commenters = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def get_influencer_by_name(name):
    return Influencer.query.filter_by(name=name).first()

def save_influencer(data):
    influencer = get_influencer_by_name(data['name'])
    
    if not influencer:
        influencer = Influencer()
    
    # Update influencer data
    for key, value in data.items():
        if hasattr(influencer, key):
            setattr(influencer, key, value)
    
    db.session.add(influencer)
    db.session.commit()
    return influencer

def delete_inactive_influencers(follower_threshold=5000):
    Influencer.query.filter(Influencer.followers < follower_threshold).delete()
    db.session.commit()
