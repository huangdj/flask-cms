from flask import render_template
from . import home_blue  # 导入蓝图对象


@home_blue.route('/')
def index():
    return render_template('home/index/index.html')
