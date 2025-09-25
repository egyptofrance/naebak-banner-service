# 🖼️ LEADER - دليل خدمة إدارة البنرات

**اسم الخدمة:** naebak-banners-service  
**المنفذ:** 8009  
**الإطار:** Flask 2.3  
**قاعدة البيانات:** Redis (للبيانات البسيطة والسريعة)  
**التخزين:** Google Cloud Storage  

---

## 📋 **نظرة عامة على الخدمة**

### **🎯 الغرض الأساسي:**
خدمة إدارة البنرات مخصصة للتحكم في البنرات الرئيسية عبر منصة نائبك، تشمل:

1. **بنرات صفحة الهبوط الرئيسية** - البنرات الترحيبية والإعلانية الأساسية
2. **بنرات صفحة تصفح النواب** - إعلانات وبنرات توجيهية في صفحة عرض قائمة النواب
3. **بنرات الصفحات الداخلية للنواب** - بنرات مخصصة لكل نائب في صفحته الشخصية
4. **البنرات المنبثقة** - إعلانات مؤقتة وتنبيهات مهمة
5. **البنرات الإعلانية الإضافية** - محتوى ترويجي وإعلامي

هذه خدمة **خفيفة وسريعة** تركز على عرض وإدارة البنرات بكفاءة عالية دون الحاجة لقاعدة بيانات معقدة.

### **🔧 الوظائف الرئيسية:**
1. **رفع وإدارة البنرات** - دعم أنواع ملفات متعددة مع تحسين تلقائي
2. **إدارة المواضع المحددة** - تحكم في البنرات حسب الصفحات:
   - **صفحة الهبوط:** بنرات ترحيبية وإعلانية رئيسية
   - **صفحة تصفح النواب:** بنرات توجيهية وإعلامية
   - **صفحات النواب الفردية:** بنرات مخصصة لكل نائب
   - **البنرات المنبثقة:** تنبيهات وإعلانات مؤقتة
3. **الجدولة الذكية** - تحديد أوقات عرض البنرات وانتهاء الصلاحية
4. **التحليلات السريعة** - تتبع المشاهدات والنقرات في Redis
5. **التحكم في الأذونات** - إدارة من يمكنه إنشاء وتعديل البنرات
6. **التحسين التلقائي** - ضغط وتحسين الصور للويب والهواتف

---

## 🌐 **دور الخدمة في منصة نائبك**

### **🏛️ المكانة في النظام:**
خدمة البنرات تعمل كنظام إعلاني مركزي يدعم جميع أجزاء المنصة بالمحتوى البصري والإعلانات المهمة.

### **📡 العلاقات مع الخدمات الأخرى:**

#### **🔗 الخدمات المباشرة:**
- **خدمة المصادقة (8001)** - للتحقق من صلاحيات المستخدمين
- **خدمة الإدارة (8002)** - لموافقة المديرين على البنرات
- **خدمة الإحصائيات (8012)** - لإرسال بيانات المشاهدات والنقرات
- **خدمة البوابة (8013)** - لتوجيه الطلبات وتوزيع الأحمال

#### **🔄 التفاعلات:**
```
Frontend (3000) → Gateway (8013) → Banners Service (8009)
                                        ↓
Statistics Service (8012) ← Analytics Data
                                        ↓
Auth Service (8001) ← Permission Check
                                        ↓
Admin Service (8002) ← Approval Workflow
```

#### **📊 تدفق البيانات:**
1. **الواجهة الأمامية** تطلب البنرات النشطة
2. **خدمة البنرات** تتحقق من الصلاحيات مع خدمة المصادقة
3. **إرسال البيانات** للإحصائيات عند كل مشاهدة/نقرة
4. **التنسيق مع خدمة الإدارة** لموافقة البنرات الجديدة

---

## 📦 **البيانات والنماذج من المستودع المخزن**

