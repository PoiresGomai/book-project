from django.db import models
from django.utils import timezone
from decimal import Decimal
import os
import uuid


# 创建数据库对象模型
# 管理员登录类
class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=32, verbose_name="账号")
    password = models.CharField(max_length=32, verbose_name="密码")
    name = models.CharField(max_length=32, verbose_name="名字")

    # 指定数据表名称（未指定即为默认类名）
    class Meta:
        db_table = "manager"


# 出版社类
class Publisher(models.Model):
    # 出版社名称
    publisher_name = models.CharField(max_length=32, verbose_name="出版社名称")
    # 出版社地址
    publisher_address = models.CharField(max_length=32, verbose_name="出版社地址")

    # 指定数据表名称（未指定即为默认类名）
    class Meta:
        db_table = "publisher"


# 图书类
class Book(models.Model):
    # 图书id
    id = models.AutoField(primary_key=True)
    # 图书名称
    name = models.CharField(max_length=32)
    # 图书描述
    description = models.TextField(verbose_name='图书描述', blank=True, null=True, help_text='图书详细描述信息')
    # 图书封面
    cover_image = models.ImageField(
        upload_to='book_covers/', 
        verbose_name='图书封面', 
        blank=True, 
        null=True,
        help_text='上传图书封面图片'
    )
    # 图书文件/下载链接
    book_file = models.FileField(
        upload_to='book_files/',
        verbose_name='图书文件',
        blank=True,
        null=True,
        help_text='上传图书PDF、EPUB等文件，或者留空使用下载链接'
    )
    download_link = models.URLField(
        max_length=500,
        verbose_name='下载链接',
        blank=True,
        null=True,
        help_text='外部下载链接（Google Drive、OneDrive等）'
    )
    # 图书价格 最多5位，小数保留2位
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # 库存
    inventory = models.IntegerField(verbose_name='库存数')
    # 销量
    sale_num = models.IntegerField(verbose_name='卖出数')
    # 出版社（一对一 外键）
    publisher = models.ForeignKey(to='Publisher', on_delete=models.CASCADE)

    class Meta:
        db_table = "book"
    
    def get_cover_url(self):
        """获取封面图片URL，如果没有封面则返回默认图片"""
        if self.cover_image and hasattr(self.cover_image, 'url'):
            return self.cover_image.url
        return '/static/images/default_book_cover.jpg'
    
    def get_short_description(self, max_length=100):
        """获取简短描述"""
        if self.description:
            if len(self.description) > max_length:
                return self.description[:max_length] + '...'
            return self.description
        return '暂无描述'
    
    def get_medium_description(self):
        """获取中等长度描述(150字符)"""
        return self.get_short_description(150)
    
    def get_brief_description(self):
        """获取简要描述(100字符)"""
        return self.get_short_description(100)
    
    def get_long_description(self):
        """获取较长描述(300字符)"""
        return self.get_short_description(300)
    
    def has_download(self):
        """检查是否有下载文件或链接"""
        return bool(self.book_file) or bool(self.download_link)
    
    def get_download_url(self):
        """获取下载URL，优先返回文件URL，其次是下载链接"""
        if self.book_file and hasattr(self.book_file, 'url'):
            return self.book_file.url
        elif self.download_link:
            return self.download_link
        return None
    
    def get_download_type(self):
        """获取下载类型：file（文件）或 link（链接）"""
        if self.book_file:
            return 'file'
        elif self.download_link:
            return 'link'
        return None


# 作者类
class Author(models.Model):
    # 作者id
    id = models.AutoField(primary_key=True)
    # 作者名字
    name = models.CharField(max_length=32)
    # 所创图书（多对多）
    book = models.ManyToManyField(to='Book')

    # 指定数据表名称（未指定即为默认类名）
    class Meta:
        db_table = "author"


# E-commerce Models for Shopping Cart and Orders

PAYMENT_METHOD_CHOICES = [
    ('credit_card', '信用卡'),
    ('debit_card', '借记卡'),
    ('paypal', 'PayPal'),
    ('alipay', '支付宝'),
    ('wechat_pay', '微信支付'),
    ('bank_transfer', '银行转账'),
    ('cash_on_delivery', '货到付款'),
]

ORDER_STATUS_CHOICES = [
    ('pending', '待处理'),
    ('payment_pending', '待付款'),
    ('paid', '已付款'),
    ('confirmed', '已确认'),
    ('processing', '处理中'),
    ('shipped', '已发货'),
    ('delivered', '已送达'),
    ('cancelled', '已取消'),
    ('refunded', '已退款'),
]

PAYMENT_STATUS_CHOICES = [
    ('pending', '待支付'),
    ('processing', '支付处理中'),
    ('completed', '支付完成'),
    ('failed', '支付失败'),
    ('refunded', '已退款'),
    ('cancelled', '已取消'),
]


