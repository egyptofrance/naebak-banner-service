# -*- coding: utf-8 -*-
"""ثوابت وبيانات أساسية لخدمة إدارة البنرات"""

# أنواع البنرات
BANNER_TYPES = [
    {
        "type": "hero",
        "name": "بنر رئيسي",
        "name_en": "Hero Banner",
        "description": "البنر الرئيسي في أعلى الصفحة",
        "recommended_size": "1920x600",
        "max_file_size_mb": 5
    },
    {
        "type": "sidebar",
        "name": "بنر جانبي",
        "name_en": "Sidebar Banner",
        "description": "بنر في الشريط الجانبي",
        "recommended_size": "300x250",
        "max_file_size_mb": 2
    },
    {
        "type": "header",
        "name": "بنر علوي",
        "name_en": "Header Banner",
        "description": "بنر في رأس الصفحة",
        "recommended_size": "728x90",
        "max_file_size_mb": 1
    },
    {
        "type": "footer",
        "name": "بنر سفلي",
        "name_en": "Footer Banner",
        "description": "بنر في أسفل الصفحة",
        "recommended_size": "728x90",
        "max_file_size_mb": 1
    },
    {
        "type": "popup",
        "name": "بنر منبثق",
        "name_en": "Popup Banner",
        "description": "بنر منبثق",
        "recommended_size": "600x400",
        "max_file_size_mb": 3
    },
    {
        "type": "mobile",
        "name": "بنر الهاتف",
        "name_en": "Mobile Banner",
        "description": "بنر مخصص للهواتف المحمولة",
        "recommended_size": "320x100",
        "max_file_size_mb": 1
    }
]

# مواضع البنرات
BANNER_POSITIONS = [
    {
        "position": "top",
        "name": "أعلى الصفحة",
        "name_en": "Top of Page",
        "priority": 1
    },
    {
        "position": "middle",
        "name": "وسط الصفحة",
        "name_en": "Middle of Page",
        "priority": 2
    },
    {
        "position": "bottom",
        "name": "أسفل الصفحة",
        "name_en": "Bottom of Page",
        "priority": 3
    },
    {
        "position": "sidebar_right",
        "name": "الشريط الجانبي الأيمن",
        "name_en": "Right Sidebar",
        "priority": 4
    },
    {
        "position": "sidebar_left",
        "name": "الشريط الجانبي الأيسر",
        "name_en": "Left Sidebar",
        "priority": 5
    },
    {
        "position": "floating",
        "name": "عائم",
        "name_en": "Floating",
        "priority": 6
    }
]

# حالات البنر
BANNER_STATUS = [
    {"status": "draft", "name": "مسودة", "name_en": "Draft", "color": "#6C757D"},
    {"status": "pending", "name": "في الانتظار", "name_en": "Pending", "color": "#FFC107"},
    {"status": "approved", "name": "معتمد", "name_en": "Approved", "color": "#28A745"},
    {"status": "active", "name": "نشط", "name_en": "Active", "color": "#007BFF"},
    {"status": "paused", "name": "متوقف", "name_en": "Paused", "color": "#FD7E14"},
    {"status": "expired", "name": "منتهي الصلاحية", "name_en": "Expired", "color": "#DC3545"},
    {"status": "rejected", "name": "مرفوض", "name_en": "Rejected", "color": "#DC3545"}
]

# فئات البنرات
BANNER_CATEGORIES = [
    {
        "category": "political",
        "name": "سياسي",
        "name_en": "Political",
        "description": "بنرات سياسية وانتخابية",
        "icon": "🗳️"
    },
    {
        "category": "informational",
        "name": "إعلامي",
        "name_en": "Informational",
        "description": "بنرات إعلامية وتوعوية",
        "icon": "📢"
    },
    {
        "category": "service",
        "name": "خدمي",
        "name_en": "Service",
        "description": "بنرات الخدمات الحكومية",
        "icon": "🏛️"
    },
    {
        "category": "event",
        "name": "فعالية",
        "name_en": "Event",
        "description": "بنرات الفعاليات والمؤتمرات",
        "icon": "📅"
    },
    {
        "category": "announcement",
        "name": "إعلان",
        "name_en": "Announcement",
        "description": "إعلانات عامة ومهمة",
        "icon": "📣"
    },
    {
        "category": "emergency",
        "name": "طوارئ",
        "name_en": "Emergency",
        "description": "بنرات الطوارئ والتنبيهات",
        "icon": "🚨"
    }
]

# المحافظات المصرية
GOVERNORATES = [
    {"name": "القاهرة", "name_en": "Cairo", "code": "CAI"},
    {"name": "الجيزة", "name_en": "Giza", "code": "GIZ"},
    {"name": "الإسكندرية", "name_en": "Alexandria", "code": "ALX"},
    {"name": "الدقهلية", "name_en": "Dakahlia", "code": "DAK"},
    {"name": "البحر الأحمر", "name_en": "Red Sea", "code": "RSS"},
    {"name": "البحيرة", "name_en": "Beheira", "code": "BEH"},
    {"name": "الفيوم", "name_en": "Fayoum", "code": "FAY"},
    {"name": "الغربية", "name_en": "Gharbia", "code": "GHR"},
    {"name": "الإسماعيلية", "name_en": "Ismailia", "code": "ISM"},
    {"name": "المنوفية", "name_en": "Monufia", "code": "MNF"},
    {"name": "المنيا", "name_en": "Minya", "code": "MNY"},
    {"name": "القليوبية", "name_en": "Qalyubia", "code": "QLY"},
    {"name": "الوادي الجديد", "name_en": "New Valley", "code": "WAD"},
    {"name": "شمال سيناء", "name_en": "North Sinai", "code": "NSI"},
    {"name": "جنوب سيناء", "name_en": "South Sinai", "code": "SSI"},
    {"name": "الشرقية", "name_en": "Sharqia", "code": "SHR"},
    {"name": "سوهاج", "name_en": "Sohag", "code": "SOH"},
    {"name": "السويس", "name_en": "Suez", "code": "SUZ"},
    {"name": "أسوان", "name_en": "Aswan", "code": "ASW"},
    {"name": "أسيوط", "name_en": "Asyut", "code": "ASY"},
    {"name": "بني سويف", "name_en": "Beni Suef", "code": "BNS"},
    {"name": "بورسعيد", "name_en": "Port Said", "code": "PTS"},
    {"name": "دمياط", "name_en": "Damietta", "code": "DAM"},
    {"name": "كفر الشيخ", "name_en": "Kafr El Sheikh", "code": "KFS"},
    {"name": "مطروح", "name_en": "Matrouh", "code": "MAT"},
    {"name": "الأقصر", "name_en": "Luxor", "code": "LUX"},
    {"name": "قنا", "name_en": "Qena", "code": "QEN"}
]

