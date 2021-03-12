from flask import Blueprint

type_blue = Blueprint('type_blue', __name__)  # 创建蓝图对象

from . import views


@type_blue.context_processor
def view_share():
    return dict(_type='am-active')
