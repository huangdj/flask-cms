from flask import Blueprint

type_blue = Blueprint('type_blue', __name__)  # 创建蓝图对象

from . import views