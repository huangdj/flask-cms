from flask import Flask
from config import config, Config
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session  # 导入session扩展
from redis import StrictRedis  # 导入 Redis

app = Flask(__name__)
db = SQLAlchemy()

# 实例化redis，用来临时缓存和业务逻辑相关的数据，比如说图片验证码、短信验证码、用户信息
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)


# 定义工厂函数，生产app
def create_app(config_name):
    app.config.from_object(config[config_name])  # 加载配置文件挪到工厂函数中

    db.init_app(app)  # 通过 init_app 去实例化db对象
    Session(app)  # 实例化Session

    # 前台首页蓝图
    from app.home import home_blue
    app.register_blueprint(home_blue)

    # 后台首页蓝图
    from app.admin import admin_blue
    app.register_blueprint(admin_blue)

    return app  # 最后返回当前app
