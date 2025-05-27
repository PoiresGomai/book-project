"""
Generate static HTML files from Django templates for Netlify deployment
"""
import os
import django
from django.conf import settings
from django.template.loader import render_to_string
from django.test import RequestFactory
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_Project.settings')
django.setup()

from manager.models import Book, Author, Publisher, Manager

def create_static_files():
    """Generate static HTML files"""
    
    # Create static build directory
    static_dir = 'static_build'
    public_dir = os.path.join(static_dir, 'public')
    os.makedirs(public_dir, exist_ok=True)
    
    # Create request factory for context
    factory = RequestFactory()
    
    # Get data from database (with fallback for empty DB)
    try:
        books = list(Book.objects.all()[:20])  # Limit for static generation
        authors = list(Author.objects.all()[:20])
        publishers = list(Publisher.objects.all()[:20])
        
        # Statistics
        book_count = Book.objects.count()
        author_count = Author.objects.count()
        publisher_count = Publisher.objects.count()
        
        # Featured and recent books
        featured_books = Book.objects.order_by('-sale_num')[:6]
        recent_books = Book.objects.order_by('-id')[:8]
        
    except Exception as e:
        print(f"Database error: {e}")
        # Fallback data
        books, authors, publishers = [], [], []
        book_count = author_count = publisher_count = 0
        featured_books = recent_books = []
    
    # Generate home page
    home_context = {
        'book_count': book_count,
        'author_count': author_count,
        'publisher_count': publisher_count,
        'featured_books': featured_books,
        'recent_books': recent_books,
    }
    
    # Create a simple base template context
    base_context = {
        'request': factory.get('/public/'),
    }
    
    # Generate static HTML content (simplified without full template inheritance)
    home_html = f"""
<!DOCTYPE html>
<html lang="zh-hans">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>首页 - 图书管理系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }}
        .hero-section {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 100px 0; }}
        .btn-primary-modern {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; padding: 12px 30px; border-radius: 25px; }}
        .stats-card {{ background: white; padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0 5px 20px rgba(0,0,0,0.1); margin-bottom: 30px; }}
        .card-modern {{ background: white; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border: none; }}
        .price-tag {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/public/">
                <i class="fas fa-book-open"></i> 图书管理系统
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/public/">首页</a>
                <a class="nav-link" href="books.html">图书</a>
                <a class="nav-link" href="authors.html">作者</a>
                <a class="nav-link" href="publishers.html">出版社</a>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6">
                    <h1 class="display-4 fw-bold mb-4">欢迎来到图书管理系统</h1>
                    <p class="lead mb-4">探索丰富的图书资源，发现知识的海洋。我们为您提供最全面的图书信息查询和浏览服务。</p>
                    <div class="d-flex gap-3 flex-wrap">
                        <a href="books.html" class="btn btn-primary-modern btn-modern">
                            <i class="fas fa-search"></i> 浏览图书
                        </a>
                        <a href="authors.html" class="btn btn-outline-light btn-modern">
                            <i class="fas fa-users"></i> 查看作者
                        </a>
                    </div>
                </div>
                <div class="col-lg-6">
                    <div class="text-center">
                        <i class="fas fa-book-reader" style="font-size: 15rem; opacity: 0.1;"></i>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Statistics -->
    <section class="py-5">
        <div class="container">
            <div class="row">
                <div class="col-lg-4">
                    <div class="stats-card">
                        <div class="mb-3"><i class="fas fa-book text-primary" style="font-size: 3rem;"></i></div>
                        <h3 class="fw-bold text-primary">{book_count}</h3>
                        <p class="text-muted mb-0">精选图书</p>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="stats-card">
                        <div class="mb-3"><i class="fas fa-user-edit text-success" style="font-size: 3rem;"></i></div>
                        <h3 class="fw-bold text-success">{author_count}</h3>
                        <p class="text-muted mb-0">知名作者</p>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="stats-card">
                        <div class="mb-3"><i class="fas fa-building text-warning" style="font-size: 3rem;"></i></div>
                        <h3 class="fw-bold text-warning">{publisher_count}</h3>
                        <p class="text-muted mb-0">出版社</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Notice Section -->
    <section class="py-5 bg-light">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="card card-modern text-center">
                        <div class="card-body p-5">
                            <i class="fas fa-info-circle text-primary mb-3" style="font-size: 4rem;"></i>
                            <h3 class="fw-bold mb-3">静态演示版本</h3>
                            <p class="text-muted mb-4">
                                这是图书管理系统的静态演示版本。完整的功能需要Django服务器环境。
                                <br>本演示展示了系统的界面设计和基本布局。
                            </p>
                            <div class="d-flex gap-3 justify-content-center flex-wrap">
                                <a href="books.html" class="btn btn-primary-modern">浏览图书列表</a>
                                <a href="authors.html" class="btn btn-outline-primary">查看作者</a>
                                <a href="publishers.html" class="btn btn-outline-primary">出版社</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
    
    # Write home page
    with open(os.path.join(public_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(home_html)
    
    # Generate other static pages
    generate_books_page(public_dir, books)
    generate_authors_page(public_dir, authors)
    generate_publishers_page(public_dir, publishers)
    generate_static_notice(static_dir)
    
    print(f"Static files generated in {static_dir}/")

def generate_books_page(public_dir, books):
    """Generate static books page"""
    books_html = f"""
