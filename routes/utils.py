from functools import wraps
import jwt
from flask import request, jsonify
import re
from datetime import datetime

def validate_social_links(links):
    patterns = {
        'instagram': r'^https?:\/\/(www\.)?instagram\.com\/[\w\.-]+\/?$',
        'tiktok': r'^https?:\/\/(www\.)?tiktok\.com\/@[\w\.-]+\/?$',
        'youtube': r'^https?:\/\/(www\.)?youtube\.com\/(c\/|channel\/)?[\w\.-]+\/?$',
        'facebook': r'^https?:\/\/(www\.)?facebook\.com\/[\w\.-]+\/?$'
    }
    
    valid_links = {}
    for platform, link in links.items():
        if link and re.match(patterns.get(platform, ''), link):
            valid_links[platform] = link
    return valid_links

def format_follower_count(count):
    if count >= 1000000:
        return f"{count/1000000:.1f}M"
    elif count >= 1000:
        return f"{count/1000:.1f}K"
    return str(count)

def calculate_engagement_rate(likes, comments, followers):
    if followers == 0:
        return 0
    return ((likes + comments) / followers) * 100
