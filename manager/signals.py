"""
Order Management System - Django Signals
Handles database notifications when payments are made
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Order, OrderNotification
import logging

logger = logging.getLogger(__name__)

# Debug print to confirm signals are loaded
print("🔔 Order management signals loaded successfully!")


@receiver(pre_save, sender=Order)
def track_payment_status_change(sender, instance, **kwargs):
    """Track payment status changes before saving"""
    print(f"🔍 Pre-save signal triggered for order: {instance.order_number if hasattr(instance, 'order_number') else 'NEW'}")
    if instance.pk:  # Only for existing orders
        try:
            old_order = Order.objects.get(pk=instance.pk)
            instance._old_payment_status = old_order.payment_status
            print(f"🔍 Old payment status: {old_order.payment_status}, New: {instance.payment_status}")
        except Order.DoesNotExist:
            instance._old_payment_status = None
    else:
        instance._old_payment_status = None


@receiver(post_save, sender=Order)
def handle_payment_status_change(sender, instance, created, **kwargs):
    """Handle payment status changes and send notifications"""
    print(f"💾 Post-save signal triggered for order: {instance.order_number}, created: {created}")
    
    # Skip if this is a new order creation
    if created:
        logger.info(f"New order created: {instance.order_number}")
        print(f"📝 New order created: {instance.order_number}")
        return
    
    # Check if payment status changed
    old_status = getattr(instance, '_old_payment_status', None)
    current_status = instance.payment_status
    
    print(f"🔄 Checking status change: {old_status} -> {current_status}")
    
    if old_status and old_status != current_status:
        logger.info(f"Payment status changed for order {instance.order_number}: {old_status} -> {current_status}")
        print(f"✅ Payment status changed for order {instance.order_number}: {old_status} -> {current_status}")
        
        # Create notification record
        create_payment_notification(instance, old_status, current_status)
        
        # Send email notification if payment is successful
        if current_status == 'paid':
            send_payment_confirmation(instance)
        
        # Handle refund notifications
        elif current_status == 'refunded':
            send_refund_notification(instance)
    else:
        print(f"❌ No payment status change detected or old_status is None")


def create_payment_notification(order, old_status, new_status):
    """Create a notification record in the database"""
    try:
        # Create notification message
        status_messages = {
            ('pending', 'paid'): f"订单 {order.order_number} 支付成功",
            ('pending', 'failed'): f"订单 {order.order_number} 支付失败",
            ('paid', 'refunded'): f"订单 {order.order_number} 已退款",
            ('failed', 'paid'): f"订单 {order.order_number} 重新支付成功",
        }
        
        message = status_messages.get((old_status, new_status), 
                                    f"订单 {order.order_number} 支付状态从 {old_status} 变更为 {new_status}")
        
        # Create notification record
        OrderNotification.objects.create(
            order=order,
            notification_type='payment_status_change',
            message=message,
            details={
                'old_status': old_status,
                'new_status': new_status,
                'order_number': order.order_number,
                'customer_name': order.customer_name,
                'total_amount': str(order.total_amount),
                'timestamp': timezone.now().isoformat()
            }
        )
        
        logger.info(f"Payment notification created for order {order.order_number}")
        
    except Exception as e:
        logger.error(f"Failed to create payment notification for order {order.order_number}: {str(e)}")


def send_payment_confirmation(order):
    """Send payment confirmation email to customer"""
    try:
        if not order.customer_email:
            logger.warning(f"No email address for order {order.order_number}")
            return
        
        subject = f"支付确认 - 订单号: {order.order_number}"
        message = f"""
亲爱的 {order.customer_name}，

您的订单已成功支付！

订单信息：
订单号：{order.order_number}
支付金额：¥{order.total_amount}
支付时间：{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

我们将尽快为您处理订单，感谢您的购买！

此邮件为系统自动发送，请勿回复。
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer_email],
            fail_silently=False
        )
        
        logger.info(f"Payment confirmation email sent for order {order.order_number}")
        
    except Exception as e:
        logger.error(f"Failed to send payment confirmation email for order {order.order_number}: {str(e)}")


def send_refund_notification(order):
    """Send refund notification email to customer"""
    try:
        if not order.customer_email:
            logger.warning(f"No email address for order {order.order_number}")
            return
        
        subject = f"退款通知 - 订单号: {order.order_number}"
        message = f"""
亲爱的 {order.customer_name}，

您的订单退款已处理完成。

订单信息：
订单号：{order.order_number}
退款金额：¥{order.total_amount}
退款时间：{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}

退款将在3-5个工作日内到账，请注意查收。

如有疑问，请联系客服。

此邮件为系统自动发送，请勿回复。
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer_email],
            fail_silently=False
        )
        
        logger.info(f"Refund notification email sent for order {order.order_number}")
        
    except Exception as e:
        logger.error(f"Failed to send refund notification email for order {order.order_number}: {str(e)}")


@receiver(post_save, sender=Order)
def update_order_status_on_payment(sender, instance, created, **kwargs):
    """Automatically update order status when payment is confirmed"""
    
    if not created and instance.payment_status == 'paid' and instance.status == 'pending':
        # Automatically move to processing when payment is confirmed
        Order.objects.filter(pk=instance.pk).update(status='processing')
        logger.info(f"Order {instance.order_number} status automatically updated to processing after payment")
