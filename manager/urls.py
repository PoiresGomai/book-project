from django.urls import path,re_path
from manager import views

# manager中转路由
urlpatterns = [
    # 指定跳转
    re_path(r'^$', views.index),

    # =========================管理员登录========================
    path("login/", views.manager_login),
    # =========================出版社========================
    # 添加出版社
    path("add_publisher/", views.add_publisher),
    # 查询所有出版社信息
    path("publisher_list/", views.publisher_list),
    # 修改出版社信息
    path("edit_publisher/", views.edit_publisher),
    # 删除出版社
    path("delete_publisher/", views.delete_publisher),
    # =========================图书 ========================
    # 添加图书
    path("add_book/", views.add_book),
    # 查询所有图书
    path("book_list/", views.book_list),
    # 修改图书
    path("edit_book/", views.edit_book),
    # 删除图书
    path("delete_book/", views.delete_book),
    # =========================作家 ========================
    # 添加作家
    path("add_author/", views.add_author),
    # 查找所有作家
    path("author_list/", views.author_list),
    # 修改作家信息
    path("edit_author/", views.edit_author),
    # 删除作家
    path("delete_author/", views.delete_author),

    # =========================其他功能========================
    path("logout/", views.logout)
]
