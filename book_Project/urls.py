from django.urls import path, include

# 主路由（进入各个模块的入口）
urlpatterns = [
    path("manager/", include("manager.urls"))
]