### **🏛️ المحافظات المصرية (27 محافظة):**
```python
GOVERNORATES = [
    {"name": "القاهرة", "name_en": "Cairo", "code": "CAI"},
    {"name": "الجيزة", "name_en": "Giza", "code": "GIZ"},
    {"name": "الإسكندرية", "name_en": "Alexandria", "code": "ALX"},
    # ... باقي المحافظات الـ 27
]
```
**الاستخدام:** تحديد البنرات المخصصة لمحافظات معينة

### **🎭 أنواع البنرات (6 أنواع):**
```python
BANNER_TYPES = [
    {"type": "hero", "name": "بنر رئيسي", "recommended_size": "1920x600"},
    {"type": "sidebar", "name": "بنر جانبي", "recommended_size": "300x250"},
    {"type": "header", "name": "بنر علوي", "recommended_size": "728x90"},
    {"type": "footer", "name": "بنر سفلي", "recommended_size": "728x90"},
    {"type": "popup", "name": "بنر منبثق", "recommended_size": "600x400"},
    {"type": "mobile", "name": "بنر الهاتف", "recommended_size": "320x100"}
]
```

### **📍 مواضع العرض (6 مواضع):**
```python
BANNER_POSITIONS = [
    {"position": "top", "name": "أعلى الصفحة", "priority": 1},
    {"position": "middle", "name": "وسط الصفحة", "priority": 2},
    {"position": "bottom", "name": "أسفل الصفحة", "priority": 3},
    {"position": "sidebar_right", "name": "الشريط الجانبي الأيمن", "priority": 4},
    {"position": "sidebar_left", "name": "الشريط الجانبي الأيسر", "priority": 5},
    {"position": "floating", "name": "عائم", "priority": 6}
]
```

### **📂 فئات البنرات (6 فئات):**
```python
BANNER_CATEGORIES = [
    {"category": "political", "name": "سياسي", "icon": "🗳️"},
    {"category": "informational", "name": "إعلامي", "icon": "📢"},
    {"category": "service", "name": "خدمي", "icon": "🏛️"},
    {"category": "event", "name": "فعالية", "icon": "📅"},
    {"category": "announcement", "name": "إعلان", "icon": "📣"},
    {"category": "emergency", "name": "طوارئ", "icon": "🚨"}
]
```

### **🔄 حالات البنر (7 حالات):**
```python
BANNER_STATUS = [
    {"status": "draft", "name": "مسودة", "color": "#6C757D"},
    {"status": "pending", "name": "في الانتظار", "color": "#FFC107"},
    {"status": "approved", "name": "معتمد", "color": "#28A745"},
    {"status": "active", "name": "نشط", "color": "#007BFF"},
    {"status": "paused", "name": "متوقف", "color": "#FD7E14"},
    {"status": "expired", "name": "منتهي الصلاحية", "color": "#DC3545"},
    {"status": "rejected", "name": "مرفوض", "color": "#DC3545"}
]
```

---

## ⚙️ **إعدادات Google Cloud Run**
### **🛠️ بيئة التطوير (Development):**
```yaml
service_name: naebak-banners-service-dev
image: gcr.io/naebak-472518/banners-service:dev
cpu: 0.3
memory: 256Mi
min_instances: 0
max_instances: 3
concurrency: 100
timeout: 300s

environment_variables:
  - FLASK_ENV=development
  - DEBUG=true
  - LOG_LEVEL=DEBUG
  - REQUIRE_ADMIN_APPROVAL=false
  - IMAGE_OPTIMIZATION=false
  - CDN_ENABLED=false
  - REDIS_URL=redis://localhost:6379/9
```

