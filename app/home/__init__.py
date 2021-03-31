from flask import Blueprint  # 引入蓝图模块
from app.models import Type, Area

home_blue = Blueprint('home_blue', __name__)  # 创建蓝图对象

from . import views  # 导入当前模块


@home_blue.context_processor
def view_share():
    return dict(types=Type.query.all(), areas=Area.query.all())
