from flask import Blueprint

# 创建蓝图对象
api_blue = Blueprint('api_blue', __name__)

# 导入当前模板
from . import views