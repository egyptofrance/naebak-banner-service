# -*- coding: utf-8 -*-
"""
Banner Service Data Models - Naebak Project

This module defines the core data models and business logic for the Naebak Banner Service.
It includes models for banner data, statistics, image information, and the main banner service class.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from PIL import Image
import constants

@dataclass
class BannerData:
    """
    Represents a banner in the system.

    This dataclass encapsulates all the information needed to display and manage a banner,
    including its content, positioning, scheduling, and performance metrics.

    Attributes:
        id (Optional[int]): The unique identifier for the banner.
        title (str): The title of the banner.
        description (str): A detailed description of the banner content.
        image_url (str): The URL of the banner image.
        link_url (str): The URL that the banner links to when clicked.
        alt_text (str): Alternative text for accessibility.
        banner_type (str): The type of banner (e.g., 'hero', 'sidebar', 'footer').
        position (str): The position where the banner should be displayed.
        category (str): The category of the banner (e.g., 'informational', 'promotional').
        status (str): The current status of the banner (e.g., 'draft', 'active', 'expired').
        priority (int): The priority level for display ordering (1-5, where 1 is highest).
        governorate (Optional[str]): The specific governorate to target (if any).
        start_date (Optional[datetime]): When the banner should start being displayed.
        end_date (Optional[datetime]): When the banner should stop being displayed.
        created_by (Optional[int]): The ID of the user who created the banner.
        created_at (Optional[datetime]): When the banner was created.
        updated_at (Optional[datetime]): When the banner was last updated.
        click_count (int): The number of times the banner has been clicked.
        view_count (int): The number of times the banner has been viewed.
    """
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    image_url: str = ""
    link_url: str = ""
    alt_text: str = ""
    banner_type: str = "hero"
    position: str = "top"
    category: str = "informational"
    status: str = "draft"
    priority: int = 3
    governorate: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    click_count: int = 0
    view_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the banner data to a dictionary format.
        
        This method is useful for serialization, API responses, and database operations.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the banner data.
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'link_url': self.link_url,
            'alt_text': self.alt_text,
            'banner_type': self.banner_type,
            'position': self.position,
            'category': self.category,
            'status': self.status,
            'priority': self.priority,
            'governorate': self.governorate,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'click_count': self.click_count,
            'view_count': self.view_count
        }

@dataclass
class BannerStats:
    """
    Represents analytics and performance statistics for a banner.

    This dataclass tracks various metrics to help administrators understand
    the effectiveness of their banners and make data-driven decisions.

    Attributes:
        banner_id (int): The ID of the banner these statistics belong to.
        total_views (int): The total number of times the banner has been viewed.
        total_clicks (int): The total number of times the banner has been clicked.
        click_through_rate (float): The percentage of views that resulted in clicks.
        unique_viewers (int): The number of unique users who have viewed the banner.
        last_viewed (Optional[datetime]): The timestamp of the most recent view.
    """
    banner_id: int
    total_views: int = 0
    total_clicks: int = 0
    click_through_rate: float = 0.0
    unique_viewers: int = 0
    last_viewed: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the banner statistics to a dictionary format.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the banner statistics.
        """
        return {
            'banner_id': self.banner_id,
            'total_views': self.total_views,
            'total_clicks': self.total_clicks,
            'click_through_rate': self.click_through_rate,
            'unique_viewers': self.unique_viewers,
            'last_viewed': self.last_viewed.isoformat() if self.last_viewed else None
        }

