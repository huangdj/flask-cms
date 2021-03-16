from flask import Blueprint
from app.models import Type, Area

project_blue = Blueprint('project_blue', __name__)  # 创建蓝图对象

from . import views


@project_blue.context_processor
def view_share():
    return dict(_project='am-active', types=Type.query.all(), areas=Area.query.all())
