# Generated by Django 5.2 on 2025-05-28 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_order_orderitem_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='admin_notes',
            field=models.TextField(blank=True, verbose_name='管理员备注'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_completed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='支付完成时间'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('pending', '待支付'), ('processing', '支付处理中'), ('completed', '支付完成'), ('failed', '支付失败'), ('refunded', '已退款'), ('cancelled', '已取消')], default='pending', max_length=20, verbose_name='支付状态'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='支付交易号'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', '待处理'), ('payment_pending', '待付款'), ('paid', '已付款'), ('confirmed', '已确认'), ('processing', '处理中'), ('shipped', '已发货'), ('delivered', '已送达'), ('cancelled', '已取消'), ('refunded', '已退款')], default='pending', max_length=20, verbose_name='订单状态'),
        ),
        migrations.CreateModel(
            name='OrderNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('payment_status_change', '支付状态变更'), ('order_status_change', '订单状态变更'), ('order_created', '订单创建'), ('order_cancelled', '订单取消'), ('refund_processed', '退款处理')], max_length=50, verbose_name='通知类型')),
                ('message', models.TextField(verbose_name='通知消息')),
                ('details', models.JSONField(blank=True, null=True, verbose_name='详细信息')),
                ('is_read', models.BooleanField(default=False, verbose_name='是否已读')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='manager.order', verbose_name='订单')),
            ],
            options={
                'verbose_name': '订单通知',
                'verbose_name_plural': '订单通知',
                'db_table': 'order_notification',
                'ordering': ['-created_at'],
            },
        ),
    ]