# أنواع الملفات المدعومة
SUPPORTED_FILE_TYPES = [
    {
        "extension": "jpg",
        "mime_type": "image/jpeg",
        "name": "JPEG",
        "max_size_mb": 5,
        "supports_transparency": False
    },
    {
        "extension": "jpeg",
        "mime_type": "image/jpeg",
        "name": "JPEG",
        "max_size_mb": 5,
        "supports_transparency": False
    },
    {
        "extension": "png",
        "mime_type": "image/png",
        "name": "PNG",
        "max_size_mb": 5,
        "supports_transparency": True
    },
    {
        "extension": "gif",
        "mime_type": "image/gif",
        "name": "GIF",
        "max_size_mb": 3,
        "supports_transparency": True,
        "supports_animation": True
    },
    {
        "extension": "webp",
        "mime_type": "image/webp",
        "name": "WebP",
        "max_size_mb": 4,
        "supports_transparency": True
    },
    {
        "extension": "svg",
        "mime_type": "image/svg+xml",
        "name": "SVG",
        "max_size_mb": 1,
        "supports_transparency": True,
        "is_vector": True
    }
]

# إعدادات البنرات
BANNER_SETTINGS = {
    'MAX_BANNERS_PER_USER': 10,
    'MAX_BANNERS_PER_POSITION': 5,
    'DEFAULT_BANNER_DURATION_DAYS': 30,
    'MAX_BANNER_DURATION_DAYS': 365,
    'MIN_BANNER_WIDTH': 300,
    'MAX_BANNER_WIDTH': 1920,
    'MIN_BANNER_HEIGHT': 150,
    'MAX_BANNER_HEIGHT': 1080,
    'COMPRESSION_QUALITY': 85,
    'THUMBNAIL_SIZE': (200, 150),
    'CACHE_DURATION_SECONDS': 3600,
    'AUTO_APPROVE_TRUSTED_USERS': True,
    'REQUIRE_ALT_TEXT': True,
    'MAX_ALT_TEXT_LENGTH': 125
}

# رسائل التحقق والأخطاء
VALIDATION_MESSAGES = {
    'FILE_TOO_LARGE': 'حجم الملف كبير جداً',
    'INVALID_FILE_TYPE': 'نوع الملف غير مدعوم',
    'INVALID_DIMENSIONS': 'أبعاد الصورة غير صحيحة',
    'MISSING_ALT_TEXT': 'النص البديل مطلوب',
    'INVALID_POSITION': 'موضع البنر غير صحيح',
    'EXPIRED_BANNER': 'البنر منتهي الصلاحية',
    'UNAUTHORIZED_ACCESS': 'غير مخول للوصول',
    'BANNER_LIMIT_EXCEEDED': 'تم تجاوز الحد الأقصى للبنرات',
    'INVALID_DATE_RANGE': 'نطاق التاريخ غير صحيح'
}

# أولويات العرض
DISPLAY_PRIORITIES = [
    {"priority": 1, "name": "عالية جداً", "name_en": "Very High"},
    {"priority": 2, "name": "عالية", "name_en": "High"},
    {"priority": 3, "name": "متوسطة", "name_en": "Medium"},
    {"priority": 4, "name": "منخفضة", "name_en": "Low"},
    {"priority": 5, "name": "منخفضة جداً", "name_en": "Very Low"}
]

# للاستخدام في Flask/Django choices
BANNER_TYPE_CHOICES = [(banner['type'], banner['name']) for banner in BANNER_TYPES]
POSITION_CHOICES = [(pos['position'], pos['name']) for pos in BANNER_POSITIONS]
STATUS_CHOICES = [(status['status'], status['name']) for status in BANNER_STATUS]
CATEGORY_CHOICES = [(cat['category'], cat['name']) for cat in BANNER_CATEGORIES]

# وظائف مساعدة
def get_banner_type_info(banner_type):
    """الحصول على معلومات نوع البنر"""
    for banner in BANNER_TYPES:
        if banner['type'] == banner_type:
            return banner
    return None

def get_file_type_info(extension):
    """الحصول على معلومات نوع الملف"""
    for file_type in SUPPORTED_FILE_TYPES:
        if file_type['extension'] == extension.lower():
            return file_type
    return None

def is_valid_file_type(filename):
    """التحقق من صحة نوع الملف"""
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return any(ft['extension'] == extension for ft in SUPPORTED_FILE_TYPES)

def get_max_file_size(extension):
    """الحصول على الحد الأقصى لحجم الملف"""
    file_info = get_file_type_info(extension)
    return file_info['max_size_mb'] if file_info else 5
