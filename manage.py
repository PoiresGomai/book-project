import os
import sys


# 项目入口
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_Project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "未安装Django，或其他所需模块！"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
