from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_http_methods, require_POST
from django.db.models import Sum, Avg
from decimal import Decimal
import uuid
import json
from . import models


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


# ====================   管理员登出  ===========================
def manager_logout(request):
    """Manager logout function - renamed from logout to avoid conflicts"""
    request.session.clear()
    return render(request, "admin/admin.html")


# Keep the old logout function for backward compatibility
def logout(request):
    """Legacy logout function - redirects to manager_logout"""
    return manager_logout(request)


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
        # 1获取表单提交过来的内容
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        inventory = request.POST.get('inventory')
        sale_num = request.POST.get('sale_num')
        publisher_id = request.POST.get('publisher_id')
        cover_image = request.FILES.get('cover_image')
        
        # 2保存到数据库（insert）
        book = models.Book.objects.create(
            name=name, 
            description=description,
            price=price, 
            inventory=inventory, 
            sale_num=sale_num,
            publisher_id=publisher_id
        )
        
        # Handle image upload
        if cover_image:
            book.cover_image = cover_image
            book.save()
        
        # 3重定向到图书列表页面
        return redirect('/manager/book_list/')
    else:
        # 1获取所有的出版社（点击添加图书按钮时，得到所有出版社信息供用户选择）
        publisher_obj_list = models.Publisher.objects.all()
        # 2返回html页面（在页面中遍历出版社对象列表）
        return render(request, 'book/add_book.html', locals())


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
        description = request.POST.get('description', '')
        inventory = request.POST.get('inventory')
        price = request.POST.get('price')
        sale_num = request.POST.get('sale_num')
        publisher_id = request.POST.get('publisher_id')
        cover_image = request.FILES.get('cover_image')
        
        # 获取要更新的图书对象
        book = models.Book.objects.get(id=id)
        
        # 数据库中更新图书信息
        book.name = name
        book.description = description
        book.inventory = inventory
        book.price = price
        book.sale_num = sale_num
        book.publisher_id = publisher_id
        
        # Handle image upload
        if cover_image:
            book.cover_image = cover_image
            
        book.save()
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
        try:
            author_obj = models.Author.objects.get(id=id)
            book_obj_list = models.Book.objects.all()
            # Get currently associated books
            current_books = author_obj.book.all()
            return render(request, 'author/edit_author.html',
                          {
                              'author_obj': author_obj, 
                              'book_obj_list': book_obj_list,
                              'current_books': current_books,
                              "name": request.session["name"]
                          })
        except models.Author.DoesNotExist:
            return redirect('/manager/author_list/')
    
    # 提交修改表单
    else:
        id = request.POST.get('id')
        name = request.POST.get('name')
        book_ids = request.POST.getlist('books')  # Get list of selected book IDs
        
        try:
            # 找到作者对象
            author_obj = models.Author.objects.filter(id=id).first()
            if author_obj:
                author_obj.name = name
                # Clear existing relationships and set new ones
                author_obj.book.set(book_ids)  # This handles the many-to-many relationship
                author_obj.save()
            return redirect('/manager/author_list/')
        except Exception as e:
            # Handle any errors gracefully
            return redirect(f'/manager/edit_author/?id={id}')

# 04 删除作者
def delete_author(request):
    # 登录判断
    if "name" not in request.session:
        return redirect("/manager/login")
    # 1获取id
    id = request.GET.get('id')
    # 2删除作者
    models.Author.objects.filter(id=id).delete()
    # 3重定向作者列表 - Fixed URL
    return redirect('/manager/author_list')


# ====================   PUBLIC USER INTERFACE  ===========================

def public_home(request):
    """Public homepage with book statistics and featured content"""
    book_count = models.Book.objects.count()
    author_count = models.Author.objects.count()
    publisher_count = models.Publisher.objects.count()
    
    # Get featured books (top 6 by sales)
    featured_books = models.Book.objects.select_related('publisher').order_by('-sale_num')[:6]
    
    # Recent books (last 8 added)
    recent_books = models.Book.objects.select_related('publisher').order_by('-id')[:8]
    
    context = {
        'book_count': book_count,
        'author_count': author_count,
        'publisher_count': publisher_count,
        'featured_books': featured_books,
        'recent_books': recent_books,
    }
    return render(request, 'public/home.html', context)

def public_books(request):
    """Public book listing with search and pagination"""
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')
    
    books = models.Book.objects.select_related('publisher')
    
    if search_query:
        books = books.filter(name__icontains=search_query)
    
    # Sorting options
    if sort_by == 'price_low':
        books = books.order_by('price')
    elif sort_by == 'price_high':
        books = books.order_by('-price')
    elif sort_by == 'popular':
        books = books.order_by('-sale_num')
    else:
        books = books.order_by('name')
    
    context = {
        'books': books,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'public/books.html', context)

