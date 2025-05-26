from django.db import models


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

# 创建(同步)数据表命令
# 创建数据库db_book
# python manage.py makemigrations
# python manage.py migrate
