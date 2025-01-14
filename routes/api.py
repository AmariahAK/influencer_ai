from flask import Blueprint, request, jsonify
from models.database import db, Influencer, save_influencer, get_influencer_by_name
from models.influencer_model import is_influencer, process_commenters
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/influencer', methods=['POST'])
def add_influencer():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Invalid data provided"}), 400
    
    # Check if profile qualifies as an influencer
    if is_influencer(
        followers=data.get('followers', 0),
        following_influencers=data.get('following_influencers', 0),
        engagement_rate=data.get('engagement_rate', 0)
    ):
        influencer = save_influencer(data)
        return jsonify({
            "message": "Influencer saved successfully",
            "id": influencer.id
        }), 201
    return jsonify({"message": "Profile does not qualify as an influencer"}), 200

@api_bp.route('/influencer/<int:id>', methods=['GET'])
def get_influencer(id):
    influencer = Influencer.query.get_or_404(id)
    return jsonify({
        "id": influencer.id,
        "name": influencer.name,
        "profile_pic": influencer.profile_pic,
        "tags": influencer.tags,
        "bio": influencer.bio,
        "contact": influencer.contact,
        "followers": influencer.followers,
        "social_links": {
            "instagram": influencer.instagram_link,
            "tiktok": influencer.tiktok_link,
            "facebook": influencer.facebook_link,
            "youtube": influencer.youtube_link
        }
    })

@api_bp.route('/influencers', methods=['GET'])
def get_influencers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    influencers = Influencer.query.paginate(page=page, per_page=per_page)
    return jsonify({
        "total": influencers.total,
        "pages": influencers.pages,
        "current_page": influencers.page,
        "influencers": [{
            "id": inf.id,
            "name": inf.name,
            "followers": inf.followers,
            "tags": inf.tags
        } for inf in influencers.items]
    })

@api_bp.route('/process-post', methods=['POST'])
def process_post():
    data = request.json
    if not data or 'post_id' not in data or 'commenters' not in data:
        return jsonify({"error": "Invalid post data"}), 400
    
    process_commenters(data['post_id'], data['commenters'])
    return jsonify({"message": "Post processed successfully"}), 200

@api_bp.route('/influencer/search', methods=['GET'])
def search_influencers():
    query = request.args.get('q', '')
    tags = request.args.get('tags', '')
    
    influencers = Influencer.query
    
    if query:
        influencers = influencers.filter(Influencer.name.ilike(f'%{query}%'))
    if tags:
        tag_list = tags.split(',')
        for tag in tag_list:
            influencers = influencers.filter(Influencer.tags.ilike(f'%{tag.strip()}%'))
    
    return jsonify({
        "results": [{
            "id": inf.id,
            "name": inf.name,
            "followers": inf.followers,
            "tags": inf.tags
        } for inf in influencers.all()]
    })