### **🏭 إعدادات بيئة الإنتاج:**
```yaml
service_name: naebak-banners-service
image: gcr.io/naebak-472518/banners-service:latest
cpu: 0.3
memory: 256Mi
min_instances: 1
max_instances: 5
concurrency: 1000
timeout: 60s

environment_variables:
  - FLASK_ENV=production
  - DEBUG=false
  - LOG_LEVEL=WARNING
  - REQUIRE_ADMIN_APPROVAL=true
  - IMAGE_OPTIMIZATION=true
  - CDN_ENABLED=true
  - REDIS_URL=${REDIS_URL}
```**🔧 إعدادات Google Cloud Storage:**
```yaml
# بيئة التطوير
GCS_BUCKET_NAME: naebak-banners-dev
GCS_PROJECT_ID: naebak-472518
CDN_BASE_URL: https://storage.googleapis.com/naebak-banners-dev/

# بيئة الإنتاج
GCS_BUCKET_NAME: naebak-banners-prod
GCS_PROJECT_ID: naebak-472518
CDN_BASE_URL: https://cdn.naebak.com/banners/
```

---

## 🔐 **الأمان والصلاحيات**

### **🛡️ مستويات الوصول:**
1. **مشاهد عام** - عرض البنرات النشطة فقط
2. **مستخدم مسجل** - عرض البنرات + تتبع التفاعل
3. **محرر محتوى** - إنشاء وتعديل البنرات (تحتاج موافقة)
4. **مدير** - موافقة ورفض البنرات
5. **مدير عام** - تحكم كامل في النظام

### **🔒 آليات الحماية:**
- **JWT Authentication** للعمليات الحساسة
- **Rate Limiting** - 200 طلب/ساعة للمستخدم العادي
- **File Validation** - فحص نوع وحجم الملفات
- **Image Scanning** - فحص المحتوى المرفوع
- **CORS Protection** - حماية من الطلبات الخارجية

---

## 📊 **المتغيرات والثوابت الأساسية**

### **🔢 إعدادات الملفات:**
```python
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
    'CACHE_DURATION_SECONDS': 3600
}
```

### **📁 أنواع الملفات المدعومة:**
```python
SUPPORTED_FILE_TYPES = [
    {"extension": "jpg", "mime_type": "image/jpeg", "max_size_mb": 5},
    {"extension": "png", "mime_type": "image/png", "max_size_mb": 5},
    {"extension": "gif", "mime_type": "image/gif", "max_size_mb": 3},
    {"extension": "webp", "mime_type": "image/webp", "max_size_mb": 4},
    {"extension": "svg", "mime_type": "image/svg+xml", "max_size_mb": 1}
]
```

---

## 🔗 **واجهات برمجة التطبيقات (APIs)**

### **📡 نقاط النهاية الرئيسية:**
```
GET  /health                           - فحص صحة الخدمة
GET  /api/banners/                     - قائمة البنرات النشطة
GET  /api/banners/<id>                 - بنر محدد
POST /api/banners/                     - إنشاء بنر جديد (يحتاج مصادقة)
PUT  /api/banners/<id>                 - تحديث بنر (يحتاج مصادقة)
DELETE /api/banners/<id>               - حذف بنر (يحتاج مصادقة)
POST /api/banners/<id>/click           - تسجيل نقرة
GET  /api/banners/<id>/stats           - إحصائيات البنر
GET  /api/banners/types                - أنواع البنرات المتاحة
GET  /api/banners/positions            - مواضع البنرات المتاحة
GET  /api/banners/categories           - فئات البنرات المتاحة
GET  /api/banners/recommendations      - توصيات البنرات
```

### **📥 مثال طلب إنشاء بنر:**
```json
POST /api/banners/
Content-Type: multipart/form-data
Authorization: Bearer <jwt_token>

{
  "title": "مرحباً بكم في منصة نائبك",
  "description": "منصة تفاعلية للتواصل مع ممثليكم",
  "link_url": "https://naebak.com/about",
  "alt_text": "صورة ترحيبية لمنصة نائبك",
  "banner_type": "hero",
  "position": "top",
  "category": "informational",
  "priority": 1,
  "governorate": "القاهرة",
  "start_date": "2025-01-01T00:00:00Z",
  "end_date": "2025-12-31T23:59:59Z",
  "image": <file>
}
```

---

## 🔄 **الفروق بين بيئات التشغيل**

