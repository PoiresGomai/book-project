# 图书管理系统 (Book Management System)

一个基于Django框架开发的图书管理系统，用于管理图书、作者和出版社信息。

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/PoiresGomai/book-project.git)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.1+-green?logo=django)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-5.7+-orange?logo=mysql)](https://www.mysql.com/)

## 🚀 快速开始

### 克隆项目
```bash
git clone https://github.com/PoiresGomai/book-project.git
cd book-project
```

### 环境设置
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate
# 激活虚拟环境 (Linux/Mac)
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 数据库配置
```bash
# 创建MySQL数据库
mysql -u root -p
CREATE DATABASE db_book CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 导入数据库结构
mysql -u root -p db_book < db_book.sql
```

### 运行项目
```bash
# 检查环境配置
python check_requirements.py

# 启动开发服务器
python manage.py runserver
```

### 访问系统
- 🌐 **URL**: http://127.0.0.1:8000/manager/login
- 👤 **用户名**: bhml
- 🔑 **密码**: 123456

## 📋 项目简介

本系统是一个完整的图书管理平台，提供了对图书、作者和出版社的全面管理功能。管理员可以通过系统进行登录，并执行各种管理操作，包括添加、编辑、删除和查看图书、作者及出版社信息。

## ✨ 功能特点

### 👥 用户管理
- 管理员登录认证
- 会话管理
- 安全登出功能

### 🏢 出版社管理
- ➕ 添加新出版社
- ✏️ 编辑出版社信息
- 🗑️ 删除出版社
- 📋 查看所有出版社列表

### 📚 图书管理
- ➕ 添加新图书
- ✏️ 编辑图书信息（名称、价格、库存、销量等）
- 🗑️ 删除图书
- 📋 查看所有图书列表

### ✍️ 作者管理
- ➕ 添加新作者
- ✏️ 编辑作者信息及其关联图书
- 🗑️ 删除作者
- 📋 查看所有作者及其著作列表

## 🛠️ 技术栈

- **🐍 后端**: Django 4.1+
- **🗄️ 数据库**: MySQL 5.7+
- **🎨 前端**: HTML, CSS, JavaScript
- **📱 UI框架**: Bootstrap
- **⚡ 前端库**: jQuery
- **🔗 数据库驱动**: mysqlclient 或 PyMySQL

## 📁 项目结构

```
book_Project/
├── 📁 book_Project/          # 项目配置目录
│   ├── __init__.py
│   ├── settings.py        # 项目设置
│   ├── urls.py            # 主URL配置
│   ├── wsgi.py            # WSGI配置
│   └── asgi.py            # ASGI配置
├── 📁 manager/               # 应用目录
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── 📁 migrations/        # 数据库迁移文件
│   ├── models.py          # 数据模型
│   ├── tests.py
│   ├── urls.py            # 应用URL配置
│   ├── views.py           # 视图函数
│   ├── 📁 static/            # 静态资源
│   │   ├── 📁 css/
│   │   └── 📁 js/
│   └── 📁 templates/         # HTML模板
│       ├── 📁 admin/
│       ├── 📁 author/
│       ├── 📁 book/
│       └── 📁 publisher/
├── manage.py              # Django命令行工具
├── db_book.sql            # 数据库SQL文件
├── requirements.txt       # 依赖文件
├── check_requirements.py  # 环境检查脚本
├── setup_guide.md        # 详细安装指南
└── .gitignore            # Git忽略文件
```

## 🎯 系统要求

### 必需软件
- **Python**: 3.8+ (推荐 3.9+)
- **MySQL**: 5.7+ 或 8.0+
- **pip**: Python包管理器

### 必需Python包
```bash
Django>=4.1.0,<5.0.0
mysqlclient>=2.1.0  # MySQL数据库驱动
# 或者使用 PyMySQL>=1.0.2 作为替代
```

### 可选工具
- **Git**: 用于版本控制
- **虚拟环境**: venv 或 virtualenv (强烈推荐)

## 🗄️ 数据模型 (Data Models)

### Manager (管理员)
- `id`: 主键 (int)
- `number`: 账号 (varchar 32)
- `password`: 密码 (varchar 32) - **⚠️ 注意: 生产环境应使用加密存储**
- `name`: 名字 (varchar 32)

### Publisher (出版社)
- `id`: 主键 (bigint)
- `publisher_name`: 出版社名称 (varchar 32)
- `publisher_address`: 出版社地址 (varchar 32)

### Book (图书)
- `id`: 主键 (int)
- `name`: 图书名称 (varchar 32)
- `price`: 价格 (decimal 5,2)
- `inventory`: 库存数量 (int)
- `sale_num`: 销售数量 (int)
- `publisher`: 外键关联出版社 (bigint)

### Author (作者)
- `id`: 主键 (int)
- `name`: 作者名称 (varchar 32)
- `book`: 多对多关系关联图书 (通过 author_book 表)

## 🛣️ 路由说明 (URL Routes)

### 管理员相关
- `/manager/login` - 管理员登录
- `/manager/logout/` - 退出登录

### 图书相关
- `/manager/book_list/` - 图书列表
- `/manager/add_book/` - 添加图书
- `/manager/edit_book/` - 编辑图书
- `/manager/delete_book/` - 删除图书

### 作者相关
- `/manager/author_list/` - 作者列表
- `/manager/add_author/` - 添加作者
- `/manager/edit_author/` - 编辑作者
- `/manager/delete_author/` - 删除作者

### 出版社相关
- `/manager/publisher_list/` - 出版社列表
- `/manager/add_publisher/` - 添加出版社
- `/manager/edit_publisher/` - 编辑出版社
- `/manager/delete_publisher/` - 删除出版社

## 🚨 故障排除 (Troubleshooting)

### 常见问题

#### 1. MySQL连接错误
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```
**解决方案:**
- 确保MySQL服务正在运行
- 检查settings.py中的数据库配置
- 验证用户名和密码

#### 2. mysqlclient安装失败
```
error: Microsoft Visual C++ 14.0 is required
```
**解决方案:**
- 安装 Microsoft C++ Build Tools
- 或使用 PyMySQL 替代

#### 3. 端口已被占用
```
Error: That port is already in use.
```
**解决方案:**
```bash
# 使用其他端口
python manage.py runserver 8001
```

## 🤝 贡献指南 (Contributing)

1. Fork 此仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

### 开发流程
```bash
# 克隆你的 fork
git clone https://github.com/你的用户名/book-project.git

# 添加上游仓库
git remote add upstream https://github.com/PoiresGomai/book-project.git

# 创建新分支
git checkout -b feature/new-feature

# 提交更改
git add .
git commit -m "描述你的更改"

# 推送到你的 fork
git push origin feature/new-feature
```

## 🔒 安全注意事项

1. **🔐 密码安全**: 当前管理员密码以明文存储，生产环境应实现密码加密
2. **🗄️ 数据库安全**: 为数据库创建专用用户，避免使用root账户
3. **🔑 SECRET_KEY**: 确保Django的SECRET_KEY在生产环境中是唯一且安全的
4. **🚫 DEBUG模式**: 生产环境应设置 `DEBUG = False`

## 🎯 使用说明

1. **登录系统**
   - 使用管理员账号和密码登录系统

2. **出版社管理**
   - 添加、编辑、删除、查看出版社信息

3. **图书管理**
   - 添加、编辑、删除、查看图书信息

4. **作者管理**
   - 添加、编辑、删除、查看作者信息及其著作

5. **退出系统**
   - 点击退出按钮安全退出系统

## 📞 联系方式

- **GitHub**: [PoiresGomai](https://github.com/PoiresGomai)
- **项目仓库**: [book-project](https://github.com/PoiresGomai/book-project.git)

## 📄 许可证 (License)

此项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件

---

⭐ 如果这个项目对你有帮助，请给它一个 star！