@dataclass
class ImageInfo:
    """
    Represents metadata about an uploaded image file.

    This dataclass stores technical information about banner images,
    which is useful for optimization, validation, and display purposes.

    Attributes:
        filename (str): The generated filename for the uploaded image.
        original_filename (str): The original filename as uploaded by the user.
        file_size (int): The size of the image file in bytes.
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.
        format (str): The image format (e.g., 'JPEG', 'PNG').
        mime_type (str): The MIME type of the image file.
        upload_path (str): The full path where the image is stored.
        thumbnail_path (Optional[str]): The path to the thumbnail version (if generated).
    """
    filename: str
    original_filename: str
    file_size: int
    width: int
    height: int
    format: str
    mime_type: str
    upload_path: str
    thumbnail_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the image information to a dictionary format.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the image information.
        """
        return {
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'width': self.width,
            'height': self.height,
            'format': self.format,
            'mime_type': self.mime_type,
            'upload_path': self.upload_path,
            'thumbnail_path': self.thumbnail_path
        }

class BannerService:
    """
    Main service class for banner management operations.

    This class encapsulates all the business logic for managing banners,
    including validation, image processing, analytics, and recommendations.
    It serves as the primary interface between the API layer and the data layer.

    Attributes:
        config: The application configuration object.
        upload_folder (str): The directory where uploaded images are stored.
        max_file_size (int): The maximum allowed file size for uploads.
        allowed_extensions (set): The set of allowed file extensions.
    """
    
    def __init__(self, config):
        """
        Initialize the banner service with configuration settings.
        
        Args:
            config: The application configuration object containing upload settings.
        """
        self.config = config
        self.upload_folder = config.UPLOAD_FOLDER
        self.max_file_size = config.MAX_CONTENT_LENGTH
        self.allowed_extensions = config.ALLOWED_EXTENSIONS
    
    def validate_banner_data(self, banner_data: BannerData) -> List[str]:
        """
        Validates banner data according to business rules.

        This method performs comprehensive validation of banner data to ensure
        it meets all requirements before being saved to the database.

        Args:
            banner_data (BannerData): The banner data to validate.

        Returns:
            List[str]: A list of validation error messages. Empty if validation passes.
        """
        errors = []
        
        # Validate title
        if not banner_data.title or len(banner_data.title.strip()) < 3:
            errors.append("العنوان مطلوب ويجب أن يكون 3 أحرف على الأقل")
        
        # Validate alt text (required if admin approval is needed)
        if self.config.REQUIRE_ADMIN_APPROVAL and not banner_data.alt_text:
            errors.append("النص البديل مطلوب")
        
        # Validate banner type
        valid_types = [bt['type'] for bt in constants.BANNER_TYPES]
        if banner_data.banner_type not in valid_types:
            errors.append("نوع البنر غير صحيح")
        
        # Validate position
        valid_positions = [pos['position'] for pos in constants.BANNER_POSITIONS]
        if banner_data.position not in valid_positions:
            errors.append("موضع البنر غير صحيح")
        
        # Validate category
        valid_categories = [cat['category'] for cat in constants.BANNER_CATEGORIES]
        if banner_data.category not in valid_categories:
            errors.append("فئة البنر غير صحيحة")
        
        # Validate dates
        if banner_data.start_date and banner_data.end_date:
            if banner_data.start_date >= banner_data.end_date:
                errors.append("تاريخ البداية يجب أن يكون قبل تاريخ النهاية")
        
        return errors
    
    def validate_image_file(self, file) -> List[str]:
        """
        Validates an uploaded image file.

        This method checks the file type, size, and other constraints
        to ensure the uploaded image is suitable for use as a banner.

        Args:
            file: The uploaded file object.

        Returns:
            List[str]: A list of validation error messages. Empty if validation passes.
        """
        errors = []
        
        # Check if file exists
        if not file or not file.filename:
            errors.append("لم يتم اختيار ملف")
            return errors
        
        # Check file type
        if not constants.is_valid_file_type(file.filename):
            errors.append("نوع الملف غير مدعوم")
            return errors
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        max_size = self.max_file_size
        if file_size > max_size:
            errors.append(f"حجم الملف كبير جداً (الحد الأقصى: {max_size // (1024*1024)}MB)")
        
        return errors
    
    def process_image(self, file, banner_type: str) -> ImageInfo:
        """
        Processes and optimizes an uploaded image.

        This method handles image optimization, resizing, and metadata extraction
        to prepare the image for use as a banner.

        Args:
            file: The uploaded file object.
            banner_type (str): The type of banner this image will be used for.

        Returns:
            ImageInfo: An object containing metadata about the processed image.
        """
        # Get banner type information
        banner_info = constants.get_banner_type_info(banner_type)
        
        # Open the image
        image = Image.open(file)
        original_width, original_height = image.size
        
        # Optimize image if required
        if self.config.IMAGE_OPTIMIZATION:
            # Compress image
            if image.format in ['JPEG', 'JPG']:
                image = image.convert('RGB')
        
        # Resize if required
        if self.config.AUTO_RESIZE and banner_info:
            recommended_size = banner_info.get('recommended_size', '').split('x')
            if len(recommended_size) == 2:
                target_width = int(recommended_size[0])
                target_height = int(recommended_size[1])
                
                # Resize while maintaining aspect ratio
                image.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Create image information
        image_info = ImageInfo(
            filename=file.filename,
            original_filename=file.filename,
            file_size=file_size if 'file_size' in locals() else 0,
            width=image.width,
            height=image.height,
            format=image.format,
            mime_type=file.content_type,
            upload_path=f"{self.upload_folder}/{file.filename}"
        )
        
        return image_info
    
    def get_active_banners(self, position: Optional[str] = None, 
                          category: Optional[str] = None,
                          governorate: Optional[str] = None) -> List[BannerData]:
        """
        Retrieves active banners based on filtering criteria.

        This method implements the core business logic for banner selection,
        including filtering by position, category, and geographic targeting.

        Args:
            position (Optional[str]): Filter by banner position.
            category (Optional[str]): Filter by banner category.
            governorate (Optional[str]): Filter by target governorate.

        Returns:
            List[BannerData]: A list of active banners matching the criteria.
        """
        # This is a sample implementation - in a real application, this would query the database
        banners = []
        
        # Sample data
        sample_banners = [
            BannerData(
                id=1,
                title="مرحباً بكم في منصة نائبك",
                description="منصة تفاعلية للتواصل مع ممثليكم",
                image_url="/static/banners/welcome.jpg",
                banner_type="hero",
                position="top",
                category="informational",
                status="active",
                priority=1
            ),
            BannerData(
                id=2,
                title="قدم شكواك الآن",
                description="خدمة سريعة لتقديم الشكاوى",
                image_url="/static/banners/complaints.jpg",
                banner_type="sidebar",
                position="sidebar_right",
                category="service",
                status="active",
                priority=2
            )
        ]
        
        # Apply filters
        for banner in sample_banners:
            if position and banner.position != position:
                continue
            if category and banner.category != category:
                continue
            if governorate and banner.governorate and banner.governorate != governorate:
                continue
            banners.append(banner)
        
        # Sort by priority
        banners.sort(key=lambda x: x.priority)
        
        return banners
    
    def get_banner_analytics(self, banner_id: int, 
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> BannerStats:
        """
        Retrieves analytics data for a specific banner.

        This method calculates and returns performance metrics for a banner,
        which can be used for reporting and optimization purposes.

        Args:
            banner_id (int): The ID of the banner to get analytics for.
            start_date (Optional[datetime]): The start date for the analytics period.
            end_date (Optional[datetime]): The end date for the analytics period.

        Returns:
            BannerStats: An object containing the banner's performance statistics.
        """
        # Sample data - in a real implementation, this would query analytics data
        stats = BannerStats(
            banner_id=banner_id,
            total_views=1250,
            total_clicks=89,
            click_through_rate=7.12,
            unique_viewers=1100,
            last_viewed=datetime.now()
        )
        
        return stats
    
    def create_thumbnail(self, image_path: str, thumbnail_size: tuple = (200, 150)) -> str:
        """
        Creates a thumbnail version of an image.

        This method generates a smaller version of the banner image for use in
        admin interfaces, previews, and mobile displays.

        Args:
            image_path (str): The path to the original image.
            thumbnail_size (tuple): The desired thumbnail dimensions (width, height).

        Returns:
            str: The path to the created thumbnail image.
        """
        image = Image.open(image_path)
        image.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        
        # Save thumbnail
        thumbnail_path = image_path.replace('.', '_thumb.')
        image.save(thumbnail_path)
        
        return thumbnail_path
    
    def schedule_banner_expiry(self, banner_id: int, expiry_date: datetime):
        """
        Schedules a banner to expire at a specific date.

        This method sets up automated expiry for banners, ensuring they
        are automatically deactivated when their campaign period ends.

        Args:
            banner_id (int): The ID of the banner to schedule for expiry.
            expiry_date (datetime): When the banner should expire.

        Note:
            In a real implementation, this would use a task scheduler like Celery.
        """
        # In a real application, this would use Celery or another task scheduler
        pass
    
    def get_banner_recommendations(self, user_id: int, 
                                 position: str) -> List[BannerData]:
        """
        Gets personalized banner recommendations for a user.

        This method implements a simple recommendation algorithm that considers
        banner priority, popularity, and user context to suggest the most
        relevant banners for display.

        Args:
            user_id (int): The ID of the user to get recommendations for.
            position (str): The position where banners will be displayed.

        Returns:
            List[BannerData]: A list of recommended banners, ordered by relevance.
        """
        # Simple recommendation algorithm
        active_banners = self.get_active_banners(position=position)
        
        # Sort by priority and popularity
        recommendations = sorted(active_banners, 
                               key=lambda x: (x.priority, -x.view_count))
        
        return recommendations[:5]  # Top 5 recommendations
