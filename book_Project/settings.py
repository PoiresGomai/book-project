import os

# 在项目内部构建路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 安全警告：对生产中使用的密钥保密！所有Django实例之间都是唯一的
SECRET_KEY = 'a(h=tp9w#%3_rvd)a_hedu4vaeku9n)5ij(ouaa01&vbvd*5we'

# 调试模式，如果项目没有部署到远程服务器，且DEBUG = True(线下模式，允许调试)
DEBUG = True

# 设置允许哪些主机访问我们的django后台站点，
# 如果项目上线部署到远程服务器，那就必须设置allow_host为本地的ipv4地址
# (设置为"*"也可以，但是不安全)，否则本地是无法访问远程的django站点
ALLOWED_HOSTS = ['*']


# 应用程序定义
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'manager.apps.ManagerConfig'
    # 新加入的程序模块放这里
]

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 根URL配置
ROOT_URLCONF = 'book_Project.urls'
# ROOT_URLCONF = 'manager.urls'

# 模板（前端页面）
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_应用程序
WSGI_APPLICATION = 'book_Project.wsgi.application'


# 数据库配置
# Database configuration for the book management system
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_book',
        'USER': 'bookuser',                    # Use dedicated user
        'PASSWORD': 'BookProject123!',        # Use the password you set
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'autocommit': True,
        },
    }
}

# For production, use environment variables:
# 'USER': os.environ.get('DB_USER', 'bookuser'),
# 'PASSWORD': os.environ.get('DB_PASSWORD', 'BookProject123!'),


# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 国际化配置
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# 静态文件地址 (存放前段所需的CSS, JavaScript, Images等文件)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
