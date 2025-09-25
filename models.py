# -*- coding: utf-8 -*-
"""نماذج البيانات الأساسية لخدمة إدارة البنرات"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
from PIL import Image
import constants

@dataclass
class BannerData:
    """نموذج بيانات البنر"""
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
        """تحويل البيانات إلى قاموس"""
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
    """إحصائيات البنر"""
    banner_id: int
    total_views: int = 0
    total_clicks: int = 0
    click_through_rate: float = 0.0
    unique_viewers: int = 0
    last_viewed: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل البيانات إلى قاموس"""
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
    """معلومات الصورة"""
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
        """تحويل البيانات إلى قاموس"""
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
    """خدمة إدارة البنرات"""
    
    def __init__(self, config):
        self.config = config
        self.upload_folder = config.UPLOAD_FOLDER
        self.max_file_size = config.MAX_CONTENT_LENGTH
        self.allowed_extensions = config.ALLOWED_EXTENSIONS
    
    def validate_banner_data(self, banner_data: BannerData) -> List[str]:
        """التحقق من صحة بيانات البنر"""
        errors = []
        
        # التحقق من العنوان
        if not banner_data.title or len(banner_data.title.strip()) < 3:
            errors.append("العنوان مطلوب ويجب أن يكون 3 أحرف على الأقل")
        
        # التحقق من النص البديل
        if self.config.REQUIRE_ADMIN_APPROVAL and not banner_data.alt_text:
            errors.append("النص البديل مطلوب")
        
        # التحقق من نوع البنر
        valid_types = [bt['type'] for bt in constants.BANNER_TYPES]
        if banner_data.banner_type not in valid_types:
            errors.append("نوع البنر غير صحيح")
        
        # التحقق من الموضع
        valid_positions = [pos['position'] for pos in constants.BANNER_POSITIONS]
        if banner_data.position not in valid_positions:
            errors.append("موضع البنر غير صحيح")
        
        # التحقق من الفئة
        valid_categories = [cat['category'] for cat in constants.BANNER_CATEGORIES]
        if banner_data.category not in valid_categories:
            errors.append("فئة البنر غير صحيحة")
        
        # التحقق من التواريخ
        if banner_data.start_date and banner_data.end_date:
            if banner_data.start_date >= banner_data.end_date:
                errors.append("تاريخ البداية يجب أن يكون قبل تاريخ النهاية")
        
        return errors
    
    def validate_image_file(self, file) -> List[str]:
        """التحقق من صحة ملف الصورة"""
        errors = []
        
        # التحقق من وجود الملف
        if not file or not file.filename:
            errors.append("لم يتم اختيار ملف")
            return errors
        
        # التحقق من نوع الملف
        if not constants.is_valid_file_type(file.filename):
            errors.append("نوع الملف غير مدعوم")
            return errors
        
        # التحقق من حجم الملف
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        max_size = self.max_file_size
        if file_size > max_size:
            errors.append(f"حجم الملف كبير جداً (الحد الأقصى: {max_size // (1024*1024)}MB)")
        
        return errors
    
    def process_image(self, file, banner_type: str) -> ImageInfo:
        """معالجة وتحسين الصورة"""
        # الحصول على معلومات نوع البنر
        banner_info = constants.get_banner_type_info(banner_type)
        
        # فتح الصورة
        image = Image.open(file)
        original_width, original_height = image.size
        
        # تحسين الصورة إذا كان مطلوباً
        if self.config.IMAGE_OPTIMIZATION:
            # ضغط الصورة
            if image.format in ['JPEG', 'JPG']:
                image = image.convert('RGB')
        
        # تغيير الحجم إذا كان مطلوباً
        if self.config.AUTO_RESIZE and banner_info:
            recommended_size = banner_info.get('recommended_size', '').split('x')
            if len(recommended_size) == 2:
                target_width = int(recommended_size[0])
                target_height = int(recommended_size[1])
                
                # تغيير الحجم مع الحفاظ على النسبة
                image.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
        
        # إنشاء معلومات الصورة
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
        """الحصول على البنرات النشطة"""
        # هذه دالة نموذجية - في التطبيق الفعلي ستتصل بقاعدة البيانات
        banners = []
        
        # بيانات تجريبية
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
        
        # تطبيق الفلاتر
        for banner in sample_banners:
            if position and banner.position != position:
                continue
            if category and banner.category != category:
                continue
            if governorate and banner.governorate and banner.governorate != governorate:
                continue
            banners.append(banner)
        
        # ترتيب حسب الأولوية
        banners.sort(key=lambda x: x.priority)
        
        return banners
    
    def get_banner_analytics(self, banner_id: int, 
                           start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> BannerStats:
        """الحصول على إحصائيات البنر"""
        # بيانات تجريبية
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
        """إنشاء صورة مصغرة"""
        image = Image.open(image_path)
        image.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        
        # حفظ الصورة المصغرة
        thumbnail_path = image_path.replace('.', '_thumb.')
        image.save(thumbnail_path)
        
        return thumbnail_path
    
    def schedule_banner_expiry(self, banner_id: int, expiry_date: datetime):
        """جدولة انتهاء صلاحية البنر"""
        # في التطبيق الفعلي، سيتم استخدام Celery أو مجدول مهام آخر
        pass
    
    def get_banner_recommendations(self, user_id: int, 
                                 position: str) -> List[BannerData]:
        """الحصول على توصيات البنرات للمستخدم"""
        # خوارزمية بسيطة للتوصيات
        active_banners = self.get_active_banners(position=position)
        
        # ترتيب حسب الأولوية والشعبية
        recommendations = sorted(active_banners, 
                               key=lambda x: (x.priority, -x.view_count))
        
        return recommendations[:5]  # أفضل 5 توصيات
