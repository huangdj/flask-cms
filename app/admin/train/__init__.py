from flask import Blueprint

train_blue = Blueprint('train_blue', __name__)  # 创建蓝图对象

from . import views


@train_blue.context_processor
def view_share():
    return dict(_train='am-active')