# Generated by Django 5.2 on 2025-05-27 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(blank=True, help_text='上传图书封面图片', null=True, upload_to='book_covers/', verbose_name='图书封面'),
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, help_text='图书详细描述信息', null=True, verbose_name='图书描述'),
        ),
    ]