def public_book_detail(request, book_id):
    """Public book detail view"""
    book = get_object_or_404(models.Book.objects.select_related('publisher'), id=book_id)
    authors = book.author_set.all()
    
    # Related books by same publisher
    related_books = models.Book.objects.filter(
        publisher=book.publisher
    ).exclude(id=book.id)[:4]
    
    context = {
        'book': book,
        'authors': authors,
        'related_books': related_books,
    }
    return render(request, 'public/book_detail.html', context)

def public_authors(request):
    """Public authors listing"""
    search_query = request.GET.get('search', '')
    
    # Fix: Use 'book' instead of 'book_set' for ManyToMany relationship
    authors = models.Author.objects.prefetch_related('book').all()
    
    if search_query:
        authors = authors.filter(name__icontains=search_query)
    
    authors = authors.order_by('name')
    
    context = {
        'authors': authors,
        'search_query': search_query,
    }
    return render(request, 'public/authors.html', context)

def public_author_detail(request, author_id):
    """Public author detail view"""
    author = get_object_or_404(models.Author, id=author_id)
    # Fix: Use 'book' instead of 'book_set' for ManyToMany relationship
    books = author.book.select_related('publisher').all()
    
    # Calculate statistics
    total_sales = sum(book.sale_num for book in books)
    total_inventory = sum(book.inventory for book in books)
    avg_price = sum(book.price for book in books) / len(books) if books else 0
    
    context = {
        'author': author,
        'books': books,
        'total_sales': total_sales,
        'total_inventory': total_inventory,
        'avg_price': avg_price,
    }
    return render(request, 'public/author_detail.html', context)

def public_publishers(request):
    """Public publishers listing"""
    search_query = request.GET.get('search', '')
    
    publishers = models.Publisher.objects.all()
    
    if search_query:
        publishers = publishers.filter(publisher_name__icontains=search_query)
    
    publishers = publishers.order_by('publisher_name')
    
    context = {
        'publishers': publishers,
        'search_query': search_query,
    }
    return render(request, 'public/publishers.html', context)

def public_publisher_detail(request, publisher_id):
    """Public publisher detail view"""
    publisher = get_object_or_404(models.Publisher, id=publisher_id)
    books = models.Book.objects.filter(publisher=publisher).order_by('name')
    
    # Calculate statistics
    total_sales = sum(book.sale_num for book in books)
    total_inventory = sum(book.inventory for book in books)
    avg_price = sum(book.price for book in books) / len(books) if books else 0
    
    # Count unique authors
    author_count = models.Author.objects.filter(book__publisher=publisher).distinct().count()
    
    context = {
        'publisher': publisher,
        'books': books,
        'total_sales': total_sales,
        'total_inventory': total_inventory,
        'avg_price': avg_price,
        'author_count': author_count,
    }
    return render(request, 'public/publisher_detail.html', context)

# ==================== E-COMMERCE FUNCTIONALITY ====================

def get_session_key(request):
    """Get or create session key for cart functionality"""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

