from flask import render_template
from . import project_blue
from app.utils.common import login_required


# 项目列表
@project_blue.route('/admin/project')
@login_required
def index():
    return render_template('admin/project/index.html')


# 新增项目
@project_blue.route('/admin/project/create')
@login_required
def create():
    return render_template('admin/project/create.html')
