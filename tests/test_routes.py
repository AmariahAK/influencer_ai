import unittest
from app import create_app
from models.database import db, Influencer

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_add_influencer(self):
        response = self.client.post('/api/influencer', json={
            'name': 'testuser',
            'followers': 6000,
            'following_influencers': 10,
            'engagement_rate': 0.05
        })
        self.assertEqual(response.status_code, 201)
    
    def test_get_influencers(self):
        response = self.client.get('/api/influencers')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
