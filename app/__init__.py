from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session  # 导入session扩展

app = Flask(__name__)
db = SQLAlchemy()

app.config.from_object(config['development'])


# 定义工厂函数，生产app
def create_app(config_name):
    app.config.from_object(config[config_name])  # 加载配置文件挪到工厂函数中

    db.init_app(app)  # 通过 init_app 去实例化db对象
    Session(app)  # 实例化Session

    # 注册前台蓝图
    from app.home import home_blue
    app.register_blueprint(home_blue)

    return app  # 最后返回当前app