<!DOCTYPE html>
<html lang="zh-hans">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>图书列表 - 图书管理系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{ font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 0; }}
        .card-modern {{ background: white; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border: none; }}
        .price-tag {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 5px 15px; border-radius: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1 class="text-center">图书列表</h1>
            <p class="text-center">浏览我们的图书收藏</p>
        </div>
    </div>
    
    <div class="container py-5">
        <div class="row">
            {''.join([f'''
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card card-modern h-100">
                    <div class="card-body">
                        <h5 class="card-title">{book.name}</h5>
                        <p class="text-muted"><i class="fas fa-building"></i> {book.publisher.publisher_name}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="price-tag">¥{book.price}</span>
                            <small class="text-muted">库存: {book.inventory}</small>
                        </div>
                    </div>
                </div>
            </div>
            ''' for book in books[:12]])}
        </div>
        
        <div class="text-center mt-4">
            <a href="index.html" class="btn btn-outline-primary">返回首页</a>
        </div>
    </div>
</body>
</html>
"""
    
    with open(os.path.join(public_dir, 'books.html'), 'w', encoding='utf-8') as f:
        f.write(books_html)

def generate_authors_page(public_dir, authors):
    """Generate static authors page"""
    authors_html = f"""
<!DOCTYPE html>
<html lang="zh-hans">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>作者列表 - 图书管理系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{ font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 0; }}
        .card-modern {{ background: white; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border: none; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1 class="text-center">作者列表</h1>
            <p class="text-center">认识我们的作者</p>
        </div>
    </div>
    
    <div class="container py-5">
        <div class="row">
            {''.join([f'''
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card card-modern h-100">
                    <div class="card-body text-center">
                        <div class="mb-3">
                            <i class="fas fa-user-circle text-primary" style="font-size: 4rem;"></i>
                        </div>
                        <h5 class="card-title">{author.name}</h5>
                        <p class="text-muted">作品数量: {author.book.count()}</p>
                    </div>
                </div>
            </div>
            ''' for author in authors[:12]])}
        </div>
        
        <div class="text-center mt-4">
            <a href="index.html" class="btn btn-outline-primary">返回首页</a>
        </div>
    </div>
</body>
</html>
"""
    
    with open(os.path.join(public_dir, 'authors.html'), 'w', encoding='utf-8') as f:
        f.write(authors_html)

def generate_publishers_page(public_dir, publishers):
    """Generate static publishers page"""
    publishers_html = f"""
<!DOCTYPE html>
<html lang="zh-hans">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>出版社列表 - 图书管理系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {{ font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 60px 0; }}
        .card-modern {{ background: white; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); border: none; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1 class="text-center">出版社列表</h1>
            <p class="text-center">我们的合作出版社</p>
        </div>
    </div>
    
    <div class="container py-5">
        <div class="row">
            {''.join([f'''
            <div class="col-lg-6 mb-4">
                <div class="card card-modern h-100">
                    <div class="card-body">
                        <div class="d-flex align-items-center">
                            <div class="me-3">
                                <i class="fas fa-building text-primary" style="font-size: 3rem;"></i>
                            </div>
                            <div>
                                <h5 class="card-title mb-1">{publisher.publisher_name}</h5>
                                <p class="text-muted mb-0">
                                    <i class="fas fa-map-marker-alt"></i> {publisher.publisher_address}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            ''' for publisher in publishers[:12]])}
        </div>
        
        <div class="text-center mt-4">
            <a href="index.html" class="btn btn-outline-primary">返回首页</a>
        </div>
    </div>
</body>
</html>
"""
    
    with open(os.path.join(public_dir, 'publishers.html'), 'w', encoding='utf-8') as f:
        f.write(publishers_html)

def generate_static_notice(static_dir):
    """Generate notice page for admin/manager access"""
    notice_html = """
<!DOCTYPE html>
<html lang="zh-hans">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>管理员功能不可用 - 图书管理系统</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; }
        .notice-card { background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); padding: 60px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="notice-card">
                    <i class="fas fa-server text-warning mb-4" style="font-size: 5rem;"></i>
                    <h2 class="fw-bold mb-4">管理员功能需要服务器环境</h2>
                    <p class="text-muted mb-4">
                        这是图书管理系统的静态演示版本。管理员登录和数据管理功能需要Django服务器环境才能正常运行。
                    </p>
                    <div class="d-flex gap-3 justify-content-center flex-wrap">
                        <a href="/public/" class="btn btn-primary">
                            <i class="fas fa-home"></i> 返回首页
                        </a>
                        <a href="/public/books.html" class="btn btn-outline-primary">
                            <i class="fas fa-book"></i> 浏览图书
                        </a>
                    </div>
                    
                    <hr class="my-4">
                    
                    <h5 class="fw-bold mb-3">本地运行完整版本</h5>
                    <div class="text-start bg-light p-3 rounded">
                        <code>
                            # 克隆项目<br>
                            git clone [your-repo-url]<br>
                            cd book_Project<br><br>
                            
                            # 安装依赖<br>
                            pip install django pymysql<br><br>
                            
                            # 运行服务器<br>
                            python manage.py runserver<br><br>
                            
                            # 访问: http://127.0.0.1:8000/
                        </code>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    with open(os.path.join(static_dir, 'static-notice.html'), 'w', encoding='utf-8') as f:
        f.write(notice_html)

if __name__ == '__main__':
    create_static_files()
