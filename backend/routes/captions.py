from flask import Blueprint, request, jsonify
from database import get_database
from datetime import datetime
from bson import ObjectId
from model import generate_caption

try:
    from cloud import upload_image
except Exception:
    upload_image = None

captions_bp = Blueprint('captions', __name__)


@captions_bp.route('/generate-caption', methods=['POST'])
def generate_caption_api():
    """
    Multipart form-data:
      - image: file (required)
      - sentiment: string (optional)
      - length: string|number (optional)
      - user_id: string (optional)

    Returns:
      { caption, image_url?, caption_id? }
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'image file is required (field name: image)'}), 400

        image_file = request.files['image']
        if not image_file or image_file.filename == '':
            return jsonify({'error': 'image file is required'}), 400

        sentiment = (request.form.get('sentiment') or 'neutral').strip()
        length = (request.form.get('length') or 'short').strip()
        user_id = request.form.get('user_id')

        # Generate caption (currently stubbed rule-based in model.py)
        caption = generate_caption(image_file.filename, sentiment=sentiment.lower(), length=str(length).lower())

        # Optional Cloudinary upload if configured
        image_url = None
        if upload_image is not None:
            image_url = upload_image(image_file)

        # Save to MongoDB (if available)
        caption_id = None
        db = get_database()
        if db is not None:
            captions = db['captions']
            doc = {
                'user_id': user_id,
                'image_url': image_url,
                'caption': caption,
                'sentiment': sentiment,
                'length': length,
                'created_at': datetime.utcnow()
            }
            result = captions.insert_one(doc)
            caption_id = str(result.inserted_id)

        return jsonify({
            'caption': caption,
            'image_url': image_url,
            'caption_id': caption_id
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@captions_bp.route('/captions', methods=['POST'])
def save_caption():
    try:
        db = get_database()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        captions = db['captions']
        data = request.json
        
        caption_doc = {
            'user_id': data.get('user_id'),
            'image_url': data.get('image_url'),
            'caption': data.get('caption'),
            'sentiment': data.get('sentiment'),
            'length': data.get('length'),
            'created_at': datetime.utcnow()
        }
        
        result = captions.insert_one(caption_doc)
        
        return jsonify({
            'message': 'Caption saved successfully',
            'caption_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@captions_bp.route('/captions/<user_id>', methods=['GET'])
def get_user_captions(user_id):
    try:
        db = get_database()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        captions = db['captions']
        user_captions = list(captions.find({'user_id': user_id}))
        
        # Convert ObjectId to string
        for caption in user_captions:
            caption['_id'] = str(caption['_id'])
        
        return jsonify({'captions': user_captions}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500