### **🛠️ بيئة التطوير (Development):**
- **قاعدة البيانات:** Redis محلي (localhost:6379)
- **التخزين:** مجلد محلي
- **الموافقات:** تلقائية بدون مراجعة
- **التحسين:** معطل لسرعة التطوير
- **التسجيل:** مفصل (DEBUG level)
- **الحد الأدنى للخوادم:** 0 (توفير في التكلفة)
- **الموارد:** 0.3 CPU, 256Mi Memory (خفيف)

### **🏭 بيئة الإنتاج (Production):**
- **قاعدة البيانات:** Redis على Cloud Memorystore
- **التخزين:** Google Cloud Storage مع CDN
- **الموافقات:** مطلوبة من المديرين
- **التحسين:** مفعل لأفضل أداء
- **التسجيل:** أخطاء فقط (WARNING level)
- **الحد الأدنى للخوادم:** 1 (ضمان التوفر)
- **الموارد:** 0.3 CPU, 256Mi Memory (محسن للسرعة)

### **🧪 بيئة الاختبار (Testing):**
- **قاعدة البيانات:** Redis في الذاكرة (Memory)
- **التخزين:** مؤقت
- **الموافقات:** محاكاة
- **التحسين:** معطل
- **التسجيل:** شامل للتتبع
- **الحد الأدنى للخوادم:** 0

---

## 📈 **المراقبة والتحليلات**

### **📊 المقاييس المهمة:**
- **معدل الاستجابة** - يجب أن يكون أقل من 200ms
- **معدل النجاح** - يجب أن يكون أعلى من 99.5%
- **استخدام الذاكرة** - يجب ألا يتجاوز 80%
- **استخدام المعالج** - يجب ألا يتجاوز 70%
- **عدد البنرات النشطة** - مراقبة النمو
- **معدل النقر** - قياس فعالية البنرات

### **🚨 التنبيهات:**
- **خطأ في رفع الملفات** - تنبيه فوري
- **تجاوز حد التخزين** - تنبيه يومي
- **بنرات منتهية الصلاحية** - تنبيه أسبوعي
- **استخدام مفرط للموارد** - تنبيه فوري

---

## 🚀 **خطوات التطوير المطلوبة**

### **🎯 المرحلة الأولى - الأساسيات:**
1. ✅ إعداد البنية الأساسية
2. ✅ إنشاء نماذج البيانات
3. ✅ تطبيق واجهات برمجة التطبيقات
4. ⏳ ربط قاعدة البيانات
5. ⏳ تطبيق نظام رفع الملفات

### **🎯 المرحلة الثانية - الميزات المتقدمة:**
1. ⏳ تطبيق نظام الموافقات
2. ⏳ ربط Google Cloud Storage
3. ⏳ تطبيق نظام التحليلات
4. ⏳ إضافة نظام الجدولة
5. ⏳ تطبيق التحسين التلقائي للصور

### **🎯 المرحلة الثالثة - التكامل:**
1. ⏳ ربط خدمة المصادقة
2. ⏳ ربط خدمة الإحصائيات
3. ⏳ ربط خدمة الإدارة
4. ⏳ اختبار التكامل الشامل
5. ⏳ نشر بيئة الإنتاج

---

## 📚 **الموارد والمراجع**

### **📖 الوثائق المرجعية:**
- [مستودع المخزن - مواصفات الخدمات](../naebak-almakhzan/04-code-examples/03-services-specifications.md)
- [مستودع المخزن - البيانات الأولية](../naebak-almakhzan/02-data-models/04-initial-data.md)
- [مستودع المخزن - البنية التحتية](../naebak-almakhzan/07-infrastructure/01-deployment-infrastructure.md)

### **🔧 أدوات التطوير:**
- **Flask 2.3** - إطار العمل الأساسي
- **Pillow** - معالجة الصور
- **Google Cloud Storage** - تخزين الملفات
- **Redis** - التخزين المؤقت
- **PostgreSQL/SQLite** - قاعدة البيانات

---

**📝 ملاحظة:** هذا الملف هو الدليل الشامل لخدمة البنرات. يجب مراجعته وتحديثه مع كل تطوير جديد في الخدمة.
