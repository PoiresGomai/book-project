from django.shortcuts import render, redirect
from manager import models


# 方法实现（数据库操作和页面跳转）
# ====================   默认跳转  ===========================
def index(request):
    return redirect("/manager/login")


# ====================   管理员登录  ===========================
def manager_login(request):
    # 直接访问（get请求），原地跳转
    if request.method == "GET":
        return render(request, "admin/admin.html")
    # 提交表单请求（POST）
    if request.method == "POST":
        # 1.获取请求参数
        number = request.POST.get("number")
        password = request.POST.get("password")
        # 2.将数据保存到数据库中（insert）
        manager = models.Manager.objects.filter(number=number, password=password)
        if manager.exists():
            name = manager.first().name
            request.session["name"] = name
            # 获取图书信息(select *)
            book_obj_list = models.Book.objects.all()
            # 将数据渲染到页面上
            return render(request, 'book/book_list.html', {'book_obj_list': book_obj_list, "name": name})
        return redirect("/manager/login")
        # 3.重添加成功，返回出版社列表


# ====================   一、出版社模块  ===========================
# 01添加出版社
def add_publisher(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 直接访问（get请求），跳转界面
    if request.method == "GET":
        return render(request, 'publisher/add_publisher.html', {"name": request.session["name"]})
    # 提交表单请求（POST）,处理数据库,跳转到列表页面
    if request.method == "POST":
        # 1.获取请求参数
        publisher_name = request.POST.get("publisher_name")
        publisher_address = request.POST.get("publisher_address")
        # 2.将数据保存到数据库中（insert）
        models.Publisher.objects.create(
            publisher_name=publisher_name,
            publisher_address=publisher_address,
        )
        # 3.重添加成功，返回出版社列表
        return redirect("/manager/publisher_list")


# 02查询所有出版社信息
def publisher_list(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 查询数据库中的所以信息（select * from）
    publisher_list = models.Publisher.objects.all()
    # 跳转到publisher_list页面，传入publisher_list数据
    return render(request, "publisher/publisher_list.html",
                  {"publisher_obj_list": publisher_list, "name": request.session["name"]})


# 03修改出版社信息
def edit_publisher(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 1获取到的是表单提交过来的内容（POST），获取对应的值
    if request.method == "POST":
        id = request.POST.get('id')
        publisher_name = request.POST.get("publisher_name")
        publisher_address = request.POST.get("publisher_address")
        # 2根据id去数据库查找对象（where id = id）
        publisher_obj = models.Publisher.objects.get(id=id)
        # 3修改
        publisher_obj.publisher_name = publisher_name
        publisher_obj.publisher_address = publisher_address
        # 04更新数据库（update）
        publisher_obj.save()
        # 4重定向到出版社列表
        return redirect('/manager/publisher_list/')
    # get请求跳转界面（获取原始数据）
    else:
        # 1获取id
        id = request.GET.get('id')
        # 2去数据库中查找相应的数据
        publisher_obj = models.Publisher.objects.get(id=id)
        publisher_obj_list = models.Publisher.objects.all()
        # 3返回页面
        return render(request, "publisher/edit_publisher.html",
                      {"publisher_obj": publisher_obj, "publisher_obj_list": publisher_obj_list,
                       "name": request.session["name"]})


# 04删除出版社信息
def delete_publisher(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 1获取要删除图书的id
    id = request.GET.get('id')
    # 2根据id删除数据库中的记录（delete）
    models.Publisher.objects.filter(id=id).delete()
    return redirect('/manager/publisher_list')


# ============================  二、图书模块操作   ===============================
# 01获取所有图书信息
def book_list(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 1获取图书信息(select *)
    book_obj_list = models.Book.objects.all()
    # 2将数据渲染到页面上
    return render(request, 'book/book_list.html', {'book_obj_list': book_obj_list, "name": request.session["name"]})


# 02添加图书
def add_book(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    if request.method == 'POST':
        # 1获取表单提价过来的内容
        name = request.POST.get('name')
        price = request.POST.get('price')
        inventory = request.POST.get('inventory')
        sale_num = request.POST.get('sale_num')
        publisher_id = request.POST.get('publisher_id')
        # 2保存到数据库（insert）
        models.Book.objects.create(name=name, price=price, inventory=inventory, sale_num=sale_num,
                                   publisher_id=publisher_id)
        # 3重定向到图书列表页面
        return redirect('/manager/book_list/')
    else:
        # 1获取所有的出版社（点击添加图书按钮时，得到所有出版社信息供用户选择）
        publisher_obj_list = models.Publisher.objects.all()
        return render(request, 'book/add_book.html',
                      {"publisher_obj_list": publisher_obj_list, "name": request.session["name"]})


# 03修改图书信息
def edit_book(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 点击修改图书（获取要修改图书的原本信息）
    if request.method == 'GET':
        id = request.GET.get('id')
        book_obj = models.Book.objects.get(id=id)
        publisher_obj_list = models.Publisher.objects.all()
        book_obj_list = models.Book.objects.all()
        return render(request, "book/edit_book.html",
                      {"book_obj": book_obj, "book_obj_list": book_obj_list, "publisher_obj_list": publisher_obj_list,
                       "name": request.session["name"]})
    # 修改图书信息（POST表单）
    else:
        id = request.POST.get('id')
        name = request.POST.get('name')
        inventory = request.POST.get('inventory')
        price = request.POST.get('price')
        sale_num = request.POST.get('sale_num')
        publisher_id = request.POST.get('publisher_id')
        # 数据库中更新图书信息
        models.Book.objects.filter(id=id).update(name=name, inventory=inventory, price=price, sale_num=sale_num,
                                                 publisher_id=publisher_id)
        return redirect("/manager/book_list/")


# 04删除图书
def delete_book(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    id = request.GET.get('id')
    models.Book.objects.filter(id=id).delete()
    return redirect('/manager/book_list')


# ================================  三、作者操作模块  =============================
# 01作者列表
def author_list(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 列表存储作者和图书（一个作者可能有多本书）
    ret_list = []
    # 获取作者列表信息
    author_obj_list = models.Author.objects.all()
    for author_obj in author_obj_list:
        book_obj_list = author_obj.book.all()
        # 定义字典存储
        ret_dic = {'author_obj': author_obj, 'book_list': book_obj_list}
        ret_list.append(ret_dic)
    return render(request, 'author/author_list.html', {'ret_list': ret_list, "name": request.session["name"]})


# 02添加作家
def add_author(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 添加作家页面
    if request.method == 'GET':
        # 1获取所有的图书
        book_obj_list = models.Book.objects.all()
        # 2返回页面
        return render(request, 'author/add_author.html',
                      {'book_obj_list': book_obj_list, "name": request.session["name"]})
    # 数据库处理添加
    else:
        # 1.获取表单提交过来的数据
        name = request.POST.get('name')
        book_ids = request.POST.getlist('books')
        # 2 保存数据库
        author_obj = models.Author.objects.create(name=name)  # 创建对象
        author_obj.book.set(book_ids)  # 设置关系
        # 3 重定向到列表页面
        return redirect('/manager/author_list/')


# 03修改作者信息
def edit_author(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 跳转修改界面
    if request.method == 'GET':
        id = request.GET.get('id')
        author_obj = models.Author.objects.get(id=id)
        book_obj_list = models.Book.objects.all()
        return render(request, 'author/edit_author.html',
                      {'author_obj': author_obj, 'book_obj_list': book_obj_list, "name": request.session["name"]})
    # 提交修改表单
    else:
        id = request.POST.get('id')
        name = request.POST.get('name')
        book_ids = request.POST.getlist('books')
        # 找到第一个作家id即可
        author_obj = models.Author.objects.filter(id=id).first()
        author_obj.name = name
        author_obj.book.set(book_ids)
        author_obj.save()
        return redirect('/manager/author_list/')


# 04 删除作者
def delete_author(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 1获取id
    id = request.GET.get('id')
    # 2删除作者
    models.Author.objects.filter(id=id).delete()
    # 3重定向作者列表
    return redirect('/admin/author_list')


# ==================================其他功能===========================
# 退出系统
def logout(request):
    request.session.clear()
    return render(request, "admin/admin.html")
