from django.urls import path, re_path
from manager import views

# manager中转路由
app_name = 'manager'

urlpatterns = [
    # 指定跳转 - Default redirect to login
    re_path(r'^$', views.index),

    # =========================管理员登录========================
    path("login/", views.manager_login, name='manager_login'),
    path("logout/", views.manager_logout, name='manager_logout'),

    # =========================Dashboard and analytics========================
    path("dashboard/", views.manager_dashboard, name='manager_dashboard'),
    path('dashboard/analytics/', views.dashboard_analytics_api, name='dashboard_analytics_api'),

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
    # =========================E-commerce URLs========================
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/count/', views.get_cart_count, name='get_cart_count'),
    path('buy-now/<int:book_id>/', views.buy_now, name='buy_now'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    path('track-order/', views.track_order, name='track_order'),
    path('download/<int:order_id>/<int:book_id>/', views.download_book, name='download_book'),

    # =========================API Endpoints for Order Actions========================
    path('api/cancel-order/', views.api_cancel_order, name='api_cancel_order'),
    path('api/confirm-payment/', views.api_confirm_payment, name='api_confirm_payment'),

    # =========================Order Management URLs========================
    path("order_list/", views.order_list, name='order_list'),
    path("order_detail/<int:order_id>/", views.order_detail, name='order_detail'),
    path("update_order_status/", views.update_order_status, name='update_order_status'),
    path("update_payment_status/", views.update_payment_status, name='update_payment_status'),
    path("delete_order/<int:order_id>/", views.delete_order, name='delete_order'),
    path("export_orders/", views.export_orders, name='export_orders'),
]