# 客户订单模型
class Order(models.Model):
    """Order model for customer purchases - Digital Products Only"""
    order_number = models.CharField(max_length=32, unique=True, verbose_name="订单号")
    customer_name = models.CharField(max_length=100, verbose_name="客户姓名")
    customer_email = models.EmailField(verbose_name="客户邮箱")
    customer_phone = models.CharField(max_length=20, verbose_name="微信/电话号码")
    
    # 国家信息 (仅用于数字产品)
    country = models.CharField(max_length=50, default='China', verbose_name="国家")
      # 订单详情
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES, 
        verbose_name="支付方式"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总金额")
    status = models.CharField(
        max_length=20, 
        choices=ORDER_STATUS_CHOICES, 
        default='pending', 
        verbose_name="订单状态"
    )
    
    # 支付信息
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name="支付状态"
    )
    payment_transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="支付交易号"
    )
    payment_completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="支付完成时间"
    )
    
    customer_notes = models.TextField(blank=True, verbose_name="客户备注")
    admin_notes = models.TextField(blank=True, verbose_name="管理员备注")
      # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = "order"
        ordering = ['-created_at']
        verbose_name = "订单"
        verbose_name_plural = "订单"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate unique order number"""
        import datetime
        now = datetime.datetime.now()
        return f"ORD{now.strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:8].upper()}"
    
    def get_total_items(self):
        """Get total number of items in this order"""
        return sum(item.quantity for item in self.orderitem_set.all())
    
    def mark_as_paid(self, transaction_id=None):
        """Mark order as paid and update payment status"""
        self.payment_status = 'completed'
        self.status = 'paid'
        self.payment_completed_at = timezone.now()
        if transaction_id:
            self.payment_transaction_id = transaction_id
        self.save()
    
    def get_status_color(self):
        """Get bootstrap color class for order status"""
        status_colors = {
            'pending': 'warning',
            'payment_pending': 'info',
            'paid': 'success',
            'confirmed': 'primary',
            'processing': 'info',
            'shipped': 'primary',
            'delivered': 'success',
            'cancelled': 'danger',
            'refunded': 'secondary',
        }
        return status_colors.get(self.status, 'secondary')
    
    def get_payment_status_color(self):
        """Get bootstrap color class for payment status"""
        payment_colors = {
            'pending': 'warning',
            'processing': 'info',
            'completed': 'success',
            'failed': 'danger',
            'refunded': 'secondary',
            'cancelled': 'dark',
        }
        return payment_colors.get(self.payment_status, 'secondary')
    
    def is_payment_window_expired(self):
        """Check if 30-minute payment window has expired for unpaid orders"""
        from datetime import timedelta
        if self.status != 'payment_pending':
            return False
        
        expiration_time = self.created_at + timedelta(minutes=30)
        return timezone.now() > expiration_time
    
    def get_payment_time_remaining(self):
        """Get remaining time to pay in seconds"""
        from datetime import timedelta
        if self.status != 'payment_pending':
            return 0
        
        expiration_time = self.created_at + timedelta(minutes=30)
        remaining = expiration_time - timezone.now()
        return max(0, int(remaining.total_seconds()))
    
    def auto_cancel_if_expired(self):
        """Auto-cancel order if payment window expired"""
        if self.is_payment_window_expired():
            self.status = 'cancelled'
            self.save()
            return True
        return False
    
    def __str__(self):
        return f"订单 {self.order_number} - {self.customer_name}"

# 订单项模型（一个订单包含多本图书）
class OrderItem(models.Model):
    """Individual items within an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="图书")
    quantity = models.PositiveIntegerField(verbose_name="数量")
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="单价")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="小计")
    
    class Meta:
        db_table = "order_item"
        verbose_name = "订单项目"
        verbose_name_plural = "订单项目"
    
    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.book.name} x {self.quantity}"


# 购物车模型（用于多本图书选择）
class CartItem(models.Model):
    """Shopping cart item model"""
    session_key = models.CharField(max_length=40, verbose_name="会话密钥")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="图书")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = "cart_item"
        unique_together = ('session_key', 'book')
        verbose_name = "购物车项目"
        verbose_name_plural = "购物车项目"
    
    def get_total_price(self):
        """Calculate total price for this cart item"""
        return self.book.price * self.quantity
    
    def __str__(self):
        return f"{self.book.name} x {self.quantity}"

# 订单通知模型（用于跟踪支付状态变化）
class OrderNotification(models.Model):
    """Order notification model for tracking payment status changes"""
    NOTIFICATION_TYPES = [
        ('payment_status_change', '支付状态变更'),
        ('order_status_change', '订单状态变更'),
        ('order_created', '订单创建'),
        ('order_cancelled', '订单取消'),
        ('refund_processed', '退款处理'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单", related_name="notifications")
    notification_type = models.CharField(
        max_length=50, 
        choices=NOTIFICATION_TYPES, 
        verbose_name="通知类型"
    )
    message = models.TextField(verbose_name="通知消息")
    details = models.JSONField(blank=True, null=True, verbose_name="详细信息")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        db_table = "order_notification"
        ordering = ['-created_at']
        verbose_name = "订单通知"
        verbose_name_plural = "订单通知"
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.save()
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_notification_type_display()}"

# 创建(同步)数据表命令
# 创建数据库db_book
# python manage.py makemigrations
# python manage.py migrate
