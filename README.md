# Influencer AI Detection System

An AI-powered system that automatically detects and tracks social media influencers across Africa using machine learning and data scraping.

## Features

- AI-powered influencer detection using TensorFlow
- Multi-platform social media scraping (Instagram, TikTok, YouTube, Facebook)
- Automated influencer classification based on followers and engagement
- RESTful API endpoints for data access
- SQLite database for influencer storage
- Modern web interface with responsive design

## Tech Stack

- Python 3.8+
- Flask
- TensorFlow
- SQLAlchemy
- BeautifulSoup4
- React/TypeScript (Frontend - Coming Soon)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/influencer_ai.git
cd influencer_ai

Copy

Apply

README.md
Create and activate virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Copy

Execute

Install dependencies:
pip install -r requirements.txt

Copy

Execute

Set up environment variables:
cp .env.example .env
# Edit .env with your configuration

Copy

Execute

Usage
Start the Flask server:
python app.py

Copy

Execute

Access the API at http://localhost:5000/api
API Endpoints
POST /api/influencer - Add new influencer
GET /api/influencer/<id> - Get influencer details
GET /api/influencers - List all influencers
GET /api/influencer/search - Search influencers
POST /api/process-post - Process social media post
Project Structure
influencer_ai/
├── app.py
├── models/
│   ├── database.py
│   └── influencer_model.py
├── routes/
│   ├── api.py
│   ├── scrape.py
│   └── utils.py
├── static/
│   └── style.css
├── tests/
│   └── test_routes.py
└── requirements.txt

Copy

Apply

AI Model
The system uses a TensorFlow-based model to classify influencers based on:

Follower count (minimum 5000)
Engagement rate
Influencer connections
Content metrics
Testing
Run the test suite:

python -m pytest

Copy

Execute

Contributing
Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
Your Name - @AmariahAK Project Link: https://github.com/AmariahAK/influencer_ai