from flask import Blueprint

project_blue = Blueprint('project_blue', __name__)  # 创建蓝图对象

from . import views
