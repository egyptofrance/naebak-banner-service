"""
نماذج خدمة البانرات - مشروع نائبك
Flask + SQLite Models
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()


class BannerType(db.Model):
    """أنواع البانرات"""
    __tablename__ = 'banner_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    name_en = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(7), default='#007BFF')  # HEX color
    priority = db.Column(db.Integer, default=1)  # 1=عالي, 5=منخفض
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    banners = db.relationship('Banner', backref='banner_type', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<BannerType {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'priority': self.priority,
            'is_active': self.is_active,
            'banners_count': len(self.banners),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class BannerPosition(db.Model):
    """مواضع عرض البانرات"""
    __tablename__ = 'banner_positions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    name_en = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    css_class = db.Column(db.String(100))  # CSS class للتنسيق
    max_banners = db.Column(db.Integer, default=1)  # حد أقصى للبانرات في هذا الموضع
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    banners = db.relationship('Banner', backref='banner_position', lazy=True)
    
    def __repr__(self):
        return f'<BannerPosition {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'description': self.description,
            'css_class': self.css_class,
            'max_banners': self.max_banners,
            'display_order': self.display_order,
            'is_active': self.is_active,
            'active_banners_count': len([b for b in self.banners if b.is_active]),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Banner(db.Model):
    """البانرات الرئيسية"""
    __tablename__ = 'banners'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200))
    content = db.Column(db.Text)
    content_en = db.Column(db.Text)
    
    # الروابط والصور
    image_url = db.Column(db.String(500))
    link_url = db.Column(db.String(500))
    link_text = db.Column(db.String(100))
    link_target = db.Column(db.String(20), default='_self')  # _self, _blank
    
    # الإعدادات
    type_id = db.Column(db.Integer, db.ForeignKey('banner_types.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('banner_positions.id'), nullable=False)
    priority = db.Column(db.Integer, default=1)  # 1=عالي, 5=منخفض
    
    # التوقيت
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    
    # الحالة
    is_active = db.Column(db.Boolean, default=True)
    is_published = db.Column(db.Boolean, default=False)
    
    # إعدادات العرض
    show_close_button = db.Column(db.Boolean, default=True)
    auto_hide_after = db.Column(db.Integer)  # بالثواني
    animation_type = db.Column(db.String(50), default='fade')  # fade, slide, bounce
    
    # البيانات الإضافية
    custom_css = db.Column(db.Text)
    custom_js = db.Column(db.Text)
    metadata = db.Column(db.Text)  # JSON data
    
    # التتبع
    view_count = db.Column(db.Integer, default=0)
    click_count = db.Column(db.Integer, default=0)
    
    # الطوابع الزمنية
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # العلاقات
    schedules = db.relationship('BannerSchedule', backref='banner', lazy=True, cascade='all, delete-orphan')
    stats = db.relationship('BannerStats', backref='banner', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Banner {self.title}>'
    
    def is_active_now(self):
        """التحقق من نشاط البانر الآن"""
        now = datetime.utcnow()
        
        # التحقق من الحالة الأساسية
        if not self.is_active or not self.is_published:
            return False
        
        # التحقق من التاريخ
        if self.start_date and now < self.start_date:
            return False
        
        if self.end_date and now > self.end_date:
            return False
        
        return True
    
    def get_metadata(self):
        """الحصول على البيانات الإضافية"""
        if self.metadata:
            try:
                return json.loads(self.metadata)
            except:
                return {}
        return {}
    
    def set_metadata(self, data):
        """تعيين البيانات الإضافية"""
        self.metadata = json.dumps(data, ensure_ascii=False)
    
    def increment_view_count(self):
        """زيادة عدد المشاهدات"""
        self.view_count += 1
        db.session.commit()
    
    def increment_click_count(self):
        """زيادة عدد النقرات"""
        self.click_count += 1
        db.session.commit()
    
    def to_dict(self, include_stats=False):
        data = {
            'id': self.id,
            'title': self.title,
            'title_en': self.title_en,
            'content': self.content,
            'content_en': self.content_en,
            'image_url': self.image_url,
            'link_url': self.link_url,
            'link_text': self.link_text,
            'link_target': self.link_target,
            'type': self.banner_type.to_dict() if self.banner_type else None,
            'position': self.banner_position.to_dict() if self.banner_position else None,
            'priority': self.priority,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'is_published': self.is_published,
            'is_active_now': self.is_active_now(),
            'show_close_button': self.show_close_button,
            'auto_hide_after': self.auto_hide_after,
            'animation_type': self.animation_type,
            'custom_css': self.custom_css,
            'custom_js': self.custom_js,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
        
        if include_stats:
            data.update({
                'view_count': self.view_count,
                'click_count': self.click_count,
                'ctr': round((self.click_count / max(self.view_count, 1)) * 100, 2)  # Click Through Rate
            })
        
        return data


class BannerSchedule(db.Model):
    """جدولة البانرات"""
    __tablename__ = 'banner_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    banner_id = db.Column(db.Integer, db.ForeignKey('banners.id'), nullable=False)
    
    # أيام الأسبوع (0=الأحد, 6=السبت)
    days_of_week = db.Column(db.String(20))  # "0,1,2,3,4,5,6" أو "1,2,3,4,5" للأيام العملية
    
    # أوقات العرض
    start_time = db.Column(db.Time)  # وقت البداية اليومي
    end_time = db.Column(db.Time)    # وقت النهاية اليومي
    
    # المناطق الزمنية
    timezone = db.Column(db.String(50), default='Africa/Cairo')
    
    # الحالة
    is_active = db.Column(db.Boolean, default=True)
    
    # الطوابع الزمنية
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BannerSchedule {self.banner_id}>'
    
    def get_days_list(self):
        """الحصول على قائمة الأيام"""
        if self.days_of_week:
            return [int(d) for d in self.days_of_week.split(',')]
        return []
    
    def set_days_list(self, days):
        """تعيين قائمة الأيام"""
        self.days_of_week = ','.join(map(str, days))
    
    def is_scheduled_now(self):
        """التحقق من الجدولة الآن"""
        if not self.is_active:
            return False
        
        now = datetime.now()
        
        # التحقق من اليوم
        if self.days_of_week:
            current_day = now.weekday()  # 0=الاثنين, 6=الأحد
            # تحويل للنظام المستخدم (0=الأحد)
            current_day = (current_day + 1) % 7
            if current_day not in self.get_days_list():
                return False
        
        # التحقق من الوقت
        current_time = now.time()
        if self.start_time and current_time < self.start_time:
            return False
        if self.end_time and current_time > self.end_time:
            return False
        
        return True
    
    def to_dict(self):
        return {
            'id': self.id,
            'banner_id': self.banner_id,
            'days_of_week': self.get_days_list(),
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'timezone': self.timezone,
            'is_active': self.is_active,
            'is_scheduled_now': self.is_scheduled_now(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class BannerStats(db.Model):
    """إحصائيات البانرات"""
    __tablename__ = 'banner_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    banner_id = db.Column(db.Integer, db.ForeignKey('banners.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    # الإحصائيات اليومية
    views = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    unique_views = db.Column(db.Integer, default=0)
    unique_clicks = db.Column(db.Integer, default=0)
    
    # معدلات الأداء
    ctr = db.Column(db.Float, default=0.0)  # Click Through Rate
    avg_view_duration = db.Column(db.Float, default=0.0)  # بالثواني
    
    # بيانات إضافية
    bounce_rate = db.Column(db.Float, default=0.0)
    conversion_rate = db.Column(db.Float, default=0.0)
    
    # الطوابع الزمنية
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # فهرس مركب للأداء
    __table_args__ = (
        db.Index('idx_banner_date', 'banner_id', 'date'),
    )
    
    def __repr__(self):
        return f'<BannerStats {self.banner_id}-{self.date}>'
    
    def calculate_ctr(self):
        """حساب معدل النقر"""
        if self.views > 0:
            self.ctr = round((self.clicks / self.views) * 100, 2)
        else:
            self.ctr = 0.0
    
    def to_dict(self):
        return {
            'id': self.id,
            'banner_id': self.banner_id,
            'date': self.date.isoformat() if self.date else None,
            'views': self.views,
            'clicks': self.clicks,
            'unique_views': self.unique_views,
            'unique_clicks': self.unique_clicks,
            'ctr': self.ctr,
            'avg_view_duration': self.avg_view_duration,
            'bounce_rate': self.bounce_rate,
            'conversion_rate': self.conversion_rate,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserBanner(db.Model):
    """بانرات المرشحين والنواب الشخصية"""
    __tablename__ = 'user_banners'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # ID المرشح/النائب
    user_type = db.Column(db.String(20), nullable=False)  # candidate, representative
    
    # محتوى البانر
    title = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    description = db.Column(db.Text)
    description_en = db.Column(db.Text)
    
    # الصور والروابط
    image_url = db.Column(db.String(500))
    background_image_url = db.Column(db.String(500))
    logo_url = db.Column(db.String(500))
    
    # روابط إضافية
    website_url = db.Column(db.String(500))
    facebook_url = db.Column(db.String(500))
    twitter_url = db.Column(db.String(500))
    instagram_url = db.Column(db.String(500))
    
    # إعدادات التصميم
    primary_color = db.Column(db.String(7), default='#007BFF')
    secondary_color = db.Column(db.String(7), default='#6C757D')
    text_color = db.Column(db.String(7), default='#FFFFFF')
    
    # إعدادات العرض
    layout_type = db.Column(db.String(50), default='standard')  # standard, modern, minimal
    show_social_links = db.Column(db.Boolean, default=True)
    show_contact_info = db.Column(db.Boolean, default=True)
    
    # الحالة والتحكم
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)  # موافقة الإدارة
    approved_by = db.Column(db.Integer)  # ID المدير الذي وافق
    approved_at = db.Column(db.DateTime)
    
    # التحكم في التعديل
    can_edit_by_user = db.Column(db.Boolean, default=True)  # يمكن للمستخدم التعديل
    last_edited_by = db.Column(db.Integer)  # آخر من عدل (user_id أو admin_id)
    last_edit_type = db.Column(db.String(20), default='user')  # user, admin
    
    # البيانات الإضافية
    custom_css = db.Column(db.Text)
    metadata = db.Column(db.Text)  # JSON data
    
    # الطوابع الزمنية
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # فهرس للأداء
    __table_args__ = (
        db.Index('idx_user_type', 'user_id', 'user_type'),
    )
    
    def __repr__(self):
        return f'<UserBanner {self.user_id}-{self.user_type}>'
    
    def get_metadata(self):
        """الحصول على البيانات الإضافية"""
        if self.metadata:
            try:
                return json.loads(self.metadata)
            except:
                return {}
        return {}
    
    def set_metadata(self, data):
        """تعيين البيانات الإضافية"""
        self.metadata = json.dumps(data, ensure_ascii=False)
    
    def can_be_edited_by(self, user_id, is_admin=False):
        """التحقق من إمكانية التعديل"""
        if is_admin:
            return True
        
        if not self.can_edit_by_user:
            return False
        
        return self.user_id == user_id
    
    def approve(self, admin_id):
        """موافقة الإدارة على البانر"""
        self.is_approved = True
        self.approved_by = admin_id
        self.approved_at = datetime.utcnow()
    
    def to_dict(self, include_admin_info=False):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'user_type': self.user_type,
            'title': self.title,
            'title_en': self.title_en,
            'description': self.description,
            'description_en': self.description_en,
            'image_url': self.image_url,
            'background_image_url': self.background_image_url,
            'logo_url': self.logo_url,
            'website_url': self.website_url,
            'facebook_url': self.facebook_url,
            'twitter_url': self.twitter_url,
            'instagram_url': self.instagram_url,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'text_color': self.text_color,
            'layout_type': self.layout_type,
            'show_social_links': self.show_social_links,
            'show_contact_info': self.show_contact_info,
            'is_active': self.is_active,
            'custom_css': self.custom_css,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_admin_info:
            data.update({
                'is_approved': self.is_approved,
                'approved_by': self.approved_by,
                'approved_at': self.approved_at.isoformat() if self.approved_at else None,
                'can_edit_by_user': self.can_edit_by_user,
                'last_edited_by': self.last_edited_by,
                'last_edit_type': self.last_edit_type
            })
        
        return data


class PageBanner(db.Model):
    """بانرات الصفحات (صفحة المرشحين، النواب، إلخ)"""
    __tablename__ = 'page_banners'
    
    id = db.Column(db.Integer, primary_key=True)
    page_key = db.Column(db.String(100), nullable=False, unique=True)  # candidates, representatives, home
    page_name = db.Column(db.String(200), nullable=False)
    page_name_en = db.Column(db.String(200))
    
    # محتوى البانر
    title = db.Column(db.String(200))
    title_en = db.Column(db.String(200))
    subtitle = db.Column(db.String(300))
    subtitle_en = db.Column(db.String(300))
    description = db.Column(db.Text)
    description_en = db.Column(db.Text)
    
    # الصور والخلفيات
    image_url = db.Column(db.String(500))
    background_image_url = db.Column(db.String(500))
    mobile_image_url = db.Column(db.String(500))  # صورة للموبايل
    
    # إعدادات التصميم
    background_color = db.Column(db.String(7), default='#007BFF')
    text_color = db.Column(db.String(7), default='#FFFFFF')
    overlay_opacity = db.Column(db.Float, default=0.5)  # شفافية الطبقة فوق الصورة
    
    # إعدادات العرض
    height = db.Column(db.String(20), default='400px')  # ارتفاع البانر
    alignment = db.Column(db.String(20), default='center')  # left, center, right
    animation_type = db.Column(db.String(50), default='fade')
    
    # أزرار الإجراء
    cta_text = db.Column(db.String(100))  # نص الزر
    cta_text_en = db.Column(db.String(100))
    cta_url = db.Column(db.String(500))  # رابط الزر
    cta_style = db.Column(db.String(50), default='primary')  # primary, secondary, outline
    
    # الحالة
    is_active = db.Column(db.Boolean, default=True)
    is_published = db.Column(db.Boolean, default=False)
    
    # التحكم الإداري
    created_by = db.Column(db.Integer)  # ID المدير الذي أنشأ البانر
    updated_by = db.Column(db.Integer)  # ID آخر من عدل البانر
    
    # البيانات الإضافية
    custom_css = db.Column(db.Text)
    custom_js = db.Column(db.Text)
    metadata = db.Column(db.Text)  # JSON data
    
    # الطوابع الزمنية
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<PageBanner {self.page_key}>'
    
    def get_metadata(self):
        """الحصول على البيانات الإضافية"""
        if self.metadata:
            try:
                return json.loads(self.metadata)
            except:
                return {}
        return {}
    
    def set_metadata(self, data):
        """تعيين البيانات الإضافية"""
        self.metadata = json.dumps(data, ensure_ascii=False)
    
    def publish(self, admin_id):
        """نشر البانر"""
        self.is_published = True
        self.published_at = datetime.utcnow()
        self.updated_by = admin_id
    
    def unpublish(self, admin_id):
        """إلغاء نشر البانر"""
        self.is_published = False
        self.updated_by = admin_id
    
    def to_dict(self, include_admin_info=False):
        data = {
            'id': self.id,
            'page_key': self.page_key,
            'page_name': self.page_name,
            'page_name_en': self.page_name_en,
            'title': self.title,
            'title_en': self.title_en,
            'subtitle': self.subtitle,
            'subtitle_en': self.subtitle_en,
            'description': self.description,
            'description_en': self.description_en,
            'image_url': self.image_url,
            'background_image_url': self.background_image_url,
            'mobile_image_url': self.mobile_image_url,
            'background_color': self.background_color,
            'text_color': self.text_color,
            'overlay_opacity': self.overlay_opacity,
            'height': self.height,
            'alignment': self.alignment,
            'animation_type': self.animation_type,
            'cta_text': self.cta_text,
            'cta_text_en': self.cta_text_en,
            'cta_url': self.cta_url,
            'cta_style': self.cta_style,
            'is_active': self.is_active,
            'is_published': self.is_published,
            'custom_css': self.custom_css,
            'custom_js': self.custom_js,
            'metadata': self.get_metadata(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
        
        if include_admin_info:
            data.update({
                'created_by': self.created_by,
                'updated_by': self.updated_by
            })
        
        return data


class BannerPermission(db.Model):
    """صلاحيات التحكم في البانرات"""
    __tablename__ = 'banner_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # admin, candidate, representative
    
    # صلاحيات البانرات العامة
    can_create_banners = db.Column(db.Boolean, default=False)
    can_edit_banners = db.Column(db.Boolean, default=False)
    can_delete_banners = db.Column(db.Boolean, default=False)
    can_approve_banners = db.Column(db.Boolean, default=False)
    
    # صلاحيات بانرات المستخدمين
    can_edit_own_banner = db.Column(db.Boolean, default=True)
    can_edit_user_banners = db.Column(db.Boolean, default=False)
    can_approve_user_banners = db.Column(db.Boolean, default=False)
    
    # صلاحيات بانرات الصفحات
    can_edit_page_banners = db.Column(db.Boolean, default=False)
    can_publish_page_banners = db.Column(db.Boolean, default=False)
    
    # صلاحيات إضافية
    can_view_stats = db.Column(db.Boolean, default=False)
    can_manage_settings = db.Column(db.Boolean, default=False)
    
    # القيود
    max_banners = db.Column(db.Integer, default=1)  # حد أقصى للبانرات
    max_file_size = db.Column(db.Integer, default=5242880)  # 5MB
    allowed_file_types = db.Column(db.String(200), default='jpg,jpeg,png,gif')
    
    # الحالة
    is_active = db.Column(db.Boolean, default=True)
    
    # الطوابع الزمنية
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # فهرس للأداء
    __table_args__ = (
        db.Index('idx_user_permissions', 'user_id', 'user_type'),
    )
    
    def __repr__(self):
        return f'<BannerPermission {self.user_id}-{self.user_type}>'
    
    def get_allowed_file_types_list(self):
        """الحصول على قائمة أنواع الملفات المسموحة"""
        if self.allowed_file_types:
            return [ext.strip() for ext in self.allowed_file_types.split(',')]
        return []
    
    def set_allowed_file_types_list(self, types):
        """تعيين قائمة أنواع الملفات المسموحة"""
        self.allowed_file_types = ','.join(types)
    
    def can_perform_action(self, action):
        """التحقق من إمكانية تنفيذ إجراء معين"""
        if not self.is_active:
            return False
        
        action_map = {
            'create_banners': self.can_create_banners,
            'edit_banners': self.can_edit_banners,
            'delete_banners': self.can_delete_banners,
            'approve_banners': self.can_approve_banners,
            'edit_own_banner': self.can_edit_own_banner,
            'edit_user_banners': self.can_edit_user_banners,
            'approve_user_banners': self.can_approve_user_banners,
            'edit_page_banners': self.can_edit_page_banners,
            'publish_page_banners': self.can_publish_page_banners,
            'view_stats': self.can_view_stats,
            'manage_settings': self.can_manage_settings
        }
        
        return action_map.get(action, False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_type': self.user_type,
            'can_create_banners': self.can_create_banners,
            'can_edit_banners': self.can_edit_banners,
            'can_delete_banners': self.can_delete_banners,
            'can_approve_banners': self.can_approve_banners,
            'can_edit_own_banner': self.can_edit_own_banner,
            'can_edit_user_banners': self.can_edit_user_banners,
            'can_approve_user_banners': self.can_approve_user_banners,
            'can_edit_page_banners': self.can_edit_page_banners,
            'can_publish_page_banners': self.can_publish_page_banners,
            'can_view_stats': self.can_view_stats,
            'can_manage_settings': self.can_manage_settings,
            'max_banners': self.max_banners,
            'max_file_size': self.max_file_size,
            'allowed_file_types': self.get_allowed_file_types_list(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class BannerSettings(db.Model):
    """إعدادات نظام البانرات"""
    __tablename__ = 'banner_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), nullable=False, unique=True)
    setting_value = db.Column(db.Text)
    setting_type = db.Column(db.String(20), default='string')  # string, integer, boolean, json
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='general')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BannerSettings {self.setting_key}>'
    
    def get_value(self):
        """الحصول على القيمة بالنوع الصحيح"""
        if not self.setting_value:
            return None
        
        try:
            if self.setting_type == 'integer':
                return int(self.setting_value)
            elif self.setting_type == 'boolean':
                return self.setting_value.lower() in ('true', '1', 'yes', 'on')
            elif self.setting_type == 'json':
                return json.loads(self.setting_value)
            else:
                return self.setting_value
        except:
            return self.setting_value
    
    def set_value(self, value):
        """تعيين القيمة"""
        if self.setting_type == 'json':
            self.setting_value = json.dumps(value, ensure_ascii=False)
        else:
            self.setting_value = str(value)
    
    def to_dict(self):
        return {
            'id': self.id,
            'setting_key': self.setting_key,
            'setting_value': self.get_value(),
            'setting_type': self.setting_type,
            'description': self.description,
            'category': self.category,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
