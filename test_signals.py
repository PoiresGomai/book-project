"""
Test script to simulate payment status changes and verify signal functionality
"""

import os
import sys
import django
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_Project.settings')
django.setup()

from manager.models import Order, OrderNotification


def test_payment_signals():
    """Test payment status change signals"""
    print("Testing payment status change signals...")
    
    # Get first pending order
    pending_orders = Order.objects.filter(payment_status='pending')
    
    if not pending_orders.exists():
        print("No pending orders found. Creating a test order...")
        # Create a test order for signal testing
        from manager.models import Book
        book = Book.objects.first()
        if book:
            test_order = Order.objects.create(
                customer_name="测试用户",
                customer_email="test@example.com",
                customer_phone="13800000000",
                shipping_address="测试地址",
                shipping_city="测试城市",
                shipping_state="测试省份",
                payment_method="alipay",
                status="pending",
                payment_status="pending",
                total_amount=100.00
            )
            print(f"Created test order: {test_order.order_number}")
        else:
            print("No books found. Cannot create test order.")
            return
    else:
        test_order = pending_orders.first()
        print(f"Using existing order: {test_order.order_number}")
    
    print(f"Current payment status: {test_order.payment_status}")
    print(f"Current order status: {test_order.status}")
    
    # Test payment status change from pending to paid
    print("\n1. Testing payment status change: pending -> paid")
    old_notification_count = OrderNotification.objects.filter(order=test_order).count()
    
    test_order.payment_status = 'paid'
    test_order.save()
    
    new_notification_count = OrderNotification.objects.filter(order=test_order).count()
    
    print(f"Notifications before: {old_notification_count}")
    print(f"Notifications after: {new_notification_count}")
    
    if new_notification_count > old_notification_count:
        latest_notification = OrderNotification.objects.filter(order=test_order).first()
        print(f"✅ Signal worked! Created notification: {latest_notification.message}")
        print(f"   Notification type: {latest_notification.notification_type}")
        print(f"   Details: {latest_notification.details}")
    else:
        print("❌ Signal may not be working - no new notification created")
    
    # Test refund
    print("\n2. Testing payment status change: paid -> refunded")
    old_notification_count = OrderNotification.objects.filter(order=test_order).count()
    
    test_order.payment_status = 'refunded'
    test_order.save()
    
    new_notification_count = OrderNotification.objects.filter(order=test_order).count()
    
    print(f"Notifications before: {old_notification_count}")
    print(f"Notifications after: {new_notification_count}")
    
    if new_notification_count > old_notification_count:
        latest_notification = OrderNotification.objects.filter(order=test_order).first()
        print(f"✅ Refund signal worked! Created notification: {latest_notification.message}")
    else:
        print("❌ Refund signal may not be working - no new notification created")
    
    # Show all notifications for this order
    print(f"\n3. All notifications for order {test_order.order_number}:")
    notifications = OrderNotification.objects.filter(order=test_order)
    for i, notification in enumerate(notifications, 1):
        print(f"   {i}. {notification.message} ({notification.created_at.strftime('%Y-%m-%d %H:%M:%S')})")
    
    print(f"\nTotal notifications for this order: {notifications.count()}")


if __name__ == "__main__":
    test_payment_signals()
