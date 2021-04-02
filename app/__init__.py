from flask import Flask
from config import config, Config
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session  # 导入session扩展
from redis import StrictRedis  # 导入 Redis
from datetime import datetime
from flask_cors import *  # 导入跨域包

app = Flask(__name__)
db = SQLAlchemy()

# 实例化redis，用来临时缓存和业务逻辑相关的数据，比如说图片验证码、短信验证码、用户信息
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)


# 定义工厂函数，生产app
def create_app(config_name):
    CORS(app, supports_credentials=True)  # 获取实例
    app.config.from_object(config[config_name])  # 加载配置文件挪到工厂函数中

    db.init_app(app)  # 通过 init_app 去实例化db对象
    Session(app)  # 实例化Session

    # 定义时间日期格式化
    @app.template_filter('strftime')
    def _jinja2_filter_datetime(date, fmt=None):
        if fmt is None:
            fmt = '%Y年%m月%d日'
        return date.strftime(fmt)

    # 自定义全局辅助函数，根据当前时间显示礼貌提示语
    @app.context_processor
    def get_time():
        no = datetime.now().hour
        if no > 0 and no <= 6:
            return {"result": "凌晨好"}
        if no > 6 and no < 12:
            return {"result": "上午好"}
        if no >= 12 and no < 13:
            return {"result": "中午好"}
        if no >= 13 and no <= 18:
            return {"result": "下午好"}
        if no > 18 and no <= 24:
            return {"result": "晚上好"}

    # 前台首页蓝图
    from app.home import home_blue
    app.register_blueprint(home_blue)

    # 后台首页蓝图
    from app.admin import admin_blue
    app.register_blueprint(admin_blue)

    # 后台项目类型蓝图
    from app.admin.type import type_blue
    app.register_blueprint(type_blue)

    # 后台区域蓝图
    from app.admin.area import area_blue
    app.register_blueprint(area_blue)

    # 后台所有项目蓝图
    from app.admin.project import project_blue
    app.register_blueprint(project_blue)

    # 后台培训服务蓝图
    from app.admin.train import train_blue
    app.register_blueprint(train_blue)

    # 留言板接口
    from app.api import api_blue
    app.register_blueprint(api_blue)

    return app  # 最后返回当前app
