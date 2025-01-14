import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urlparse

class SocialMediaScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def extract_social_links(self, bio_text):
        social_links = {
            'instagram': None,
            'youtube': None,
            'tiktok': None,
            'facebook': None
        }
        
        for line in bio_text.split('\n'):
            if 'instagram.com' in line:
                social_links['instagram'] = line.strip()
            elif 'youtube.com' in line:
                social_links['youtube'] = line.strip()
            elif 'tiktok.com' in line:
                social_links['tiktok'] = line.strip()
            elif 'facebook.com' in line:
                social_links['facebook'] = line.strip()
                
        return social_links

def scrape_instagram_profile(username):
    scraper = SocialMediaScraper()
    url = f"https://www.instagram.com/{username}/"
    
    try:
        response = requests.get(url, headers=scraper.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract meta tags
            meta_tags = soup.find_all('meta', property='og:description')
            description = meta_tags[0]['content'] if meta_tags else ''
            
            # Parse follower count from description
            followers = 0
            if 'Followers' in description:
                followers_text = description.split('Followers')[0].strip().split()[-1]
                followers = parse_follower_count(followers_text)
            
            # Extract profile image
            profile_pic = soup.find('meta', property='og:image')
            profile_pic_url = profile_pic['content'] if profile_pic else ''
            
            # Extract bio and tags
            bio = soup.find('meta', property='og:description')
            bio_text = bio['content'] if bio else ''
            tags = extract_tags(bio_text)
            
            # Extract contact information
            contact = extract_contact_info(bio_text)
            
            # Get other social media links
            social_links = scraper.extract_social_links(bio_text)
            
            return {
                "name": username,
                "followers": followers,
                "bio": bio_text,
                "profile_pic": profile_pic_url,
                "tags": tags,
                "contact": contact,
                "social_links": social_links
            }
    except Exception as e:
        print(f"Error scraping profile {username}: {str(e)}")
        return None
    
    return None

def parse_follower_count(followers_text):
    try:
        if 'K' in followers_text:
            return int(float(followers_text.replace('K', '')) * 1000)
        elif 'M' in followers_text:
            return int(float(followers_text.replace('M', '')) * 1000000)
        return int(followers_text.replace(',', ''))
    except:
        return 0

def extract_tags(text):
    hashtags = [word for word in text.split() if word.startswith('#')]
    return ', '.join([tag.strip('#') for tag in hashtags])

def extract_contact_info(text):
    import re
    # Match email addresses
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email:
        return email.group()
    
    # Match phone numbers (various formats)
    phone = re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
    if phone:
        return phone.group()
    
    return None

def validate_profile_data(profile_data):
    required_fields = ['name', 'followers', 'bio', 'profile_pic']
    return all(field in profile_data for field in required_fields)
