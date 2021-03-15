from flask import Blueprint

area_blue = Blueprint('area_blue', __name__)  # 创建蓝图对象

from . import views


@area_blue.context_processor
def view_share():
    return dict(_area='am-active')
