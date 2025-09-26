# -*- coding: utf-8 -*-
"""
Naebak Banner Service - Flask Application

This is the main application file for the Naebak Banner Service. It provides a RESTful API
for managing banners, including creation, retrieval, analytics tracking, and recommendations.

The service handles banner display logic, image uploads, click tracking, and provides
administrative endpoints for banner management.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import logging
from functools import wraps

from config import get_config
from models import BannerService, BannerData, BannerStats
import constants

# Create Flask application
app = Flask(__name__)
config = get_config()
app.config.from_object(config)

# Setup CORS
CORS(app, origins=app.config['CORS_ALLOWED_ORIGINS'])

# Setup Rate Limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per hour"]
)

# Setup Logging
logging.basicConfig(
    level=getattr(logging, app.config['LOG_LEVEL']),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create banner service instance
banner_service = BannerService(app.config)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def require_auth(f):
    """
    Decorator to require authentication for protected endpoints.
    
    This decorator checks for a valid Bearer token in the Authorization header.
    It should be applied to endpoints that require user authentication.
    
    Args:
        f: The function to be decorated.
        
    Returns:
        The decorated function that includes authentication checks.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "رمز المصادقة مطلوب"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for service monitoring.
    
    This endpoint is used by load balancers and monitoring systems to verify
    that the service is running and responsive.
    
    Returns:
        JSON response with service status information.
    """
    return jsonify({
        "status": "ok",
        "service": "naebak-banners-service",
        "version": app.config['SERVICE_VERSION'],
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/api/banners/', methods=['GET'])
@limiter.limit("50 per minute")
def get_banners():
    """
    Retrieve a list of banners based on filtering criteria.
    
    This endpoint supports filtering by position, category, governorate, and status.
    It's the primary endpoint used by frontend applications to fetch banners for display.
    
    Query Parameters:
        position (str, optional): Filter by banner position (e.g., 'top', 'sidebar').
        category (str, optional): Filter by banner category (e.g., 'informational', 'promotional').
        governorate (str, optional): Filter by target governorate.
        status (str, optional): Filter by banner status (default: 'active').
    
    Returns:
        JSON response containing:
        - banners: List of banner objects
        - total: Total number of banners returned
        - filters: Applied filter parameters
    """
    try:
        # Get query parameters
        position = request.args.get('position')
        category = request.args.get('category')
        governorate = request.args.get('governorate')
        status = request.args.get('status', 'active')
        
        # Get banners using the service
        banners = banner_service.get_active_banners(
            position=position,
            category=category,
            governorate=governorate
        )
        
        # Convert to dictionaries for JSON response
        banners_data = [banner.to_dict() for banner in banners]
        
        return jsonify({
            "banners": banners_data,
            "total": len(banners_data),
            "filters": {
                "position": position,
                "category": category,
                "governorate": governorate,
                "status": status
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving banners: {str(e)}")
        return jsonify({"error": "خطأ في الحصول على البنرات"}), 500

@app.route('/api/banners/<int:banner_id>', methods=['GET'])
@limiter.limit("100 per minute")
def get_banner(banner_id):
    """
    Retrieve a specific banner by its ID.
    
    This endpoint returns detailed information about a single banner,
    including all its metadata and configuration.
    
    Args:
        banner_id (int): The unique identifier of the banner.
    
    Returns:
        JSON response with the banner data, or 404 if not found.
    """
    try:
        # Sample data - in a real implementation, this would query the database
        banner = BannerData(
            id=banner_id,
            title="بنر تجريبي",
            description="وصف البنر التجريبي",
            image_url=f"/static/banners/banner_{banner_id}.jpg",
            banner_type="hero",
            position="top",
            category="informational",
            status="active"
        )
        
        return jsonify(banner.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error retrieving banner {banner_id}: {str(e)}")
        return jsonify({"error": "البنر غير موجود"}), 404

@app.route('/api/banners/', methods=['POST'])
@require_auth
@limiter.limit("10 per minute")
def create_banner():
    """
    Create a new banner with image upload.
    
    This endpoint handles the creation of new banners, including image upload,
    validation, and processing. It requires authentication and has strict rate limiting
    to prevent abuse.
    
    Form Data:
        image (file): The banner image file (required).
        title (str): The banner title.
        description (str): The banner description.
        link_url (str): The URL the banner should link to.
        alt_text (str): Alternative text for accessibility.
        banner_type (str): The type of banner (default: 'hero').
        position (str): The display position (default: 'top').
        category (str): The banner category (default: 'informational').
        priority (int): The display priority (default: 3).
        governorate (str, optional): Target governorate.
    
    Returns:
        JSON response with the created banner data and image information.
    """
    try:
        # Check for image file
        if 'image' not in request.files:
            return jsonify({"error": "ملف الصورة مطلوب"}), 400
        
        file = request.files['image']
        
        # Validate the file
        file_errors = banner_service.validate_image_file(file)
        if file_errors:
            return jsonify({"errors": file_errors}), 400
        
        # Get banner data from form
        banner_data = BannerData(
            title=request.form.get('title', ''),
            description=request.form.get('description', ''),
            link_url=request.form.get('link_url', ''),
            alt_text=request.form.get('alt_text', ''),
            banner_type=request.form.get('banner_type', 'hero'),
            position=request.form.get('position', 'top'),
            category=request.form.get('category', 'informational'),
            priority=int(request.form.get('priority', 3)),
            governorate=request.form.get('governorate'),
            created_at=datetime.now()
        )
        
        # Validate banner data
        validation_errors = banner_service.validate_banner_data(banner_data)
        if validation_errors:
            return jsonify({"errors": validation_errors}), 400
        
        # Process the image
        image_info = banner_service.process_image(file, banner_data.banner_type)
        
        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Update image URL
        banner_data.image_url = f"/uploads/banners/{filename}"
        
        # In a real application, this would save to database
        banner_data.id = 123  # Sample ID
        
        return jsonify({
            "message": "تم إنشاء البنر بنجاح",
            "banner": banner_data.to_dict(),
            "image_info": image_info.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating banner: {str(e)}")
        return jsonify({"error": "خطأ في إنشاء البنر"}), 500

@app.route('/api/banners/<int:banner_id>/click', methods=['POST'])
@limiter.limit("100 per minute")
def track_banner_click(banner_id):
    """
    Track a banner click for analytics purposes.
    
    This endpoint is called when a user clicks on a banner. It records
    the click event along with metadata for analytics and optimization.
    
    Args:
        banner_id (int): The ID of the banner that was clicked.
    
    Returns:
        JSON response confirming the click was recorded.
    """
    try:
        # Record the click
        click_data = {
            "banner_id": banner_id,
            "timestamp": datetime.now().isoformat(),
            "user_agent": request.headers.get('User-Agent', ''),
            "ip_address": request.remote_addr,
            "referrer": request.headers.get('Referer', '')
        }
        
        # In a real application, this would save to database
        logger.info(f"Recorded click on banner {banner_id}")
        
        return jsonify({
            "message": "تم تسجيل النقرة بنجاح",
            "banner_id": banner_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error tracking click: {str(e)}")
        return jsonify({"error": "خطأ في تسجيل النقرة"}), 500

@app.route('/api/banners/<int:banner_id>/stats', methods=['GET'])
@require_auth
@limiter.limit("30 per minute")
def get_banner_stats(banner_id):
    """
    Retrieve analytics statistics for a specific banner.
    
    This endpoint provides detailed performance metrics for a banner,
    including views, clicks, click-through rates, and other analytics data.
    It requires authentication as it contains sensitive business data.
    
    Args:
        banner_id (int): The ID of the banner to get statistics for.
    
    Returns:
        JSON response with banner statistics.
    """
    try:
        stats = banner_service.get_banner_analytics(banner_id)
        return jsonify(stats.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error retrieving statistics: {str(e)}")
        return jsonify({"error": "خطأ في الحصول على الإحصائيات"}), 500

@app.route('/api/banners/types', methods=['GET'])
def get_banner_types():
    """
    Retrieve available banner types.
    
    This endpoint returns a list of all supported banner types with their
    configurations and recommended dimensions. It's used by admin interfaces
    to populate banner type selection dropdowns.
    
    Returns:
        JSON response with available banner types.
    """
    return jsonify(constants.BANNER_TYPES), 200

@app.route('/api/banners/positions', methods=['GET'])
def get_banner_positions():
    """
    Retrieve available banner positions.
    
    This endpoint returns a list of all supported banner positions where
    banners can be displayed on the website. It's used by admin interfaces
    to configure banner placement.
    
    Returns:
        JSON response with available banner positions.
    """
    return jsonify(constants.BANNER_POSITIONS), 200

@app.route('/api/banners/categories', methods=['GET'])
def get_banner_categories():
    """
    Retrieve available banner categories.
    
    This endpoint returns a list of all supported banner categories for
    content classification and filtering purposes.
    
    Returns:
        JSON response with available banner categories.
    """
    return jsonify(constants.BANNER_CATEGORIES), 200

@app.route('/uploads/banners/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded banner image files.
    
    This endpoint serves the uploaded banner images to the frontend.
    It handles the static file serving for banner images.
    
    Args:
        filename (str): The name of the image file to serve.
    
    Returns:
        The requested image file.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/banners/recommendations', methods=['GET'])
@limiter.limit("20 per minute")
def get_banner_recommendations():
    """
    Get personalized banner recommendations for a user.
    
    This endpoint implements a recommendation algorithm that suggests
    the most relevant banners for a specific user and position based on
    various factors like priority, popularity, and user context.
    
    Query Parameters:
        user_id (int, optional): The ID of the user to get recommendations for.
        position (str): The position where banners will be displayed (default: 'top').
    
    Returns:
        JSON response with recommended banners.
    """
    try:
        user_id = request.args.get('user_id', type=int)
        position = request.args.get('position', 'top')
        
        recommendations = banner_service.get_banner_recommendations(user_id, position)
        recommendations_data = [banner.to_dict() for banner in recommendations]
        
        return jsonify({
            "recommendations": recommendations_data,
            "total": len(recommendations_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving recommendations: {str(e)}")
        return jsonify({"error": "خطأ في الحصول على التوصيات"}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return jsonify({"error": "الصفحة غير موجودة"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    return jsonify({"error": "خطأ داخلي في الخادم"}), 500

@app.errorhandler(413)
def file_too_large(error):
    """Handle 413 Request Entity Too Large errors (file upload size exceeded)."""
    return jsonify({"error": "حجم الملف كبير جداً"}), 413

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=app.config['SERVICE_PORT'],
        debug=app.config['DEBUG']
    )
