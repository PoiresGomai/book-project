from django.urls import path, re_path
from manager import views

# manager中转路由
urlpatterns = [
    # 指定跳转 - Default redirect to login
    re_path(r'^$', views.index),

    # =========================管理员登录========================
    path("login/", views.manager_login, name='manager_login'),
    path("logout/", views.manager_logout, name='manager_logout'),

    # =========================出版社========================
    path("add_publisher/", views.add_publisher, name='add_publisher'),
    path("publisher_list/", views.publisher_list, name='publisher_list'),
    path("edit_publisher/", views.edit_publisher, name='edit_publisher'),
    path("delete_publisher/", views.delete_publisher, name='delete_publisher'),

    # =========================图书 ========================
    path("add_book/", views.add_book, name='add_book'),
    path("book_list/", views.book_list, name='book_list'),
    path("edit_book/", views.edit_book, name='edit_book'),
    path("delete_book/", views.delete_book, name='delete_book'),

    # =========================作家 ========================
    path("add_author/", views.add_author, name='add_author'),
    path("author_list/", views.author_list, name='author_list'),
    path("edit_author/", views.edit_author, name='edit_author'),
    path("delete_author/", views.delete_author, name='delete_author'),

    # =========================Public Interface URLs========================
    path('public/', views.public_home, name='public_home'),
    path('public/books/', views.public_books, name='public_books'),
    path('public/books/<int:book_id>/', views.public_book_detail, name='public_book_detail'),
    path('public/authors/', views.public_authors, name='public_authors'),
    path('public/authors/<int:author_id>/', views.public_author_detail, name='public_author_detail'),
    path('public/publishers/', views.public_publishers, name='public_publishers'),
    path('public/publishers/<int:publisher_id>/', views.public_publisher_detail, name='public_publisher_detail'),
]
