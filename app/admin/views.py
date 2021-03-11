from flask import render_template
from . import admin_blue  # 导入蓝图对象


# 后台首页路由
@admin_blue.route('/admin')
def index():
    return render_template('admin/index/index.html')
