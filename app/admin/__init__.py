from flask import Blueprint  # 引入 flask 自带的蓝图模块

admin_blue = Blueprint('admin_blue', __name__)  # 创建蓝图对象

from . import views  # 引入开发文件 views.py