@require_POST
def add_to_cart(request, book_id):
    """Add book to shopping cart"""
    try:
        book = get_object_or_404(models.Book, id=book_id)
        quantity = int(request.POST.get('quantity', 1))
        session_key = get_session_key(request)
        
        # Validate quantity
        if quantity > book.inventory:
            return JsonResponse({
                'success': False,
                'message': f'库存不足！当前库存：{book.inventory}本'
            })
        
        # Get or create cart item
        cart_item, created = models.CartItem.objects.get_or_create(
            session_key=session_key,
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update existing cart item
            new_quantity = cart_item.quantity + quantity
            if new_quantity > book.inventory:
                return JsonResponse({
                    'success': False,
                    'message': f'库存不足！当前库存：{book.inventory}本，购物车中已有：{cart_item.quantity}本'
                })
            cart_item.quantity = new_quantity
            cart_item.save()
        
        # Get total cart count
        cart_count = models.CartItem.objects.filter(session_key=session_key).count()
        
        return JsonResponse({
            'success': True,
            'message': f'已将《{book.name}》添加到购物车',
            'cart_count': cart_count,
            'item_quantity': cart_item.quantity
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': '添加到购物车失败，请重试'
        })

def view_cart(request):
    """Display shopping cart"""
    session_key = get_session_key(request)
    cart_items = models.CartItem.objects.filter(session_key=session_key).select_related('book')
    
    total_amount = sum(item.get_total_price() for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'total_items': total_items,
    }
    
    return render(request, 'public/cart.html', context)

@require_POST
def update_cart(request):
    """Update cart item quantities via AJAX"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        session_key = get_session_key(request)
        
        cart_item = get_object_or_404(models.CartItem, id=item_id, session_key=session_key)
        
        # Validate quantity
        if quantity > cart_item.book.inventory:
            return JsonResponse({
                'success': False,
                'message': f'库存不足！最大可购买：{cart_item.book.inventory}本'
            })
        
        if quantity <= 0:
            cart_item.delete()
            message = f'已从购物车移除《{cart_item.book.name}》'
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = f'已更新《{cart_item.book.name}》数量为：{quantity}本'
        
        # Recalculate totals
        cart_items = models.CartItem.objects.filter(session_key=session_key)
        total_amount = sum(item.get_total_price() for item in cart_items)
        total_items = sum(item.quantity for item in cart_items)
        
        return JsonResponse({
            'success': True,
            'message': message,
            'item_total': float(cart_item.get_total_price()) if quantity > 0 else 0,
            'cart_total': float(total_amount),
            'total_items': total_items
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': '更新购物车失败'
        })

def remove_from_cart(request, item_id):
    """Remove item from cart"""
    session_key = get_session_key(request)
    cart_item = get_object_or_404(models.CartItem, id=item_id, session_key=session_key)
    book_name = cart_item.book.name
    cart_item.delete()
    
    messages.success(request, f'已从购物车移除《{book_name}》')
    return redirect('view_cart')

def get_cart_count(request):
    """Get cart item count for AJAX requests"""
    session_key = get_session_key(request)
    cart_count = models.CartItem.objects.filter(session_key=session_key).count()
    return JsonResponse({'cart_count': cart_count})

@require_POST
def buy_now(request, book_id):
    """Direct purchase without cart"""
    try:
        book = get_object_or_404(models.Book, id=book_id)
        quantity = int(request.POST.get('quantity', 1))
        session_key = get_session_key(request)
        
        # Validate quantity
        if quantity > book.inventory:
            messages.error(request, f'库存不足！当前库存：{book.inventory}本')
            return redirect('public_book_detail', book_id=book_id)
        
        # Clear any existing cart items for this session (optional)
        models.CartItem.objects.filter(session_key=session_key).delete()
        
        # Add to cart for checkout
        models.CartItem.objects.create(
            session_key=session_key,
            book=book,
            quantity=quantity
        )
        
        # Redirect to checkout
        return redirect('checkout')
        
    except Exception as e:
        messages.error(request, '购买失败，请重试')
        return redirect('public_book_detail', book_id=book_id)

def checkout(request):
    """Checkout process"""
    session_key = get_session_key(request)
    cart_items = models.CartItem.objects.filter(session_key=session_key).select_related('book')
    
    if not cart_items.exists():
        messages.warning(request, '购物车为空，请先添加商品')
        return redirect('public_books')
    
    if request.method == 'POST':
        try:
            # Create order
            order = models.Order.objects.create(
                customer_name=request.POST.get('customer_name'),
                customer_email=request.POST.get('customer_email'),
                customer_phone=request.POST.get('customer_phone'),
                shipping_address=request.POST.get('shipping_address'),
                shipping_city=request.POST.get('shipping_city', ''),
                shipping_state=request.POST.get('shipping_state', ''),
                shipping_country=request.POST.get('shipping_country', '中国'),
                shipping_postal_code=request.POST.get('shipping_postal_code', ''),
                payment_method=request.POST.get('payment_method'),
                total_amount=sum(item.get_total_price() for item in cart_items),
                customer_notes=request.POST.get('customer_notes', '')
            )
            
            # Create order items and update inventory
            for cart_item in cart_items:
                models.OrderItem.objects.create(
                    order=order,
                    book=cart_item.book,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.book.price,
                    total_price=cart_item.get_total_price()
                )
                
                # Update book inventory and sales
                book = cart_item.book
                book.inventory -= cart_item.quantity
                book.sale_num += cart_item.quantity
                book.save()
            
            # Clear cart
            cart_items.delete()
            
            return redirect('order_confirmation', order_number=order.order_number)
            
        except Exception as e:
            messages.error(request, '订单创建失败，请重试')
    
    total_amount = sum(item.get_total_price() for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'total_items': total_items,
        'payment_methods': models.PAYMENT_METHOD_CHOICES,
    }
    
    return render(request, 'public/checkout.html', context)

def order_confirmation(request, order_number):
    """Order confirmation page"""
    order = get_object_or_404(models.Order, order_number=order_number)
    order_items = models.OrderItem.objects.filter(order=order).select_related('book')
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    
    return render(request, 'public/order_confirmation.html', context)

def track_order(request):
    """Order tracking page"""
    order = None
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        try:
            order = models.Order.objects.get(order_number=order_number)
        except models.Order.DoesNotExist:
            messages.error(request, '订单号不存在')
    
    context = {'order': order}
    return render(request, 'public/track_order.html', context)
